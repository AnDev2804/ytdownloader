from celery import shared_task
from yt_dlp import YoutubeDL
import os

@shared_task
def download_video_task(video_url, format):
    print(f"Iniciando descarga para {video_url} en formato {format}")
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
        with YoutubeDL(ydl_opts) as ydl:
            print("Descargando el video...")
            info_dict = ydl.extract_info(video_url)
            file_name = ydl.prepare_filename(info_dict)
            print(f"Video descargado: {file_name}")

        file_url = f"/media/{os.path.basename(file_name)}"
        print(f"Archivo disponible en: {file_url}")
        return {'file_url': file_url}
    
    except Exception as e:
        print(f"Error durante la descarga: {str(e)}")
        return str(e)
