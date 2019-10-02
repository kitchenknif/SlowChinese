#!/bin/sh
wayback_machine_downloader http://slow-chinese.com/images -c10 --only "/\.(gif|jpg|jpeg)$/i"
wayback_machine_downloader http://slow-chinese.com/podcasts -c10 --only "/\.(mp3|mp3\?_=1)$/i"
wayback_machine_downloader http://slow-chinese.com/podcast -c10
