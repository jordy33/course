import os
import subprocess
import glob
import yaml
import sys
import json

def get_audio_duration(audio_path):
    """Obtiene la duración del audio en segundos usando ffprobe."""
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', audio_path
        ], capture_output=True, text=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except Exception as e:
        print(f"Error obteniendo duración de {audio_path}: {e}")
        return 5.0  # Duración por defecto si falla

def create_slide_video(slide_path, duration, output_path, fade_duration=1.0):
    """Crea un video de un slide con fade out al final."""
    if fade_duration > 0:
        vf = f'fade=out:{int((duration - fade_duration) * 25)}:{int(fade_duration * 25)}'
    else:
        vf = None
    cmd = ['ffmpeg', '-y', '-loop', '1', '-i', slide_path, '-c:v', 'libx264', '-t', str(duration), '-pix_fmt', 'yuv420p']
    if vf:
        cmd.extend(['-vf', vf])
    cmd.append(output_path)
    subprocess.run(cmd, check=True)

def create_pause_video(duration, output_path, width=1920, height=1080):
    """Crea un video de pausa negra."""
    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi', '-i', f'color=black:s={width}x{height}:d={duration}',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_path
    ], check=True)

def merge_videos(video_files, output_path):
    """Une videos usando concat."""
    with open('temp_video_list.txt', 'w') as f:
        for video in video_files:
            f.write(f"file '{video}'\n")
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'temp_video_list.txt',
        '-c', 'copy', output_path
    ], check=True)
    os.remove('temp_video_list.txt')

def merge_audios(audio_files, output_path):
    """Une audios."""
    with open('temp_audio_list.txt', 'w') as f:
        for audio in audio_files:
            f.write(f"file '{audio}'\n")
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'temp_audio_list.txt',
        '-c', 'copy', output_path
    ], check=True)
    os.remove('temp_audio_list.txt')

def create_silence_audio(duration, output_path):
    """Crea un archivo de audio silencio."""
    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=24000:cl=mono',
        '-t', str(duration), '-q:a', '9', output_path
    ], check=True)

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

    # Filtrar por argumentos opcionales (módulo y slide específicos)
    if len(sys.argv) == 3:
        try:
            target_module = int(sys.argv[1])
            target_slide = int(sys.argv[2])
            slides = [s for s in slides if s['module_id'] == target_module and s['slide_id'] == target_slide]
            if not slides:
                print(f"Slide {target_module}_{target_slide} no encontrado.")
                return
        except ValueError:
            print("Argumentos inválidos. Usa: python generate_video.py [module_id] [slide_id]")
            return

    print("Generando video con transiciones y pausas...")

    os.makedirs('videos', exist_ok=True)

    video_files = []
    audio_files = []
    total_duration = 0

    # Pausa al inicio: mostrar primer slide por 3 segundos sin audio
    if slides:
        first_slide_path = f'slides/slide_{slides[0]["module_id"]}_{slides[0]["slide_id"]}.png'
        if os.path.exists(first_slide_path):
            intro_video = 'videos/intro.mp4'
            create_slide_video(first_slide_path, 3.0, intro_video, fade_duration=0)  # Sin fade
            video_files.append(intro_video)
            intro_audio = 'videos/intro_silence.wav'
            create_silence_audio(3.0, intro_audio)
            audio_files.append(intro_audio)
            total_duration += 3.0

    for slide_data in slides:
        module_id = slide_data['module_id']
        slide_id = slide_data['slide_id']
        slide_path = f'slides/slide_{module_id}_{slide_id}.png'
        audio_path = f'slide_sounds/sound_{module_id}_{slide_id}.wav'

        if not os.path.exists(slide_path):
            print(f"Slide {slide_path} no encontrado, saltando.")
            continue
        if not os.path.exists(audio_path):
            print(f"Audio {audio_path} no encontrado, usando duración por defecto.")
            duration = 5.0
        else:
            duration = get_audio_duration(audio_path)
            audio_files.append(audio_path)

        # Crear video del slide con fade out
        slide_video = f'videos/slide_{module_id}_{slide_id}.mp4'
        create_slide_video(slide_path, duration, slide_video)
        video_files.append(slide_video)

        # Agregar pausa negra de 2 segundos después del slide
        pause_video = f'videos/pause_{module_id}_{slide_id}.mp4'
        create_pause_video(2.0, pause_video)
        video_files.append(pause_video)

        # Agregar silencio para la pausa
        silence_audio = f'videos/silence_{module_id}_{slide_id}.wav'
        create_silence_audio(2.0, silence_audio)
        audio_files.append(silence_audio)

        total_duration += duration + 2.0

    # Unir todos los videos (intro + slides + pausas)
    combined_video = 'videos/combined_slides.mp4'
    merge_videos(video_files, combined_video)

    # Unir audios (intro silence + slide audios + pause silences)
    combined_audio = 'videos/combined_audio.wav'
    merge_audios(audio_files, combined_audio)

    # Combinar video y audio en MP4 final
    final_video = 'videos/final_presentation.mp4'
    subprocess.run([
        'ffmpeg', '-y', '-i', combined_video, '-i', combined_audio,
        '-c:v', 'copy', '-c:a', 'aac', final_video
    ], check=True)

    print(f"Video final generado: {final_video} (duración aproximada: {total_duration} segundos)")

    # Limpiar archivos temporales (no borrar audios originales sound_x_y.wav)
    temp_files = video_files + [f for f in audio_files if 'silence' in f or 'intro' in f]
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists(combined_video):
        os.remove(combined_video)
    if os.path.exists(combined_audio):
        os.remove(combined_audio)

if __name__ == '__main__':
    main()