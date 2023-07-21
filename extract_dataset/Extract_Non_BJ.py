import sys
from selenium import webdriver
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

width = 375
height = 810


opts = webdriver.EdgeOptions()
mobile_emulation = {
    "deviceMetrics": { "width": width, "height": height, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36"
}
opts.add_experimental_option("mobileEmulation", mobile_emulation)
opts.add_argument('--headless')


def extract_website_names_from_images(folder_path):
    website_names = []
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    for filename in os.listdir(folder_path):
        name, ext = os.path.splitext(filename)
        website_names.append(f'https://{name}')
    
    return website_names


count = 0
folder_path = 'C:/Users/rahuz/Downloads/Compressed/archive/screenshots-224x224/screenshots-224x224/NBajaj'
website_names = extract_website_names_from_images(folder_path)

for main_url in website_names:

    try:
        browser = webdriver.Edge(options=opts)
        browser.get(main_url)

        js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

        scrollheight = browser.execute_script(js)

        viewport_height = browser.execute_script("return window.innerHeight")
        offset = 0

        while offset < scrollheight:
            browser.execute_script("window.scrollTo(0, %s);" % offset)
            img = Image.open(BytesIO(browser.get_screenshot_as_png()))
            offset += viewport_height

            # Save each slice as a separate image
            img.save(f'NBajaj/screenshot_{count}.png')
            count += 1
    except: print('oops')
    
    #i +=1

browser.quit()