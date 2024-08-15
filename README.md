# YouTube Downloader - YTDownloader 🎥🎶

**YTDownloader** es una aplicación web sencilla que te permite descargar videos y audio desde YouTube en formatos MP3 y MP4 de manera rápida y eficiente.

## 🚀 Características Principales

- **Descarga de videos y audio**: Soporta descargas en formato MP4 (video) y MP3 (audio).
- **Interfaz simple**: Introduce la URL del video de YouTube y selecciona el formato de descarga.
- **Procesamiento eficiente**: Usamos `yt-dlp` para descargar y `FFmpeg` para procesar y convertir los archivos.
- **Tareas asíncronas**: Implementación de Celery para gestionar las descargas en segundo plano sin bloquear la interfaz.
- **Almacenamiento y acceso**: Los archivos descargados son almacenados en el servidor y se proporciona un enlace de descarga directo.

## 🛠 Tecnologías Utilizadas

- **Python**: Lenguaje principal para el backend de la aplicación.
- **Django**: Framework web para manejar las vistas, modelos y urls.
- **yt-dlp**: Librería para extraer y descargar videos y audio desde YouTube.
- **Celery**: Manejo de tareas en segundo plano (asíncronas).
- **Redis**: Broker de mensajes para Celery.
- **JavaScript & jQuery**: Interacciones dinámicas en la interfaz.
- **HTML5 & CSS3**: Diseño y estructura de la aplicación web.
- **FFmpeg**: Herramienta utilizada para convertir videos y audio entre diferentes formatos.

## 📋 Instrucciones de Instalación

1. **Clona el repositorio**:
    ```
    git clone https://github.com/AnDev2804/ytdownloader.git
    ```

2. **Configura las dependencias**:
    ```
    pip install -r requirements.txt
    ```

3. **Configura el broker de Celery**:
    - Asegúrate de tener Redis configurado correctamente. Establece el URL en `settings.py`:
    ```
    CELERY_BROKER_URL = 'redis://tu-redis-url'
    ```

4. **Ejecuta el servidor de desarrollo**:
    ```
    python manage.py runserver
    ```

5. **Inicia el worker de Celery**:
    ```
    celery -A ytdownloader worker --loglevel=info
    ```

6. **Descargar y configurar FFmpeg**:
    - Descarga e instala FFmpeg en tu sistema, luego establece la ruta en tu entorno de desarrollo.

## 🖥 Uso de la Aplicación

1. Ingresa la URL del video de YouTube que deseas descargar.
2. Selecciona el formato deseado: MP4 o MP3.
3. Haz clic en el botón de descarga, y la aplicación se encargará del resto.

## 🚧 Estado del Proyecto

Este proyecto está en constante mejora. Se seguirán añadiendo características y mejoras para una experiencia más fluida y eficiente.

¡Contribuciones y sugerencias son bienvenidas!

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
