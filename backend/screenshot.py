import sys
import os
from selenium import webdriver
from PIL import Image
from io import BytesIO

def take_screenshot(url, width, height, md5_folder_name, device_type, count = 1):
    opts = webdriver.ChromeOptions()
    mobile_emulation = {
        "deviceMetrics": { "width": width, "height": height, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36"
    }
    opts.add_experimental_option("mobileEmulation", mobile_emulation)
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=opts)
    browser.get(url)

    # Get the total height of the webpage by executing JavaScript in the browser
    js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'
    scrollheight = browser.execute_script(js)

    # Get the height of the browser viewport
    viewport_height = browser.execute_script("return window.innerHeight")

    offset = 0
    while offset < scrollheight:
        # Scroll the webpage to capture screenshots of the entire webpage
        browser.execute_script("window.scrollTo(0, %s);" % offset)

        # Take a screenshot of the current viewport and save it as an image
        img = Image.open(BytesIO(browser.get_screenshot_as_png()))

        # Increase the offset for the next screenshot
        offset += viewport_height

        # Save each slice as a separate image in the "inputs" folder under the md5_folder_name
        image_name = f'{device_type}_{count}.png'
        image_path = os.path.join('uploads', md5_folder_name, 'inputs', image_name)
        img.save(image_path)

        count += 1

    browser.quit() 
