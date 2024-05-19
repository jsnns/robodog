from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import base64
from PIL import Image
from io import BytesIO


def capture_canvas_images(url, interval=0.5):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    #
    driver.get(url)
    #
    # Click the button
    #
    while True:
        try:
            canvas_containers = driver.find_elements(By.CSS_SELECTOR, 'div.canvasContainer')
            image_count = 0
            # 
            for container in canvas_containers:
                canvas = container.find_element(By.CSS_SELECTOR, 'canvas[data-v-575a3a00], canvas[data-v-5c99097c]')
                canvas_data_url = driver.execute_script("return arguments[0].toDataURL('image/png').substring(22);", canvas)
                canvas_image_data = base64.b64decode(canvas_data_url)
                image = Image.open(BytesIO(canvas_image_data))
                # 
                image_path = f'canvas_image_{image_count}.png'
                image.save(image_path)
                print(f"Image saved to {image_path}")
                image_count += 1
            # 
            if image_count == 0:
                print("No canvases found in the canvasContainers")
        except Exception as e:
            print(f"An error occurred while capturing the canvas: {e}")
        #
        time.sleep(interval)
        
        



capture_canvas_images('http://10.103.153.64/vision')