web: ./install_ffmpeg.sh && gunicorn ytdownloader.wsgi --timeout 600
worker: celery -A ytdownloader worker --loglevel=info