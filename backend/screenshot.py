import sys
import os
from selenium import webdriver
from PIL import Image
from io import BytesIO

def take_screenshot(url, width, height, md5_folder_name, device_type, count):
    # Configure Selenium WebDriver with EdgeOptions to simulate mobile device
    opts = webdriver.EdgeOptions()
    mobile_emulation = {
        "deviceMetrics": { "width": width, "height": height, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36"
    }
    opts.add_experimental_option("mobileEmulation", mobile_emulation)
    opts.add_argument('--headless')  # Run the browser in headless mode (without a GUI)

    # Create a new instance of the Edge browser
    browser = webdriver.Edge(options=opts)
    browser.get(url)  # Load the specified URL in the browser

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
        image_name = f"{device_type}_{count}.png"
        image_path = os.path.join('uploads', md5_folder_name, 'inputs', image_name)
        img.save(image_path)

        count += 1

    browser.quit()  # Close the browser after capturing all screenshots

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python screenshot.py <url> <width> <height> <md5_folder_name> <device_type>")
        sys.exit(1)

    url = sys.argv[1]  # Get the URL from the command-line argument
    width = int(sys.argv[2])  # Get the width from the command-line argument and convert to an integer
    height = int(sys.argv[3])  # Get the height from the command-line argument and convert to an integer
    md5_folder_name = sys.argv[4]  # Get the MD5 folder name from the command-line argument
    device_type = sys.argv[5]  # Get the device type from the command-line argument

    take_screenshot(url, width, height, md5_folder_name, device_type, 1)  # Call the function to take the screenshot
