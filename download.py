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
UNHANDLED_FILE = 'unhandled.txt'

def download(url):
    tempFile = VIDEOS_FOLDER + '/' +'video' + '.mp4'
    ydl_opts = {
    'outtmpl': tempFile
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            songInfo = ydl.extract_info(url, download=True)
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
            return title

with open(LINKS_FILE,'r',encoding="utf8") as linksFile, open(PROCESSED_FILE,'w',encoding="utf8") as processedFile, open(UNHANDLED_FILE,'w',encoding="utf8") as errorsFile:
    for link in linksFile:
        link = link.strip()
        line = link  + '\n'
        try:
            title = download(link)
            processedFile.write(line)
            print(title + 'was downloaded !')
        except:
            errorsFile.write(line)
            print('Error on link: ' + link)
linksFile.close()
processedFile.close()
errorsFile.close()
print('finished successfully !')