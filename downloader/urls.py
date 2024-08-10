from django.urls import path
from .views import home, download_video

urlpatterns = [
    path('', home, name='home'),
    path('download/<str:format>/', download_video, name='download_video'),
]
