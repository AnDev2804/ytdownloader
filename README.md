# YouTube Downloader - YTDownloader 🎥🎶

**YTDownloader** is a simple web application that allows you to download videos and audio from YouTube in MP3 and MP4 formats quickly and efficiently.

## 🚀 Main Features.

- **Video and audio download**: Supports MP4 (video) and MP3 (audio) format downloads.
- **Simple interface**: Input YouTube video URL and select download format.
- Efficient processing**: We use `yt-dlp` to download and `FFmpeg` to process and convert the files.
- Asynchronous tasks**: Celery implementation to manage background downloads without blocking the interface.
- **Storage and access**: Downloaded files are stored on the server and a direct download link is provided.

## 🛠 Technologies Used.

- Python**: Main language for the backend of the application.
- **Django**: Web framework to handle views, models and urls.
- **yt-dlp**: Library to extract and download videos and audio from YouTube.
- Celery**: Background task management (asynchronous).
- Redis**: Message broker for Celery.
- JavaScript & jQuery**: Dynamic interactions in the interface.
- HTML5 & CSS3**: Web application design and structure.
- **FFmpeg**: Tool used to convert videos and audio between different formats.

## 📋 Installation Instructions.

1. **Clone repository**:
    ```
    git clone https://github.com/AnDev2804/ytdownloader.git
    ```

2. **Set up the dependencies**:
    ```
    pip install -r requirements.txt
    ```

3. **Configure the Celery broker**:
    - Make sure you have Redis configured correctly. Set the URL in `settings.py`:
    ```
    CELERY_BROKER_URL = 'redis://your-redis-url'
    ```

4. **Run the development server**:
    ```
    python manage.py runserver
    ```

5. **Start the Celery worker**:
    ```
    celery -A ytdownloader worker --loglevel=info
    ```

6. **Download and configure FFmpeg**:
    - Download and install FFmpeg on your system, then set the path in your development environment.

## 🖥 Using the Application

1. Enter the URL of the YouTube video you want to download.
2. Select the desired format: MP4 or MP3.
3. Click the download button, and the application will take care of the rest.

## 🚧 Project status

This project is constantly being improved. Features and improvements will continue to be added for a smoother and more efficient experience.

Contributions and suggestions are welcome!

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.