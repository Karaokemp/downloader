import os
import sys
import unicodedata
import re
import youtube_dl
import pandas as pd

VIDEOS_FOLDER = 'super-mega-wonder-songs'
LINKS_FILE = 'links.txt'


def download(url):
    tempFile = VIDEOS_FOLDER + '/' +'video' + '.mp4'
    ydl_opts = {
    'outtmpl': tempFile
}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            songInfo = ydl.extract_info(url, download=True)
            title = songInfo['title']
            newFileName = VIDEOS_FOLDER + '/' +slugify(title) + '.mp4'

            os.rename(tempFile, newFileName)
            #os.remove(tempFile)

            msg = title + " was downloaded!"
            print(msg)

def getLinks():
    links = open(LINKS_FILE,'r').readlines()
    return links

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

links = getLinks()
for link in links:
    download(link)