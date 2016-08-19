#!/usr/bin/python3

import requests
import argparse
import re
import sys
import os

parser = argparse.ArgumentParser(description='Download comics from porncomics.info')
parser.add_argument("-u", help="Url")
args = parser.parse_args()

home = os.getenv("HOME")

download_dir = '{0}/Pictures/porncomics'.format(home)

# We set args.u to the var url
url = args.u
# Here we check if the last char is / and if so remove it, this becomes important when doing the regex later on
if url[-1:] == '/':
    url = url[:-1]
else:
    pass
# We get the page text
page = requests.get(args.u).text
# We split on the char / to break up the url
search_term_split = args.u.split('/')
# get the 4th item from the broken up url (The comics name)
# We do a check to see if the bit of the url we got is the right one
if search_term_split[3] == 'www.porncomics.info':
    print("There was a error getting the comic ID\nExiting")
    sys.exit()
elif search_term_split[3] == '':
    print("There was a error getting the comic ID\nExiting")
    sys.exit()
search_term = search_term_split[3]
# We use a regex to find the links to all the comics pages
comic_pages = re.findall('{0}/[a-zA-Z0-9_-]*/'.format(url), page)
# X is going to be our page number so comics are kept in order
x = 1
for i in comic_pages:
    print('Grabbing {0}'.format(i))
    # print(comic_pages)
    comic_page = requests.get(i).text
    # We use regex to get the comics page image url
    page_image = re.findall('http://www.porncomics.info/wp-content/uploads/\d+/\d+/.*\.(?:jpg|gif|png|jpeg|gifv)', comic_page)
    # We check the number of items in the list because sometimes the list returns 0
    # We use the sites 404 message to weed out any 404s
    if len(page_image) != 0 and "Sorry, no posts matched your criteria" not in comic_page:
        # The path for us to make
        path = '{0}/{1}'.format(download_dir, search_term_split[3])
        os.system('mkdir -p {0}'.format(path))
        # The file path
        file_path = '{0}/{1}_{2}'.format(path, x, page_image[1].split('/')[7])
        r = requests.get(page_image[1], stream=True)
        with open(file_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        x = x + 1
    else:
        pass
