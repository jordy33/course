import yaml
import os
import re
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import glob
import sys

def validate_json(data):
    """Valida la estructura del JSON."""
    errors = []
    if not isinstance(data, dict):
        errors.append("El JSON raíz debe ser un objeto.")
        return errors
    
    required_keys = ['course_title', 'description', 'modules']
    for key in required_keys:
        if key not in data:
            errors.append(f"Falta la clave obligatoria: {key}")
        elif key != 'modules' and not isinstance(data[key], str):
            errors.append(f"{key} debe ser una string.")
    
    if 'modules' in data and not isinstance(data['modules'], list):
        errors.append("modules debe ser un array.")
    else:
        for i, module in enumerate(data['modules']):
            if not isinstance(module, dict):
                errors.append(f"Módulo {i+1}: Debe ser un objeto.")
                continue
            mod_keys = ['id', 'title', 'duration_estimate', 'script', 'slides']
            for k in mod_keys:
                if k not in module:
                    errors.append(f"Módulo {i+1}: Falta {k}")
                elif k == 'id' and not isinstance(module[k], int):
                    errors.append(f"Módulo {i+1}: id debe ser number.")
                elif k == 'slides' and not isinstance(module[k], list):
                    errors.append(f"Módulo {i+1}: slides debe ser array.")
                elif k != 'id' and k != 'slides' and not isinstance(module[k], str):
                    errors.append(f"Módulo {i+1}: {k} debe ser string.")
            if 'slides' in module:
                for j, slide in enumerate(module['slides']):
                    if not isinstance(slide, str):
                        errors.append(f"Módulo {i+1}, Slide {j+1}: Debe ser string.")
    return errors

def extract_slide_parts(slide_text):
    """Extrae texto, URL de imagen y código Mermaid del slide."""
    text = slide_text
    image_url = None
    mermaid_code = None
    
    # Remover "Slide X: " del inicio
    text = re.sub(r'^Slide \d+: ', '', text).strip()
    
    # Buscar imagen
    img_match = re.search(r'Imagen de ejemplo:\s*(https?://[^\s]+)', slide_text)
    if img_match:
        image_url = img_match.group(1).strip()
        text = re.sub(r'Imagen de ejemplo:\s*https?://[^\s]+', '', text).strip()
    
    # Buscar Mermaid
    mermaid_match = re.search(r'Usa este Mermaid:\s*mermaid\s*(.+)', slide_text, re.DOTALL)
    if mermaid_match:
        mermaid_code = mermaid_match.group(1).strip()
        text = re.sub(r'Usa este Mermaid:\s*mermaid\s*.+', '', text, flags=re.DOTALL).strip()
    
    return text, image_url, mermaid_code

def render_mermaid(code, output_path):
    """Renderiza código Mermaid a PNG usando mermaid-cli."""
    chrome_path = "/Users/jorgemacias/.cache/puppeteer/chrome/mac_arm-143.0.7499.192/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    env = os.environ.copy()
    env['PUPPETEER_EXECUTABLE_PATH'] = chrome_path
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        subprocess.run(['mmdc', '-i', temp_file, '-o', output_path], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error renderizando Mermaid: {e}")
        return False
    finally:
        os.unlink(temp_file)
    return True

def create_slide_image(text, image_url, mermaid_png, output_path, width=1920, height=1080):
    """Crea una imagen PNG para el slide usando Pillow."""
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 50)
        small_font = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 20)  # Para footer
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Logo en header
    logo_url = "https://git-scm.com/images/logos/downloads/Git-Logo-2Color.png"
    header_y = 20
    try:
        response = requests.get(logo_url)
        logo = Image.open(BytesIO(response.content))
        logo.thumbnail((200, 100))
        logo_x = (width - logo.width) // 2
        img.paste(logo, (logo_x, header_y))
        header_bottom = header_y + logo.height + 20
    except Exception as e:
        print(f"Error cargando logo: {e}")
        header_bottom = 50
    
    # Footer
    footer_text = "Madd Systems Group"
    bbox_footer = draw.textbbox((0, 0), footer_text, font=small_font)
    footer_y = height - 50
    footer_x = (width - (bbox_footer[2] - bbox_footer[0])) // 2
    draw.text((footer_x, footer_y), footer_text, fill='black', font=small_font)
    
    # Calcular altura del contenido
    lines = text.split('\n') if '\n' in text else [text]
    text_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] + 20 for line in lines)
    
    content_height = text_height
    if image_url and image_url != logo_url:
        content_height += 450  # Espacio para imagen
    if mermaid_png and os.path.exists(mermaid_png):
        diagram = Image.open(mermaid_png)
        diagram.thumbnail((800, 600))
        content_height += diagram.height + 50
    
    # Centrar verticalmente el contenido entre header y footer
    available_height = footer_y - header_bottom
    content_start_y = header_bottom + (available_height - content_height) // 2
    
    current_y = content_start_y
    
    # Agregar texto
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, current_y), line, fill='black', font=font)
        current_y += bbox[3] - bbox[1] + 20
    
    # Agregar imagen adicional
    if image_url and image_url != logo_url:
        try:
            response = requests.get(image_url)
            img_data = Image.open(BytesIO(response.content))
            img_data.thumbnail((600, 400))
            img_x = (width - img_data.width) // 2
            img.paste(img_data, (img_x, current_y))
            current_y += img_data.height + 50
        except Exception as e:
            print(f"Error cargando imagen {image_url}: {e}")
    
    # Agregar diagrama
    if mermaid_png and os.path.exists(mermaid_png):
        diagram = Image.open(mermaid_png)
        diagram.thumbnail((800, 600))
        diag_x = (width - diagram.width) // 2
        img.paste(diagram, (diag_x, current_y))
    
    img.save(output_path)
    
    img.save(output_path)
    
    img.save(output_path)

def main():
    """Función principal para generar slides."""
    try:
        slide_files = glob.glob('slide_yamls/slide_*.yaml')
        slides = []
        for file in slide_files:
            with open(file, 'r', encoding='utf-8') as f:
                slide_data = yaml.safe_load(f)
            slides.append(slide_data)
        slides.sort(key=lambda x: (x['module_id'], x['slide_id']))
    except Exception as e:
        print(f"Error cargando slides: {e}")
        return
    
    # Check for command-line arguments to generate only specific slide
    if len(sys.argv) == 3:
        try:
            target_module = int(sys.argv[1])
            target_slide = int(sys.argv[2])
            slides = [s for s in slides if s['module_id'] == target_module and s['slide_id'] == target_slide]
            if not slides:
                print(f"Slide {target_module}_{target_slide} no encontrado.")
                return
        except ValueError:
            print("Argumentos inválidos. Usa: python generate_slides.py [module_id] [slide_id]")
            return
    
    print("Slides cargados. Generando slides...")
    
    os.makedirs('slides', exist_ok=True)
    
    for slide_data in slides:
        module_id = slide_data['module_id']
        slide_idx = slide_data['slide_id'] - 1  # slide_id starts from 1, but for temp files use 0-based
        slide_text = slide_data['content']
        
        text, image_url, mermaid_code = extract_slide_parts(slide_text)
        
        mermaid_png = None
        if mermaid_code:
            mermaid_png = f'slides/temp_mermaid_{module_id}_{slide_idx}.png'
            if not render_mermaid(mermaid_code, mermaid_png):
                mermaid_png = None
        
        output_path = f'slides/slide_{module_id}_{slide_data["slide_id"]}.png'
        create_slide_image(text, image_url, mermaid_png, output_path)
        
        if mermaid_png:
            os.unlink(mermaid_png)
        
        print(f"Generado: {output_path}")

if __name__ == '__main__':
    main()