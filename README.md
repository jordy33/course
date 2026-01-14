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
- Imágenes: "Imagen de ejemplo: URL" (opcional). Solo se soporta una imagen por slide (la primera encontrada).
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

### Instalación de Dependencias
Para macOS, usa el script incluido `install_dependencies.sh` para instalar automáticamente Homebrew, FFmpeg, Node.js, Mermaid-CLI y Chrome Headless. Ejecuta `./install_dependencies.sh` después de hacer el script ejecutable con `chmod +x install_dependencies.sh`.
Después de instalar las dependencias del sistema, configura el entorno virtual de Python y instala los paquetes requeridos.
Sigue estos pasos:

##### Configuración del Entorno Virtual
1. **Crear el entorno virtual**:
   - Ejecuta: `python -m venv .venv`
   - Esto crea la carpeta `.venv` con el entorno aislado.

2. **Activar el entorno virtual**:
   - macOS/Linux: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
   - Verás `(.venv)` en el prompt indicando que está activado.

3. **Instalar dependencias de Python**:
   - Ejecuta: `pip install -r requirements.txt`
   - Esto instala PyYAML, Pillow y requests.

##### Otras Dependencias

1. **Kokoro TTS Server** (para generación de audio):
   - Clona y ejecuta el servidor local: https://github.com/jordy33/kokoro-tts
   - Asegúrate de que esté corriendo en `http://localhost:8880`

Asegúrate de tener Node.js, npm y Python instalados. Para macOS, usa Homebrew para instalar dependencias del sistema.

### Scripts de Generación
- `generate_slides.py`: Crea imágenes PNG desde YAML (texto + imágenes + Mermaid).
- `generate_sound.py`: Genera WAV desde scripts usando Kokoro TTS.
- `generate_video.py`: Combina slides y audio en MP4 con transiciones.

#### Uso de los Scripts
Los scripts se ejecutan desde la raíz del proyecto. Asegúrate de tener el entorno virtual activado (`source .venv/bin/activate`) y las dependencias instaladas.

- **Generar todos los slides**: `python generate_slides.py`
  - Crea la carpeta `slides/` con imágenes PNG para todos los slides en `slide_yamls/`.

- **Generar un slide específico**: `python generate_slides.py [module_id] [slide_id]`
  - Ejemplo: `python generate_slides.py 1 2` genera solo `slides/slide_1_2.png`.
  - Útil para arreglar o actualizar un slide sin regenerar todos.

- **Generar todos los sonidos**: `python generate_sound.py`
  - Crea la carpeta `slide_sounds/` con archivos WAV para todos los slides.

- **Generar un sonido específico**: `python generate_sound.py [module_id] [slide_id]`
  - Ejemplo: `python generate_sound.py 3 1` genera solo `slide_sounds/sound_3_1.wav`.
  - Ideal para corregir el audio de un slide (e.g., después de editar el script en YAML).

- **Generar el video completo**: `python generate_video.py`
  - Crea `videos/final_presentation.mp4` combinando todos los slides y audios con transiciones y pausas.

- **Generar video para un slide específico**: `python generate_video.py [module_id] [slide_id]`
  - Ejemplo: `python generate_video.py 2 3` genera un video solo para ese slide.
  - Útil para probar o arreglar una parte del video.

**Notas**:
- Los archivos generados (*.png, *.wav, *.mp4) están ignorados en `.gitignore` para no subirlos al repo.
- Si editas un YAML, regenera el slide/sonido correspondiente para aplicar cambios.
- El video incluye fades y pausas automáticas; edita `generate_video.py` para ajustar tiempos.

## Generación de YAMLs con LLMs

Los archivos YAML individuales se generan a partir de prompts para LLMs. Un LLM puede crear el contenido completo de un curso nuevo siguiendo estos pasos:

### Instrucciones para el Generador de Cursos (System Prompt)

Pasa este prompt completo a tu LLM para generar slides en YAML:

```
INSTRUCCIONES PARA GENERACIÓN DE CONTENIDO DE CURSOS (SISTEMA)

ACTÚA COMO: Experto educador técnico y diseñador instruccional.
TU TAREA: Generar diapositivas para cursos en formato YAML válido para automatización.

REGLAS DE NOMENCLATURA DE ARCHIVOS:
1. Cada diapositiva debe generar un archivo independiente siguiendo este patrón: slide_[MODULO]_[SLIDE].yaml.
2. Ejemplos de nombres válidos: slide_1_1.yaml, slide_2_3.yaml, slide_7_3.yaml, slide_8_3.yaml.

REGLAS PARA EL CAMPO "CONTENT":
1. Usa Markdown limpio y profesional.
2. Usa bullets (•) para listas y `acentos graves` para comandos técnicos.
3. Imágenes: Usa URLs de imágenes libres de derechos (ej. Unsplash). Formato: "Imagen de ejemplo: URL".
4. Generación de Diagramas Mermaid:
   - Tipos: Usar `graph TD` (vertical), `graph LR` (horizontal) o `flowchart`.
   - Etiquetas: Usa espacios en lugar de saltos de línea (\n) para textos largos (e.g., [Texto largo aquí]).
   - Estructura: "Usa este Mermaid: mermaid\n[código]".
   - Validación: El código debe ser funcional para probarse en https://mermaid.live.

REGLAS PARA EL CAMPO "SCRIPT" (SISTEMA DE VOZ):
1. El script DEBE ser un array de strings (lista de oraciones).
2. Cada oración debe estar en una línea nueva precedida por un guion (-).
3. Divide el texto en oraciones cortas y simples. Una idea por línea.
4. Fonética: Incluye la pronunciación entre paréntesis para términos en inglés (ej. "Guit" para Git, "Bránching" para Branching).
5. Idioma: Todo el contenido y script debe ser en español natural, sin jerga compleja innecesaria.

REGLAS DE CORRECCIÓN Y CALIDAD:
1. Revisa errores tipográficos: Asegúrate de que los comandos sean correctos (ej. "git" en el contenido, aunque en el script de voz uses "guit").
2. Claridad: Scripts naturales que permitan escalar la creación de cursos de manera automatizada.

ESTRUCTURA EXACTA DEL YAML:
type: slide_content
fileName: slide_[MODULO]_[SLIDE].yaml
content: "Texto de la diapositiva"
script:
  - "Primera oración corta para el locutor."
  - "Segunda oración corta para el locutor."
module_id: [NÚMERO]
slide_id: [NÚMERO]
```

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
