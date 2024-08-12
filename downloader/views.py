from django.shortcuts import render
from django.http import FileResponse
import os
from yt_dlp import YoutubeDL

def home(request):
    video_info = None
    error_message = None
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        try:
            ydl_opts = {
                'cookiefile': 'cookies.txt',  # Ruta relativa al archivo de cookies
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'referer': 'https://www.youtube.com/'
            }
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                video_info = {
                    'title': info_dict.get('title', None),
                    'thumbnail_url': info_dict.get('thumbnail', None),
                    'channel_title': info_dict.get('uploader', None),
                    'video_url': video_url
                }
        except Exception as e:
            error_message = f"Error al procesar el video: {str(e)}"
            print(error_message)
    
    return render(request, 'index.html', {'video_info': video_info, 'error_message': error_message})

def download_video(request, format):
    video_url = request.POST.get('video_url')
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
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url)
            file_name = ydl.prepare_filename(info_dict)
        
        with open(file_name, 'rb') as file:
            response = FileResponse(file)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_name)}"'
        
        os.remove(file_name)  # Elimina el archivo después de servirlo
        return response
    
    except Exception as e:
        error_message = f"Error al descargar el video: {str(e)}"
        return render(request, 'index.html', {'error_message': error_message})