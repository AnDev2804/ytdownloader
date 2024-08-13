from celery import shared_task
from yt_dlp import YoutubeDL
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@shared_task
def download_video_task(video_url, format):
    ydl_opts = {}
    file_name = None

    if format == 'mp4':
        ydl_opts = {
            'format': 'worstvideo',  # Cambia a una calidad más baja
            'outtmpl': '%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',  
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'referer': 'https://www.youtube.com/'
        }
    elif format == 'mp3':
        ydl_opts = {
            'format': 'worstaudio',  # Cambia a una calidad más baja
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',  
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'referer': 'https://www.youtube.com/'
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url)
            file_name = ydl.prepare_filename(info_dict)
            
            # Guarda el archivo en el almacenamiento temporal o en un almacenamiento permanente
            with open(file_name, 'rb') as file:
                content = ContentFile(file.read())
                saved_path = default_storage.save(file_name, content)
            
            os.remove(file_name)  # Elimina el archivo después de guardarlo

        return saved_path
    except Exception as e:
        raise e
