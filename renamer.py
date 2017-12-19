# coding=utf-8
import os
import re
import codecs
import urllib.request
import unicodedata
import imdb


def folders():
    DIRECTORY = 1
    return next(os.walk(os.curdir))[DIRECTORY]

def clean_name(path):
    remove_keys = ["BDRip", "SiMPLE", "BRRip", "HD-TS", "HC", "HEVC", "WEBRip", "HDDVD", "VPPV", "HQ", "DTS", "Hive-CM8", "mp4", "mp3", "NEW SOURCE", "Extended", "REMASTERED", "LIMITED", "XviD", "H264", "x265", "AC3", "DVDSCR", "720P", "1080P", "HDRip", "DVDRip", "x264", "AAC", "6CH", "BluRay", "-ETRG", "WEB-DL", "WEBDL", "DD5", "-EVO", "-AMIABLE", "-JYK", "-iNFAMOUS", "-ALLiANCE", "-HANDJOB", "-FUM", "-EXTREME", "-FGT", "-POOP", "-PSA", "Feel-Free", "-Ozlem", "- EVO", "- AMIABLE", "- JYK", "- iNFAMOUS", "- ALLiANCE", "- HANDJOB", "- FUM", "- EXTREME", "- FGT", "- POOP", "- PSA", "-Feel-Free", "- Ozlem", "- ETRG", "-PTpOWeR", "- PTpOWeR", "-CODY", "- CODY", "-.Hon3y", "- .Hon3y", "-XvAvX", "- XvAvX", "-RARBG", "- RARBG", "-CM8", "- CM8", "-aNaRCHo", "- aNaRCHo", "TommieCook", "-VLiS", "- VLiS", "_sujaidr", "anoXmous", "FRENCH", "JAPANESE", "-SPARKS", "- SPARKS", "-MAXSPEED", "- MAXSPEED", "-Exclusive", "- Exclusive", "- WeTv", "-WeTv", "-aXXo", "- aXXo", "Ganool", "- iExTV", "-iExTV", "NVEE", "-MAJESTiC", "- MAJESTiC", "Netflix", "-Garmin", "- Garmin", "Final Cut", "-T0XiC-iNK", "Ultimate Edition", "Final Cut", "-ArtSubs", "- ArtSubs", "-NoGrp", "- NoGrp"]
    for key in remove_keys:
        path = re.sub(re.escape(key), '', path, flags=re.IGNORECASE)

    return path

def get_year(path):
    path = clean_name(path)

    try:
        year = int(re.findall("[12][0129][0-9]{2}", path)[-1])
        if year > 1930 and year < 2020:
            return year
        else:
            return None
    except Exception as e:
        return None

def get_name(path):
    path = clean_name(path)
    year = get_year(path)

    path = path.replace(".", " ")
    path = path.replace("[]", "")
    path = re.sub('\[[^\]]+\]', '', path)
    path = re.sub("%s" % year, '', path)
    path = re.sub('\(\)', '', path)
    path = re.sub('\ \ ', ' ', path)
    path = re.sub('\ \ ', ' ', path)
    path = re.sub('\ \ ', ' ', path)

    return path

def search_movie_name(name):
    ia = imdb.IMDb()

    return ia.search_movie(name)


def fetch_movie(name, year=None):
    results = search_movie_name(name)

    if year is not None:
        for result in results:
            if "year" in result.data and int(result.data["year"]) == int(year):
                return result.data["title"], result.data["year"]

    if results and len(results):
        return results[0].data["title"], results[0].data["year"]

    return None, None

def strip_after(string, character):
    position = string.rfind(character)
    if position > 0:
        string = string[:position]

    return string

def compare_titles(local, fetched):
    local = strip_after(local, '-')
    local = strip_after(local, ':')
    fetched = strip_after(fetched, '-')
    fetched = strip_after(fetched, ':')
    ignore = '[-.,()\'" ]+'
    local = re.sub(ignore, '', local).lower()
    fetched = re.sub(ignore, '', fetched).lower()

    return local == fetched

def user_decision(name, title):
    letter = None
    while not (letter == 'n' or letter == 'y'):
        letter = input("Rename %s to %s ? (y/n) " % (name, title))

    return letter == 'y'

def rename(path_from, path_to):
    absolute_from = os.path.join(os.getcwd(), path_from)
    absolute_to = os.path.join(os.getcwd(), path_to)

    try:
        os.rename(absolute_from, absolute_to)
        return True
    except:
        return False

def print_line(folder, year, title, rename_to, action):
    def format(string, length=30):
        if len(string) > length:
            return string[:length-3] + '...'
        else:
            return string.ljust(length)

    print(format(folder), year, format(title), format(rename_to), action, flush=True)


def renamed_already(path):
    if re.match("[A-Za-z0-9\'\-\:\, ]+\([0-9]{4}\)$", path):
        return True

    return False

def rename_folder(folder):
    if renamed_already(folder):
        return True

    name = get_name(folder)
    year_title = get_year(folder)

    title, year = fetch_movie(name, year=year_title)

    rename_to = ''
    action = 'Error'
    if title and year:
        rename_to = "%s (%s)" % (title, year)
        if folder == rename_to:
            action = 'Equal'
        elif compare_titles(name, title):
            if rename(folder, rename_to):
                action = 'Renamed'
            else:
                action = 'Error'
        elif user_decision(name, title):
            if rename(folder, rename_to):
                action = 'Renamed'
            else:
                action = 'Error'
        else:
            action = 'Discarded'
    else:
        title = ''
        year = ''
        action = 'Not found'

    print_line(folder, year, title, rename_to, action)
