import gradio as gr
import json
import urllib.request
import urllib.parse
import uuid
import websocket
import random
import requests
import os
import io
import re
from pathlib import Path
from PIL import Image

# --- CONFIGURATION ---
COMFYUI_SERVER_ADDRESS = "127.0.0.1:8188" 
CLIENT_ID = str(uuid.uuid4())
WORKFLOW_FILE = "workflow_api_img2img.json" 
OUTPUT_BASE_DIR = Path("comfy_outputs").resolve()

# --- UTILS & SECURITY ---
def sanitize_name(name):
    name = str(name).strip().replace(" ", "_")
    name = re.sub(r'(?u)[^-\w]', '', name)
    return name if name else "untitled"

def get_ascii_bar(current, total, width=20):
    """Generates a visual progress bar for the terminal."""
    percent = float(current) / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {int(percent * 100)}%"

# --- API COMMUNICATION ---
def upload_image(filepath):
    with open(filepath, 'rb') as f:
        files = {'image': f}
        response = requests.post(f"http://{COMFYUI_SERVER_ADDRESS}/upload/image", files=files)
    return response.json()

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{COMFYUI_SERVER_ADDRESS}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{COMFYUI_SERVER_ADDRESS}/view?{url_values}") as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{COMFYUI_SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def generate_single_image(input_image_path):
    if not os.path.exists(WORKFLOW_FILE):
        raise FileNotFoundError(f"Workflow file '{WORKFLOW_FILE}' not found.")
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        prompt_workflow = json.load(f)

    internal_seed = random.randint(1, 10**14)
    if input_image_path is not None:
        image_info = upload_image(input_image_path)
        filename_on_server = image_info["name"]
        for node_id, node_data in prompt_workflow.items():
            if node_data.get("class_type") == "LoadImage":
                prompt_workflow[node_id]["inputs"]["image"] = filename_on_server
            if node_data.get("class_type") == "KSampler":
                prompt_workflow[node_id]["inputs"]["seed"] = internal_seed
        
    ws = websocket.WebSocket()
    ws.connect(f"ws://{COMFYUI_SERVER_ADDRESS}/ws?clientId={CLIENT_ID}")
    prompt_id = queue_prompt(prompt_workflow)['prompt_id']
    
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing' and message['data']['node'] is None and message['data']['prompt_id'] == prompt_id:
                break
    
    history = get_history(prompt_id)[prompt_id]
    output_image_data = None
    for node_id in history['outputs']:
        if 'images' in history['outputs'][node_id]:
            for image in history['outputs'][node_id]['images']:
                output_image_data = get_image(image['filename'], image['subfolder'], image['type'])
    ws.close()
    return output_image_data

# --- TERMINAL PROCESSOR ---
def batch_process_generator(list_of_images, folder_name_input, progress=gr.Progress()):
    if not list_of_images:
        yield [], "❌ TERMINAL ERROR: No source files."
        return

    safe_folder_name = sanitize_name(folder_name_input)
    target_dir = OUTPUT_BASE_DIR / safe_folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    current_gallery = []
    total = len(list_of_images)
    
    for i, img_path in enumerate(list_of_images):
        original_filename = os.path.basename(img_path.name)
        
        # ASCII progress bar for the terminal box
        ascii_progress = get_ascii_bar(i, total)
        log_msg = f"COLORING SESSION: {safe_folder_name}\n{ascii_progress}\nCURRENT: {original_filename}"
        
        yield current_gallery, log_msg
        
        try:
            img_bytes = generate_single_image(img_path.name)
            if img_bytes:
                pil_img = Image.open(io.BytesIO(img_bytes))
                safe_name = sanitize_name(os.path.splitext(original_filename)[0]) + ".png"
                pil_img.save(target_dir / safe_name)
                current_gallery.append((pil_img, safe_name))
                
                # Intermediate update
                yield current_gallery, f"COLORING SESSION: {safe_folder_name}\n{get_ascii_bar(i+1, total)}\n✅ SUCCESS: {safe_name}"
        except Exception as e:
            yield current_gallery, f"COLORING SESSION: {safe_folder_name}\n{ascii_progress}\n❌ ERROR: {str(e)}"

    final_log = f"COLORING SESSION: {safe_folder_name}\n{get_ascii_bar(total, total)}\n✨ SESSION COMPLETE. {total} IMAGES SAVED."
    yield current_gallery, final_log

# --- CYBER-AMETHYST V3.0 STYLE (GRADIO 6.0) ---

custom_css = """
.gradio-container { background: radial-gradient(circle at top, #1e1b4b 0%, #020617 100%); }

/* Extreme Bold Labels */
.block label span { 
    font-weight: 900 !important; 
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #a5b4fc !important;
}

/* ANTI-FADE: Gallery stays bright always */
.pending, .generating, .progress-parent, .processing { 
    opacity: 1 !important; 
    filter: none !important; 
}

h1 { font-weight: 900; letter-spacing: -1px; }
h1, h2, h3, p, span { color: #a5b4fc !important; }

/* Hacker Terminal Style */
#status_box { 
    background-color: #000000 !important; 
    color: #22d3ee !important; 
    border: 2px solid #312e81; 
    font-family: 'Consolas', 'Fira Code', monospace; 
    font-size: 0.9em;
    box-shadow: inset 0 0 10px #1e1b4b;
}

.generate-btn { 
    background: linear-gradient(90deg, #7c3aed 0%, #db2777 100%) !important; 
    border: none !important; 
    color: #cffafe !important; 
    font-weight: 900 !important; 
    height: 60px !important;
    font-size: 1.2em !important;
}

#gallery_output { 
    border-radius: 12px; 
    border: 2px solid #312e81; 
    background: #080a14; 
    opacity: 1 !important; 
}

footer { display: none !important; }
input, textarea { color: #22d3ee !important; font-weight: 600; }
"""

theme = gr.themes.Base(
    primary_hue="violet",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont('Rajdhani'), 'sans-serif'],
).set(
    body_background_fill="#020617",
    block_background_fill="#0f172a",
    block_border_color="#312e81",
    body_text_color="#a5b4fc",
    block_title_text_color="#818cf8",
    block_label_text_color="#6366f1",
    button_primary_background_fill="#7c3aed",
    button_primary_text_color="#cffafe",
)

# --- BUILD ---
with gr.Blocks(title="Manga Coloring Tool") as app:
    with gr.Row():
        gr.Markdown("# ⚡ MANGA COLORING TOOL")
    
    with gr.Row(equal_height=True):
        # LEFT COLUMN (CONTROLS & TERMINAL)
        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("### ⚙️ PARAMETERS")
            folder_input = gr.Textbox(label="Session Folder Name", value="manga_chapter_01")
            input_files = gr.File(label="Upload Manga Pages", file_count="multiple", file_types=["image"])
            
            gr.Markdown("### 📟 ACTIVITY TERMINAL")
            status_output = gr.Textbox(
                show_label=False, 
                placeholder="SYSTEM IDLE...", 
                elem_id="status_box", 
                lines=5,
                interactive=False
            )
            
            btn_generate = gr.Button("🚀 START COLORIZATION", variant="primary", elem_classes="generate-btn")

        # RIGHT COLUMN (RESULTS)
        with gr.Column(scale=2):
            gr.Markdown("### 🖼️ LIVE OUTPUT GALLERY")
            output_gallery = gr.Gallery(
                show_label=False, 
                elem_id="gallery_output", 
                columns=3, 
                height=700, 
                object_fit="contain"
            )

    btn_generate.click(
        fn=batch_process_generator, 
        inputs=[input_files, folder_input], 
        outputs=[output_gallery, status_output]
    )

if __name__ == "__main__":
    OUTPUT_BASE_DIR.mkdir(exist_ok=True)
    app.queue().launch(
        inbrowser=False, 
        theme=theme, 
        css=custom_css
    )