#!/usr/bin/python3
from renamer import folders, get_name, fetch_movie, compare_titles, user_decision, rename, print_line, get_year, rename_folder

print_line('Input folder', 'Year', 'Title', 'Output folder', 'Action')
print('-' * (31 * 3 + 14))

for folder in folders():
    rename_folder(folder)

print('')
os.system('DONE')
