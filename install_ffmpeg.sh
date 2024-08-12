#!/bin/bash
# Script para instalar ffmpeg en Render
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz -o ffmpeg.tar.xz
tar xJf ffmpeg.tar.xz
cp ffmpeg-*/ffmpeg /usr/local/bin/
cp ffmpeg-*/ffprobe /usr/local/bin/
