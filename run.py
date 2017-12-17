#!/usr/bin/python3
from renamer import folders, get_name, fetch_movie, compare_titles, user_decision, rename, print_line, get_year

print_line('Input folder', 'Year', 'Title', 'Output folder', 'Action')
print('-' * (31 * 3 + 14))

for folder in folders():
    name = get_name(folder)
    year_title = get_year(folder)
    year_title = (" %s" % year_title) if year_title else ""

    title, year = fetch_movie(name + year_title)
    rename_to = ''
    action = 'Error'
    if title and year:
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
