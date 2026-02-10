# 🎨 FLUX.2 Klein Manga Colorizer (v1.0 - 2026)

![Status](https://img.shields.io/badge/Status-Beta-yellow) ![Engine](https://img.shields.io/badge/Engine-FLUX.2--Klein-purple) ![Optimization](https://img.shields.io/badge/Model-FP8-green) ![Platform](https://img.shields.io/badge/UI-Gradio-orange)

El colorizador de manga definitivo basado en la arquitectura de última generación **FLUX.2 Klein 4B (FP8)**. Este software permite transformar dibujos en blanco y negro (lineart) en piezas coloreadas profesionalmente en segundos, optimizando el uso de la VRAM para funcionar en hardware doméstico.

---

## ⚡ Instalación y Ejecución Directa

Este proyecto está diseñado para ser portable y fácil de usar. Sigue estos pasos tras descomprimir el archivo `.zip`:

1. **Requisitos de Sistema:**
   - **GPU:** NVIDIA (Serie 3000 o superior recomendada) con **8GB de VRAM** mínimo.
   - **RAM:** 16GB.
   - **Espacio:** 15GB libres (para el modelo y dependencias).
   - **Python:** Tener instalado [Python 3.10+](https://www.python.org/).

2. **Acceso al Modelo (Hugging Face):**
   - El modelo es de acceso restringido. Debes aceptar los términos en [HF: FLUX.2 Klein](https://huggingface.co/black-forest-labs/FLUX.2-klein-4b-fp8).
   - Loguéate en tu terminal una sola vez:
     ```bash
     pip install huggingface_hub
     huggingface-cli login
     ```

3. **¡Lanzar con un Clic!:**
   - Haz doble clic en el archivo `run_app.bat`. 
   - El script configurará automáticamente el entorno virtual (`venv`), instalará los requisitos y abrirá la interfaz en tu navegador.

---

## 🖥️ Guía de la Interfaz y Uso



### 📥 Entrada de Datos
* **Main Manga Input:** Sube tu imagen en B/N. Funciona mejor con lineart definido y limpio.
* **Color References:** Puedes subir hasta **3 imágenes de referencia**. El sistema extraerá la estética y los tonos de estas imágenes para aplicarlos de forma coherente a tu dibujo.

### ⚙️ Ajustes de Generación
* **Strength (Fuerza de Cambio):** * `0.5`: Mantiene el dibujo original casi intacto, añade colores suaves.
    * `0.7`: **(Recomendado)** Equilibrio perfecto entre respetar tu línea y aplicar sombreado profesional.
    * `0.9`: Da más libertad a la IA para reinterpretar luces y volúmenes.
* **Guidance Scale:** Ajusta qué tan "vibrantes" o saturados serán los colores según el prompt interno.

### 📤 Salida
* El resultado aparecerá a la derecha. Puedes guardar la imagen haciendo clic derecho o usando el botón de descarga integrado.

---

## 🌟 Resultados y Capacidades

Este software no es un simple "relleno de cubeta". Gracias a **FLUX.2 Klein**, obtendrás:
* **Sombreado Cel-Shading:** Sombras nítidas y profesionales típicas del anime moderno.
* **Fusión de Referencias:** Capacidad de mezclar colores de diferentes imágenes para crear una paleta única.
* **Preservación de Detalles:** Los tramados y texturas originales del manga se respetan en gran medida.

---

## ❤️ Créditos y Ecosistema Open Source

Este proyecto es una realidad gracias a las tecnologías abiertas que impulsan la IA en 2026:

* **[Black Forest Labs](https://blackforestlabs.ai/):** Por desarrollar la revolucionaria arquitectura **FLUX**.
* **[ComfyUI](https://github.com/comfyanonymous/ComfyUI):** Cuya innovadora gestión de memoria y flujo de trabajo por nodos inspiró la optimización de este motor para GPUs de 8GB.
* **[Hugging Face](https://huggingface.co/):** Por facilitar la distribución de modelos y la librería `diffusers`.
* **[Gradio](https://gradio.app/):** Por permitir crear interfaces potentes y sencillas.
* **[Pytorch & NVIDIA](https://pytorch.org/):** Por el soporte técnico de aceleración por hardware (CUDA/FP8).

---
*Desarrollado para la comunidad de artistas y entusiastas del manga - 2026.*