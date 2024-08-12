from django.shortcuts import render
from django.http import FileResponse
import os
from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings  # Importar settings para usar YOUTUBE_API_KEY
import logging

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
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
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

logger = logging.getLogger(__name__)

def download_video(request, format):
    video_url = request.POST.get('video_url')
    if not video_url:
        logger.error("No se proporcionó una URL.")
        return render(request, 'index.html', {'error_message': "No se proporcionó una URL."})
    
    ydl_opts = {}
    file_name = None
    
    if format == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': '%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',  # Ruta relativa al archivo de cookies
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'referer': 'https://www.youtube.com/'
        }
    elif format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',  # Ruta relativa al archivo de cookies
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'referer': 'https://www.youtube.com/'
        }

    try:
        logger.info("Iniciando descarga con yt-dlp...")
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url)
            file_name = ydl.prepare_filename(info_dict)
            logger.info(f"Archivo descargado: {file_name}")
        
        with open(file_name, 'rb') as file:
            response = FileResponse(file)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_name)}"'
            logger.info("Archivo listo para enviar.")
        
        os.remove(file_name)  # Elimina el archivo después de servirlo
        return response
    
    except Exception as e:
        error_message = f"Error al descargar el video: {str(e)}"
        logger.error(error_message)
        return render(request, 'index.html', {'error_message': error_message})