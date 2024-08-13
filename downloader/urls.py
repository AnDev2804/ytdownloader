from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download/<str:format>/', views.download_video, name='download_video'),
    path('task-status/<str:task_id>/', views.task_status, name='task_status'),
]
