Movie folder rename
===================

Python script that helps cleaning up your movie collection. Scanning a folder, it looks up all sub directories on IMDb. Extracted movie title and year are use to update the folder name. It tries to match against IMDb search results page and asks the user else.

Instructions
------------

The scripts scans all folders in directory it gets started. So move the script in the directory of your movie collection and run it with Python 3.

Notes
-----

This script reads HTML content from IMDb for movie titles and release years. Therefore, like with all scrapers, it may break when the site changes its structure. If this doesn't work anymore, please report.

License
-------

This script is written by Danijar Hafner. Private use permitted. Don't publish without credits and link to repository.
