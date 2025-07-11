#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def get_url_recursive(url, depth, urls):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    img_links = soup.find_all('img')
    for img_link in img_links:
        img_url = urljoin(url, img_link.get('src'))
        if img_url not in urls:
            urls.append(img_url)
    if depth > 1:
        links = soup.find_all('a')
        for link in links:
            linktext = link.get('href')
            if linktext.startswith("http"):
                get_url_recursive(linktext, depth - 1, urls)

parser = argparse.ArgumentParser()
parser.add_argument("-r", help="recursively download images from the website and its linked websites", action="store_true")
parser.add_argument("-l", type=int, help="set the depth of the recursion, if not specified it defaults to 5")
parser.add_argument("-p", help="set the path to which images are downloaded, if not specified it defaults to ./data")
parser.add_argument("url", help="the website to download images from")
args = parser.parse_args()

depth = 0
if args.r:
    depth = 5
if args.r and args.l:
    depth = args.l
path = "./data/"
if args.p:
    path = args.p
url = args.url

urls = []
get_url_recursive(url, depth, urls)
image_name_counter = 1
for url in urls:
    file_name = urljoin(path, f"{image_name_counter}")
    if url[url.rfind("."):].find("/") != -1:
        continue
    ext_end = url.rfind("?")
    if ext_end == -1:
        file_name += url[url.rfind("."):]
    else:
        file_name += url[url.rfind("."):ext_end]
    try:
        img_data = requests.get(url).content
        with open(file_name, 'wb') as handler:
            handler.write(img_data)
            image_name_counter += 1
    except Exception as e:
        continue
