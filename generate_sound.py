import yaml
import os
import sys
import glob
import requests
import json
import subprocess

def generate_audio(text, output_path, voice="bm_daniel", lang="es"):
    """Genera audio usando Kokoro."""
    response = requests.post(
        "http://localhost:8880/dev/captioned_speech",
        json={
            "input": text,
            "voice": voice,
            "response_format": "wav",
            "speed": 1.0,
            "lang_code": lang
        }
    )
    with open(output_path, "wb") as f:
        f.write(response.content)

def create_silence(duration, output_path):
    """Crea un archivo de silencio usando ffmpeg."""
    subprocess.run([
        "ffmpeg", "-f", "lavfi", "-i", f"anullsrc=r=22050:cl=mono",
        "-t", str(duration), "-q:a", "9", output_path
    ], check=True)

def merge_audios(audio_files, output_path):
    """Une los audios con ffmpeg."""
    with open("temp_list.txt", "w") as f:
        for audio in audio_files:
            f.write(f"file '{audio}'\n")
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", "temp_list.txt",
        "-c", "copy", output_path
    ], check=True)
    os.remove("temp_list.txt")

def main():
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
    
    # Check for command-line arguments
    if len(sys.argv) == 3:
        try:
            target_module = int(sys.argv[1])
            target_slide = int(sys.argv[2])
            slides = [s for s in slides if s['module_id'] == target_module and s['slide_id'] == target_slide]
            if not slides:
                print(f"Slide {target_module}_{target_slide} no encontrado.")
                return
        except ValueError:
            print("Argumentos inválidos. Usa: python generate_sound.py [module_id] [slide_id]")
            return
    
    print("Generando sonidos...")
    
    os.makedirs('slide_sounds', exist_ok=True)
    
    for slide_data in slides:
        module_id = slide_data['module_id']
        slide_id = slide_data['slide_id']
        script = slide_data.get('script', [])
        if not script:
            print(f"No script for slide {module_id}_{slide_id}")
            continue
        
        audio_files = []
        for i, sentence in enumerate(script):
            audio_path = f'slide_sounds/sound_{module_id}_{slide_id}.{i+1:03d}.wav'
            generate_audio(sentence, audio_path)
            audio_files.append(audio_path)
            if i < len(script) - 1:  # Add silence between sentences
                silence_path = f'slide_sounds/silence_{module_id}_{slide_id}.{i+1}.wav'
                create_silence(1.0, silence_path)  # 1 second silence
                audio_files.append(silence_path)
        
        final_audio = f'slide_sounds/sound_{module_id}_{slide_id}.wav'
        merge_audios(audio_files, final_audio)
        
        # Clean up intermediate files
        for f in audio_files:
            if os.path.exists(f):
                os.remove(f)
        
        print(f"Generado: {final_audio}")

if __name__ == '__main__':
    main()