from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el entorno predeterminado para las configuraciones de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ytdownloader.settings')

app = Celery('ytdownloader')

# Carga las configuraciones desde el settings.py usando una cadena
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre y carga automáticamente las tareas de todos los módulos instalados de Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
