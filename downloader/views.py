import os
import yt_dlp
from django.shortcuts import render
from django.http import JsonResponse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
import logging
from threading import Lock
from urllib.parse import urlparse, parse_qs
import time
import subprocess

logger = logging.getLogger('downloader')
#download_lock = Lock()

def verify_ffmpeg_installation():
    required_files = ['ffmpeg.exe', 'ffprobe.exe']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(os.path.join(settings.FFMPEG_DIR, file)):
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"Archivos faltantes en FFmpeg: {', '.join(missing_files)}")
        return False
    
    try:
        subprocess.run([settings.FFMPEG_PATH, '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run([settings.FFPROBE_PATH, '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        logger.error(f"Error al verificar FFmpeg: {str(e)}")
        return False

if not verify_ffmpeg_installation():
    logger.warning("FFmpeg no está configurado correctamente. Las conversiones a MP3 fallarán.")
    

def get_video_info_from_youtube(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        request = youtube.videos().list(part='snippet', id=video_id)
        response = request.execute()
        
        if not response['items']:
            logger.error(f"No se encontraron resultados para el video ID: {video_id}")
            return None
        
        video_info = response['items'][0]['snippet']
        return {
            'title': video_info['title'],
            'thumbnail_url': video_info['thumbnails']['high']['url'],
            'channel_title': video_info['channelTitle']
        }
    except HttpError as e:
        logger.error(f"Error HTTP {e.resp.status}: {e.content}")
        return None
    
def is_valid_youtube_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc in ["www.youtube.com", "youtube.com", "youtu.be"]

def home(request):
    video_info = error_message = None
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if not video_url:
            error_message = "No se proporcionó una URL."
        elif not is_valid_youtube_url(video_url):
            error_message = "URL de YouTube no válida."
        else:
            video_id = extract_video_id(video_url)
            if not video_id:
                error_message = "URL inválida."
            else:
                video_info = get_video_info_from_youtube(video_id)
                if video_info:
                    video_info['video_url'] = video_url
                else:
                    error_message = "Error al procesar el video."
    
    return render(request, 'index.html', {'video_info': video_info, 'error_message': error_message})

def download_video(request, format):
    video_url = request.POST.get('video_url')
    if not video_url:
        return JsonResponse({"error": "URL no proporcionada"}, status=400)

    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
        'ffmpeg_location': settings.FFMPEG_DIR,  # Usa el directorio en lugar del ejecutable
        'postprocessor_args': ['-ar', '44100'],
        'quiet': False,
    }

    if format == 'mp3':
        ydl_opts.update({
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'extractaudio': True,
            'keepvideo': False,
        })

    try:
        # Verificar existencia de FFmpeg
        if not os.path.exists(settings.FFMPEG_PATH):
            raise Exception(f"FFmpeg no encontrado en {settings.FFMPEG_PATH}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
            if format == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'
                if not os.path.exists(filename):
                    # Intento alternativo de conversión
                    convert_to_mp3(filename.replace('.mp3', '.webm'), filename)
            
            return JsonResponse({
                "status": "SUCCESS",
                "file_url": f"{settings.MEDIA_URL}{os.path.basename(filename)}",
                "filename": os.path.basename(filename)
            })

    except Exception as e:
        logger.error(f"Error en descarga: {str(e)}")
        return JsonResponse({
            "error": "Error en la descarga",
            "details": str(e),
            "solution": "Verifica que FFmpeg esté instalado correctamente"
        }, status=500)

def convert_to_mp3(input_path, output_path):
    """Función alternativa de conversión a MP3"""
    try:
        subprocess.run([
            settings.FFMPEG_PATH,
            '-i', input_path,
            '-codec:a', 'libmp3lame',
            '-q:a', '2',
            output_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error en conversión: {str(e)}")
        return False

def retry_download(video_url, format):
    """Función de reintento con configuración alternativa"""
    try:
        ydl_opts = {
            'format': 'worst',  # Intentar con calidad más baja
            'force_ipv4': True,
            'sleep_interval': 5,
            'max_sleep_interval': 30,
            'ignoreerrors': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            # ... manejo del archivo igual que antes
            
    except Exception as e:
        return JsonResponse({
            "error": "YouTube está bloqueando las descargas. Prueba:",
            "solutions": [
                "1. Esperar 1-2 horas y reintentar",
                "2. Usar una VPN diferente",
                "3. Probar con otro video"
            ]
        }, status=503)

def extract_video_id(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            return parse_qs(parsed_url.query).get('v', [None])[0]
        elif parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        return None
    except Exception as e:
        logger.error(f"Error al analizar URL: {str(e)}")
        return None