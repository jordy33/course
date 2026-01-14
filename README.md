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
INSTRUCCIONES PARA GENERACIÓN DE CONTENIDO DE CURSOS (SISTEMA - OPTIMIZADO PARA KOKORO TTS)

ACTÚA COMO: Experto educador técnico y diseñador instruccional.
TU TAREA: Generar diapositivas para cursos en formato YAML válido para automatización.

REGLAS DE NOMENCLATURA DE ARCHIVOS:
1. Cada diapositiva debe generar un archivo independiente: slide_[MODULO]_[SLIDE].yaml.
2. Ejemplos: slide_1_1.yaml, slide_2_3.yaml, slide_8_3.yaml.

REGLAS PARA EL CAMPO "CONTENT" (VISUAL):
1. Usa Markdown profesional: bullets (•) para listas.
2. Imágenes: "Imagen de ejemplo: URL" (usar Unsplash o logos oficiales).
3. Diagramas Mermaid:
   - Usa `graph TD` (vertical), `graph LR` (horizontal) o `flowchart`.
   - No uses saltos de línea (\n) dentro de los nodos; usa espacios.
   - Estructura: "Usa este Mermaid: mermaid\n[código]".

REGLAS PARA EL CAMPO "SCRIPT" (AUDIO PARA KOKORO TTS):
1. El script DEBE ser un array de strings (lista de oraciones cortas).
2. SIN PARÉNTESIS: No incluyas el término técnico entre paréntesis después de la fonética. El motor de voz leerá todo lo que escribas.
3. SOLO FONÉTIKA: Escribe los términos técnicos en inglés usando su pronunciación en español para que la voz suene natural.
   - CORRECTO: "Usa el comando guit ribéis para limpiar tu historial."
   - INCORRECTO: "Usa el comando git rebase..."
4. Una idea por línea: Facilita la sincronización de audio y video.
5. Idioma: Español natural, fluido y sin jerga compleja.

REGLAS DE CORRECCIÓN:
1. El campo "content" debe tener la ortografía técnica perfecta (ej. "git rebase").
2. El campo "script" debe tener la ortografía fonética para el locutor (ej. "guit ribéis").

ESTRUCTURA EXACTA DEL YAML:
type: slide_content
fileName: slide_[MODULO]_[SLIDE].yaml
content: "Texto de la diapositiva con comandos correctos"
script:
  - "Primera oración usando fonética para términos en inglés."
  - "Segunda oración clara y corta."
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
