import os
import sys

# Añadir la ruta de tu proyecto
project_path = '/home/AnDev2804/ytdownloader'
if project_path not in sys.path:
    sys.path.append(project_path)

# Establecer las variables de entorno
os.environ['DJANGO_SETTINGS_MODULE'] = 'ytdownloader.settings'

# Importar y configurar Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()