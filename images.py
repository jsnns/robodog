from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import base64
from selenium import webdriver
def capture_canvas_images(url, image_path='canvas_image.png', interval=0.5):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    #
    url = 'http://10.103.153.64/vision'
    driver.get(url)
    #
    #
    while True:
        try:
            canvas = driver.find_element(By.CSS_SELECTOR, 'canvas[data-v-575a3a00]')
            canvas_data_url = driver.execute_script("return arguments[0].toDataURL('image/png').substring(22);", canvas)
            canvas_image_data = base64.b64decode(canvas_data_url)
                #
            with open(image_path, 'wb') as image_file:
                image_file.write(canvas_image_data)
            #
            print(f"Image saved to {image_path}")
        except Exception as e:
            print(f"An error occurred while capturing the canvas: {e}")
        #
        time.sleep(interval)
capture_canvas_images('http://10.103.153.64/vision')





