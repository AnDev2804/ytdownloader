from django.shortcuts import render
from django.http import JsonResponse
import os
from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings  # Importar settings para usar YOUTUBE_API_KEY
import logging
from threading import Lock

# Configurar logger
logger = logging.getLogger('downloader')

# Crear un lock para evitar descargas concurrentes
download_lock = Lock()

def get_video_info_from_youtube(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)  # Usar API Key desde settings
        request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()
        video_info = response['items'][0]['snippet']
        return {
            'title': video_info['title'],
            'thumbnail_url': video_info['thumbnails']['high']['url'],
            'channel_title': video_info['channelTitle']
        }
    except HttpError as e:
        logger.error(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None

def home(request):
    video_info = None
    error_message = None
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if not video_url:
            error_message = "No se proporcionó una URL."
        else:
            video_id = video_url.split('v=')[-1]
            if not video_id:
                error_message = "URL inválida."
            else:
                video_info = get_video_info_from_youtube(video_id)
                if video_info is None:
                    error_message = "Error al procesar el video."
                else:
                    video_info['video_url'] = video_url  # Añade la URL del video al contexto
    
    return render(request, 'index.html', {'video_info': video_info, 'error_message': error_message})

def download_video(request, format):
    with download_lock:
        video_url = request.POST.get('video_url')
        
        if not video_url:
            return JsonResponse({"error": "No se proporcionó una URL."})

        ydl_opts = {}

        if format == 'mp4':
            ydl_opts = {
                'format': 'best[height<=480]',  # Limita la calidad a 480p o menos
                'outtmpl': '%(title)s.%(ext)s',
                'cookiefile': 'cookies.txt',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'referer': 'https://www.youtube.com/',
                'n_threads': 1,  # Usa solo un hilo
                'logger': logger,
                'progress_hooks': [lambda d: logger.debug(f"Progreso de la descarga: {d}")],
                'download_timeout': 300  # Límite de tiempo de descarga de 5 minutos
            }
        elif format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'cookiefile': 'cookies.txt',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '64',
                }],
                'outtmpl': '%(title)s.%(ext)s',
                'n_threads': 1,
                'logger': logger,
                'progress_hooks': [lambda d: logger.debug(f"Progreso de la descarga: {d}")],
                'download_timeout': 300,
            }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                logger.debug(f"Iniciando descarga del video: {video_url}")
                info_dict = ydl.extract_info(video_url, download=True)
                file_name = ydl.prepare_filename(info_dict)
                logger.debug(f"Video descargado con éxito: {file_name}")
            
            file_url = f"/media/{os.path.basename(file_name)}"
            return JsonResponse({"status": "SUCCESS", "file_url": file_url})

        except Exception as e:
            logger.error(f"Error al descargar el video: {str(e)}")
            return JsonResponse({"status": "FAILURE", "error": str(e)})

