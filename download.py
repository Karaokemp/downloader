import os
import sys
import unicodedata
import re
import youtube_dl
from slugify import slugify
import uuid

VIDEOS_FOLDER = 'videos'
UNNAMED_FOLDER = 'to-rename'

LINKS_FILE = 'links.txt'
PROCESSED_FILE = 'finished.txt'
TITLE_PREFIX = '#'


def download(url):
    tempFile = VIDEOS_FOLDER + '/' +'video' + '.mp4'
    ydl_opts = {
    'outtmpl': tempFile
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            songInfo = ydl.extract_info(url, download=True)
        except:
            songInfo = {'title':'UNDEFINED'}
            print('could not process link: ' + url)
        title = songInfo['title']
        title = title.replace("!@#$%^&*()[]{};:,./<>?\/|`~-=_+", " ")
        newFileName = VIDEOS_FOLDER + '/' + title + '.mp4'
        try:
            os.replace(tempFile, newFileName)
        except:
                unnamedPath = VIDEOS_FOLDER + '/' + UNNAMED_FOLDER
                newFileName = unnamedPath + '/' + 'SONG-' + str(uuid.uuid4()) + '.mp4'
                if not os.path.exists(unnamedPath):
                    os.makedirs(unnamedPath)
                os.replace(tempFile, newFileName)
        msg = title + " was downloaded!"
        print(msg)
        return title

with open(LINKS_FILE,'r',encoding="utf8") as linksFile, open(PROCESSED_FILE,'w',encoding="utf8") as processedFile:
    for link in linksFile:
        if link.startswith(TITLE_PREFIX):
            continue
        link = link.strip()
        title = download(link)
        processedMessage = link  + '\n' + TITLE_PREFIX + 'song was downloaded!' + '\n'
        processedFile.write(processedMessage)
linksFile.close()
processedFile.close()
os.replace(PROCESSED_FILE,LINKS_FILE)