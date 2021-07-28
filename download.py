import os
import sys
import unicodedata
import re
import youtube_dl
from slugify import slugify
import uuid
import urllib.parse as urlparse
from urllib.parse import parse_qs

VIDEOS_FOLDER = 'videos'
UNNAMED_FOLDER = 'to-rename'
LINKS_FILE = 'links.txt'
PROCESSED_FILE = 'finished.txt'
UNHANDLED_FILE = 'unhandled.txt'


def download(url):
    parsed = urlparse.urlparse(url)
    videoId = parse_qs(parsed.query)['v'][0]
    tempFile = VIDEOS_FOLDER + '/' + videoId+ '.mp4'
    ydl_opts = {
    'outtmpl': tempFile,
    'nopart': True
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

def wait_for_file(source_dir, filename, timeout=10):
        """Wait for the creation of the specific file.

        This method checks if the specified file exists and waits for it to
        appear during the specified amount of time (by default 10 seconds).

        source_dir[in]  Source directory where the file is located.
        filename[in]    Name of the file to wait for.
        timeout[in]     Time to wait in seconds (by default 10 seconds).
        """
        file_path = os.path.normpath(os.path.join(source_dir, filename))
        attempts = 0
        while attempts < timeout:
            # Check if the file exists.
            if os.path.isfile(file_path):
                return
            # Wait 1 second before trying again.
            time.sleep(1)
            attempts += 1 
with open(LINKS_FILE,'r',encoding="utf8") as linksFile:
    for link in linksFile:
        link = link.strip()
        line = link  + '\n'
        try:
            title = download(link)
            with open(PROCESSED_FILE,'a',encoding="utf8") as processedFile:
                processedFile.write(line)
            processedFile.close()
            print(title + 'was downloaded !')
        except Exception as e:
            print(str(e))
            with open(UNHANDLED_FILE,'a',encoding="utf8") as errorsFile:
                errorsFile.write(line)
            errorsFile.close()
linksFile.close()
print('finished successfully !')