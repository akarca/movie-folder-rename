#!/usr/bin/python3
import sys

from renamer import folders, get_name, fetch_movie, compare_titles, user_decision, rename, print_line, get_year, rename_folder

print_line('Input folder', 'Year', 'Title', 'Output folder', 'Action')
print('-' * (31 * 3 + 14))

args = sys.argv
if len(args) > 1:
    for folder in args[1:]:
        rename_folder(folder)
else:
    for folder in folders():
        rename_folder(folder)

print('')
print('DONE')
