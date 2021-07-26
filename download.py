import os
import sys
import unicodedata
import re
import youtube_dl

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
            title = songInfo['title']
            newFileName = VIDEOS_FOLDER + '/' +slugify(title) + '.mp4'

            os.replace(tempFile, newFileName)

            msg = title + " was downloaded!"
            print(msg)
            return title

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
