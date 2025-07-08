import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
import re

def get_url_recursive(url, depth, urls):
    while depth:
        depth -= 1
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        links = soup.find_all('a')
        img_links = soup.find_all('img')
        try:
            for link in links:
                linktext = link.get('href')
                if linktext not in urls and "https" in linktext:
                    for img_link in img_links:
                        img_url = urljoin(url, img_link.get('src'))
                        if img_url not in urls:
                            urls.append(img_url)
                    get_url_recursive(linktext, depth, urls)
        except:
            break

def get_url(url, urls):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    img_links = soup.find_all('img')
    for img_link in img_links:
        img_url = urljoin(url, img_link.get('src'))
        if img_url not in urls:
            urls.append(img_url)

args = sys.argv[1:]
depth = 0
path = "./data/"
url = ""
i = 0
for arg in args:
    i += 1
    if "-r" in arg:
        depth = 5
        print(depth)
    elif "-l" in arg:
        depth = int(re.search(r'\d+', arg)[0])
        print(depth)
    elif "-p" in arg:
        path = arg[2:]

urls = []
url = "https://www.scrapingbee.com/blog/selenium-python/"
if depth > 0:
    get_url_recursive(url, depth, urls)
else:
    get_url(url, urls)
image_name_counter = 1
for url in urls:
    file_name = urljoin(path, f"{image_name_counter}.jpg")
    try:
        img_data = requests.get(url).content
        with open(file_name, 'wb') as handler:
            handler.write(img_data)
            image_name_counter += 1
    except:
        continue
