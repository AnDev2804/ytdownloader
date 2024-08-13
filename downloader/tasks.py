from celery import shared_task
from yt_dlp import YoutubeDL
import os
import logging

logger = logging.getLogger('downloader')

@shared_task(bind=True)
def download_video_task(self, video_url, format):
    ydl_opts = {}
    
    logger.debug(f"Iniciando la descarga del video: {video_url} en formato {format}")
    
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
        logger.debug(f"Opciones de descarga configuradas: {ydl_opts}")
        
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            logger.debug(f"Información del video obtenida: {info_dict}")
            
            file_name = ydl.prepare_filename(info_dict)
            logger.debug(f"Nombre del archivo preparado: {file_name}")
            
            ydl.download([video_url])
            logger.debug(f"Descarga completada para: {video_url}")

        file_url = os.path.join('/media/', file_name)
        logger.debug(f"Archivo guardado en: {file_url}")
        return {'file_url': file_url}
    
    except Exception as e:
        logger.error(f"Error durante la descarga: {str(e)}")
        return {'error': str(e)}
