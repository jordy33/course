# Estructura de YAML para Slides de Cursos de Aprendizaje

Este documento describe la estructura de los archivos YAML utilizados para crear slides individuales en cursos o proyectos de aprendizaje interactivos, como slideshows o videos educativos. El formato está diseñado para ser flexible y fácil de generar con LLMs (como GPT o Claude), permitiendo crear contenido educativo estructurado.

## Propósito
Cada archivo YAML representa un slide individual, con contenido visual (texto, imágenes, diagramas Mermaid), script narrativo para TTS (Text-to-Speech), y metadatos de módulo y slide. Esto facilita la generación automática de presentaciones y videos.

## Estructura General
Cada archivo YAML (e.g., `slide_1_1.yaml`) debe contener las siguientes claves obligatorias:

- `content` (string): Descripción completa del slide, incluyendo texto principal, bullets, imágenes y diagramas Mermaid.
- `script` (array de strings): Lista de frases o párrafos para el audio narrativo. Cada elemento es una oración o segmento corto para TTS.
- `module_id` (number): Identificador del módulo (empezando desde 1).
- `slide_id` (number): Identificador del slide dentro del módulo (empezando desde 1).

### Detalles de `content`
- Texto principal: Título, explicaciones, bullets (usa `•` para bullets).
- Imágenes: "Imagen de ejemplo: [URL accesible]" (opcional).
- Diagramas: "Usa este Mermaid: mermaid\n[código Mermaid válido]" (opcional).
- Ejemplo: "Slide 1: Introducción a Git. • Punto 1 • Punto 2. Usa este Mermaid: mermaid\ngraph TD\nA --> B"

### Detalles de `script`
- Array de strings en español (o idioma deseado).
- Cada string debe ser natural para voz, clara y educativa.
- Ejemplo: ["¡Bienvenidos!", "Git es un sistema de control de versiones."]

### Reglas y Convenciones
- **Idioma**: Scripts en español por defecto. Contenido en español o inglés según necesidad.
- **Mermaid**: Código válido (ver mermaid.live). Evita `\n` en etiquetas; usa espacios para multilínea.
- **Imágenes**: URLs accesibles. Si no hay, omitir.
- **Validación**: YAML válido. Usa herramientas como yamlvalidator.com.
- **Extensibilidad**: Agrega claves opcionales si necesario, pero mantén compatibilidad.

### Ejemplo de YAML Completo
```yaml
content: "Slide 1: Introducción a Git. • Git es un VCS. • Permite rastrear cambios. Imagen de ejemplo: https://git-scm.com/images/logos/downloads/Git-Logo-2Color.png. Usa este Mermaid: mermaid\ngraph TD\nA[Usuario] --> B[Git] --> C[Repositorio]"
script:
  - "¡Bienvenidos a este curso básico de Git!"
  - "Git es un sistema de control de versiones que permite rastrear cambios en el código."
module_id: 1
slide_id: 1
```

### Scripts de Generación
- `generate_slides.py`: Crea imágenes PNG desde YAML (texto + imágenes + Mermaid).
- `generate_sound.py`: Genera WAV desde scripts usando Kokoro TTS.
- `generate_video.py`: Combina slides y audio en MP4 con transiciones.

## Generación de YAMLs con LLMs

Los archivos YAML individuales se generan a partir de prompts para LLMs. Un LLM puede crear el contenido completo de un curso nuevo siguiendo estos pasos:

### 1. Prompt para LLM
Usa un prompt como este para generar contenido por slide:

```
Eres un experto educador. Genera contenido para un slide específico de un curso sobre [TEMA, ej. "Git Básico"]. El slide pertenece al módulo [NÚMERO, ej. 1], slide [NÚMERO, ej. 1].

Proporciona:
- content: Descripción del slide en string, incluyendo texto, bullets (usa •), imágenes ("Imagen de ejemplo: URL"), y Mermaid si aplica ("Usa este Mermaid: mermaid\ncódigo").
- script: Array de strings en español, natural para voz, explicando el contenido.
- module_id: [NÚMERO]
- slide_id: [NÚMERO]

Ejemplo de Mermaid: graph TD\nA[Inicio] --> B[Proceso]

Asegúrate de que sea educativo, conciso y válido YAML.
```

### 2. Generación de Diagramas Mermaid
- **Tipos comunes**: `graph TD` para vertical, `graph LR` para horizontal, `flowchart` para flujos.
- **Etiquetas**: Usa espacios en lugar de \n para multilínea (e.g., "Texto largo aquí").
- **Validación**: Prueba en https://mermaid.live.

### 3. Mejores Prácticas para LLMs
- **Claridad**: Scripts naturales, sin jerga compleja.
- **Visuales**: URLs de imágenes libres (Unsplash).
- **Corrección**: Revisa errores tipográficos (e.g., "git" no "guit").
- **Idioma**: Español para scripts y contenido.

Esto permite escalar la creación de cursos de manera automatizada.

### Cómo Generar con LLMs
- Proporciona este documento como prompt base.
- Especifica el tema (ej. "Genera un curso sobre Python básico con 5 módulos").
- Incluye ejemplos de Mermaid si el tema lo requiere (ej. diagramas de flujo para algoritmos).
- Valida el output JSON con un parser.

### Herramientas Recomendadas para Procesar
- **Validación**: Usa Python con `yaml` module (import yaml; yaml.safe_load(file)).
- **Renderizado**: Mermaid-CLI para diagramas, Pillow para imágenes compuestas.
- **Slideshow**: Reveal.js para web, FFmpeg para videos.

#### Instalación de Dependencias
Para macOS, usa el script incluido `install_dependencies.sh` para instalar automáticamente Homebrew, FFmpeg, Node.js, Mermaid-CLI y Chrome Headless. Ejecuta `./install_dependencies.sh` después de hacer el script ejecutable con `chmod +x install_dependencies.sh`.

Para otros sistemas o instalación manual, sigue estos pasos:

1. **Python 3.8+** y paquetes:
   - Crea un entorno virtual: `python -m venv .venv`
   - Activa: `source .venv/bin/activate` (macOS/Linux) o `.venv\Scripts\activate` (Windows)
   - Instala: `pip install -r requirements.txt`

2. **FFmpeg** (para procesamiento de audio y video):
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`
   - Windows: Descarga de https://ffmpeg.org/download.html

3. **Mermaid-CLI** (para renderizar diagramas Mermaid):
   - `npm install -g @mermaid-js/mermaid-cli`
   - Requiere Node.js y npm instalados.

4. **Chrome Headless** (requerido por Mermaid-CLI):
   - `npx puppeteer browsers install chrome`

5. **Kokoro TTS Server** (para generación de audio):
   - Clona y ejecuta el servidor local: https://github.com/jordy33/kokoro-tts
   - Asegúrate de que esté corriendo en `http://localhost:8880`

Asegúrate de tener Node.js, npm y Python instalados. Para macOS, usa Homebrew para instalar dependencias del sistema.
