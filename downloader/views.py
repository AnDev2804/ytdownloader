from django.shortcuts import render
from django.http import JsonResponse
import os
from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings  # Importar settings para usar YOUTUBE_API_KEY
import logging
from .tasks import download_video_task

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

def download_video(request, format):
    video_url = request.POST.get('video_url')
    if not video_url:
        return JsonResponse({"error": "No se proporcionó una URL."})

    # Llama a la tarea asíncrona
    task = download_video_task.delay(video_url, format)

    # Devuelve una respuesta que indica que la tarea ha comenzado
    return JsonResponse({"status": "Task started", "task_id": task.id})
