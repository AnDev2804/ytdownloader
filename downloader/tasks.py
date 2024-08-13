import logging
from celery import shared_task
from yt_dlp import YoutubeDL
import os

logger = logging.getLogger('downloader')  # Obtén el logger configurado para tu aplicación

@shared_task
def download_video_task(video_url, format):
    ydl_opts = {}
    progress = {}

    def my_hook(d):
        if d['status'] == 'downloading':
            progress['progress'] = d['_percent_str']
            progress['speed'] = d['_speed_str']
        elif d['status'] == 'finished':
            progress['filename'] = d['filename']

    if format == 'mp4':
        ydl_opts = {
            'format': 'worstvideo+worstaudio',
            'outtmpl': '%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'referer': 'https://www.youtube.com/',
            'progress_hooks': [my_hook],
        }
    elif format == 'mp3':
        ydl_opts = {
            'format': 'worstaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '64',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'referer': 'https://www.youtube.com/',
            'progress_hooks': [my_hook],
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url)
            file_name = ydl.prepare_filename(info_dict)
            file_url = f"/media/{os.path.basename(file_name)}"
            progress['file_url'] = file_url
            return progress  # Retorna el progreso y la URL del archivo

    except Exception as e:
        return str(e)