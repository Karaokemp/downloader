import os
import sys
import unicodedata
import re
import youtube_dl
from slugify import slugify
import uuid

VIDEOS_FOLDER = 'super-mega-wonder-songs'
LINKS_FILE = 'links.txt'
PROCESSED_FILE = 'finished.txt'
TITLE_PREFIX = 'TITLE: '


def download(url):
    tempFile = VIDEOS_FOLDER + '/' +'video' + '.mp4'
    ydl_opts = {
    'outtmpl': tempFile
}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            songInfo = ydl.extract_info(url, download=True)
            title = slugify(songInfo['title'])
            newFileName = VIDEOS_FOLDER + '/' + title + '.mp4'
            os.replace(tempFile, newFileName)

            msg = title + " was downloaded!"
            print(msg)
            return title

def getLinks():
    links = open(LINKS_FILE,'r').readlines()
    return links


with open(LINKS_FILE, "r") as linksFile, open(PROCESSED_FILE,'w') as processedFile:
    for link in linksFile:
        if link.startswith(TITLE_PREFIX):
            continue
        link = link.strip()
        title = download(link)
        processedMessage = link  + '\n' + TITLE_PREFIX+ title + ' was downloaded!' + '\n'
        processedFile.write(processedMessage)
linksFile.close()
processedFile.close()
os.replace(PROCESSED_FILE,LINKS_FILE)