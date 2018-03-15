#!/usr/bin/python3
import os
import sqlite3

conn = sqlite3.connect('/home/osmc/.kodi/userdata/Database/MyVideos107.db')
c = conn.cursor()

def file_name(folder):
    return folder.split(" (")[0]

def clean_file_name(folder):
    replace = (
        ("Star Trek:", "Star Trek"),
    )

    name = file_name(folder)

    for rp in replace:
        name = name.replace(rp[0], rp[1])

    return name.strip(".")

def folders():
    DIRECTORY = 1
    return next(os.walk(os.curdir))[DIRECTORY]

def check_if_movie_exists(name):
    c.execute("SELECT count(*) FROM movie WHERE c00 like ?", ("%%%s%%" % clean_file_name(name),))
    count = c.fetchone()

    result = count[0] > 0

    if not result:
        print(file_name(name), count)

    return result

for folder in folders():
    check_if_movie_exists(folder)
