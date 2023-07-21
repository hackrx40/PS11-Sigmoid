# import sys
# from selenium import webdriver
# from PIL import Image
# from io import BytesIO

# width = 390
# height = 844

# if len(sys.argv) > 1:
#     url = sys.argv[1]
#     if len(sys.argv) > 3:
#         width = int(sys.argv[2])
#         height = int(sys.argv[3])
# else:
#     print("Usage: python script.py <url> [width] [height]")
#     sys.exit(1)

# opts = webdriver.EdgeOptions()
# mobile_emulation = {
#     "deviceMetrics": { "width": width, "height": height, "pixelRatio": 3.0 },
#     "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36"
# }
# opts.add_experimental_option("mobileEmulation", mobile_emulation)
# opts.add_argument('--headless')

# browser = webdriver.Edge(options=opts)
# browser.get(' ')

# js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

# scrollheight = browser.execute_script(js)

# viewport_height = browser.execute_script("return window.innerHeight")
# offset = 0
# count = 0
# while offset < scrollheight:
#     browser.execute_script("window.scrollTo(0, %s);" % offset)
#     img = Image.open(BytesIO(browser.get_screenshot_as_png()))
#     offset += viewport_height

#     # Save each slice as a separate image
#     img.save(f'screenshot_{count}.png')
#     count += 1

# browser.quit()

import sys
import os
from selenium import webdriver
from PIL import Image
from io import BytesIO

width = 390
height = 844

if len(sys.argv) > 1:
    url = sys.argv[1]
    if len(sys.argv) > 3:
        width = int(sys.argv[2])
        height = int(sys.argv[3])
        md5_folder_name = sys.argv[4]
    else:
        print("Usage: python screenshot.py <url> [width] [height] [md5_folder_name]")
        sys.exit(1)
else:
    print("Usage: python screenshot.py <url> [width] [height] [md5_folder_name]")
    sys.exit(1)

opts = webdriver.EdgeOptions()
mobile_emulation = {
    "deviceMetrics": { "width": width, "height": height, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36"
}
opts.add_experimental_option("mobileEmulation", mobile_emulation)
opts.add_argument('--headless')

browser = webdriver.Edge(options=opts)
browser.get(url)

js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

scrollheight = browser.execute_script(js)

viewport_height = browser.execute_script("return window.innerHeight")
offset = 0
count = 0
while offset < scrollheight:
    browser.execute_script("window.scrollTo(0, %s);" % offset)
    img = Image.open(BytesIO(browser.get_screenshot_as_png()))
    offset += viewport_height
    # Save each slice as a separate image in the "inputs" folder under the md5_folder_name
    image_path = os.path.join('uploads', md5_folder_name, 'inputs', f'screenshot_{count}.png')
    img.save(image_path)
    count += 1

browser.quit()
