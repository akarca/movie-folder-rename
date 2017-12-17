#!/usr/bin/python3

import os
import re
import codecs
import urllib.request
import unicodedata


def folders():
    DIRECTORY = 1
    return next(os.walk(os.curdir))[DIRECTORY]

def has_year(path):
    left = re.compile('^[1-2][0-9]{3}')
    right = re.compile('[1-2][0-9]{3}$')
    path = re.sub('[()]', '', path)
    path = path.strip()
    return left.match(path) or right.match(path)

def get_name(path):
    remove_keys = ["BDRip", "XviD", "AC3", "DVDSCR", "720P", "1080P", "HDRip", "DVDRip", "x264", "AAC", "6CH", "BluRay", "-ETRG", "WEB-DL", "WEBDL", "DD5", "-EVO", "-AMIABLE", "-JYK", "-iNFAMOUS", "-ALLiANCE", "-HANDJOB", "-FUM", "-EXTREME", "-FGT", "-POOP", "-PSA", "Feel-Free", "-Ozlem", "- EVO", "- AMIABLE", "- JYK", "- iNFAMOUS", "- ALLiANCE", "- HANDJOB", "- FUM", "- EXTREME", "- FGT", "- POOP", "- PSA", "-Feel-Free", "- Ozlem", "- ETRG", "-PTpOWeR", "- PTpOWeR", "-CODY", "- CODY", "-.Hon3y", "- .Hon3y", "-XvAvX", "- XvAvX", "-RARBG", "- RARBG", "-CM8", "- CM8", "-aNaRCHo", "- aNaRCHo"]
    for key in remove_keys:
        path = path.replace(key, "")

    path = path.replace(".", " ")
    path = re.sub('\[[^\]]+\]', '', path)
    path = re.sub('^[12][0-9]{3}', '', path)
    path = path.rstrip(') ')
    path = re.sub('[12][0-9]{3}$', '', path)
    path = path.strip('() ')
    return path

def imdb_url(path):
    url = 'http://www.imdb.com/find?q=' + '+'.join(path.split(' '))
    url = unicodedata.normalize('NFKD', url).encode('ascii', errors='ignore').decode('ascii')
    return url

def crawl_imdb(url):
    request = urllib.request.Request(url, None, {'Accept-Language': 'en-US,en;q=0.8,de;q=0.6'})
    response = urllib.request.urlopen(request)
    content = response.read()
    text = content.decode('utf-8-sig', errors='ignore')
    return text

def parse_title(html):
    matches = re.search('"result_text">[^>]+>(?P<title>[^<]*)', html)
    if not matches:
        return None
    title = matches.group('title')
    title = title.strip()
    if len(title) > 3 and re.match('[0-9A-Za-z-,!?]+', title):
        return title
    return None

def parse_year(html):
    matches = re.search('"result_text">[^>]+>[^>]+> (?P<text>[^<]+) <', html)
    if not matches:
        return None
    text = matches.group('text')
    matches = re.search('(?P<year>[12][0-9]{3})', text)
    if matches:
        return matches.group('year')
    return None

def fetch_movie(name):
    url = imdb_url(name)
    html = crawl_imdb(url)
    title = parse_title(html)
    year = parse_year(html)
    return title, year

def remove_subtitle(title):
    title = strip_after(title, '-')
    title = strip_after(title, ':')
    title = title.rstrip(' ')
    return title

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
        letter = input('> Rename \'' + name + '\' to \'' + title + '\'? (y/n) ')
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
    print(format(folder), year.ljust(4), format(title), format(rename_to), action, flush=True)

print_line('Input folder', 'Year', 'Title', 'Output folder', 'Action')
print('-' * (31 * 3 + 14))

for folder in folders():
    name = get_name(folder)
    title, year = fetch_movie(name)
    rename_to = ''
    action = 'Error'
    if title and year:
        # title = remove_subtitle(title)
        rename_to = title + ' (' + year + ')'
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

print('')
os.system('DONE')
