import sys
from selenium import webdriver
from PIL import Image
from io import BytesIO
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

width = 390
height = 844

if len(sys.argv) > 1:
    url = sys.argv[1]
    if len(sys.argv) > 3:
        width = int(sys.argv[2])
        height = int(sys.argv[3])
else:
    print("Usage: python script.py <url> [width] [height]")
    sys.exit(1)

opts = webdriver.EdgeOptions()
mobile_emulation = {
    "deviceMetrics": { "width": width, "height": height, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36"
}
opts.add_experimental_option("mobileEmulation", mobile_emulation)
opts.add_argument('--headless')


def get_all_sub_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
    sub_urls = []
    urls = soup.find_all('a')
    for anchor_tag in urls:
        href = anchor_tag.get('href')
        if href and "bajajfinserv" in href:
            print(href)
            absolute_url = urljoin(base_url, href)
            print(absolute_url)
            sub_urls.append(absolute_url)
            print(absolute_url)
    return sub_urls

sub_urls = get_all_sub_urls(url)


count = 0
for main_url in sub_urls:

    browser = webdriver.Edge(options=opts)
    browser.get("https//:bajajfinserv.in/")

    js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

    scrollheight = browser.execute_script(js)

    viewport_height = browser.execute_script("return window.innerHeight")
    offset = 0

    while offset < scrollheight:
        browser.execute_script("window.scrollTo(0, %s);" % offset)
        img = Image.open(BytesIO(browser.get_screenshot_as_png()))
        offset += viewport_height

        # Save each slice as a separate image
        img.save(f'Bajaj4/screenshot_{count}.png')
        count += 1
    
    #i +=1

browser.quit()