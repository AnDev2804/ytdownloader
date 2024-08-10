from django.shortcuts import render
from pytube import YouTube
from django.http import FileResponse, HttpResponse
import os

def home(request):
    video_info = None
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        yt = YouTube(video_url)
        video_info = {
            'title': yt.title,
            'thumbnail_url': yt.thumbnail_url,
            'channel_title': yt.author,
            'video_url': video_url
        }
    
    return render(request, 'index.html', {'video_info': video_info})

def download_video(request, format):
    video_url = request.POST.get('video_url')
    yt = YouTube(video_url)
    
    if format == 'mp4':
        stream = yt.streams.get_highest_resolution()
    elif format == 'mp3':
        stream = yt.streams.filter(only_audio=True).first()
    
    output_path = stream.download()
    file_name = yt.title if format == 'mp4' else yt.title + '.mp3'
    
    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    os.remove(output_path)  # Elimina el archivo después de servirlo
    return response
