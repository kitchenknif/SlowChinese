#!/bin/sh
wayback_machine_downloader http://slow-chinese.com/images -c10 --only "/\.(gif|jpg|jpeg)$/i"
#wayback_machine_downloader http://slow-chinese.com/podcasts -c10 --only "/\.(mp3|mp3\?_=1)$/i"
wayback_machine_downloader http://slow-chinese.com/podcast -c10

mkdir ./websites/
mkdir ./websites/slow-chinese.com/
mkdir ./websites/slow-chinese.com/podcasts
cd ./websites/slow-chinese.com/podcasts
wget https://archive.org/compress/slowchinese_201909/formats=VBR%20MP3\&file=/slowchinese_201909.zip
unzip slowchinese_201909.zip
rm slowchinese_201909.zip