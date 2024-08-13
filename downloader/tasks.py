from celery import shared_task
from yt_dlp import YoutubeDL
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def download_video_task(video_url, format):
    logger.info(f"Iniciando descarga para la URL: {video_url} con formato: {format}")
    ydl_opts = {}
    if format == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': '%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
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
            'cookiefile': 'cookies.txt',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'referer': 'https://www.youtube.com/'
        }

    try:
        logger.info(f"Opciones de descarga: {ydl_opts}")
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url)
            file_name = ydl.prepare_filename(info_dict)

        file_url = os.path.join(settings.MEDIA_URL, file_name)
        logger.info(f"Descarga completada. Archivo guardado en: {file_url}")
        return {'file_url': file_url}
    
    except Exception as e:
        logger.error(f"Error durante la descarga: {str(e)}")
        return str(e)