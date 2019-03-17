from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import base64
import time
import sys
import os

#################### Change this ######################
url = "http://www.doc88.com/p-8989288134788.html"
#######################################################

#################### Change if required ###############
driver = webdriver.Firefox(executable_path='.//geckodriver')
# At the moment, only works on chrome 74 +
#driver = webdriver.Chrome(executable_path='.//chromedriver')
#######################################################






try:
    driver.set_page_load_timeout(15)
    driver.get(url)
except:
    print("Timeout - start download anyway.")

time.sleep(5)
elem_cont_button = driver.find_element_by_id("continueButton")
driver.execute_script("arguments[0].scrollIntoView(true);", elem_cont_button)
actions = ActionChains(driver)
actions.move_to_element(elem_cont_button).perform()
time.sleep(0.5)
elem_cont_button.click()

num_of_pages = int(driver.find_element_by_id('readshop').find_element_by_class_name('mainpart').find_element_by_class_name('shop3').find_element_by_class_name('text').get_attribute('innerHTML')[-3:])
print("Number of pages to save {}".format(num_of_pages))

if not os.path.exists('./output'):
	os.mkdir('output')

for pages in range(num_of_pages):
    time.sleep(0.5)

    canvas_id = "page_" + str(pages + 1)
    pagepb_id = "pagepb_" + str(pages + 1)

    element = driver.find_element_by_id(canvas_id)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(0.5)

    # Check loading status
    while(len(driver.find_element_by_id(pagepb_id).get_attribute('innerHTML')) != 0):
        sys.stdout.write('.')
        time.sleep(0.5)

    #
    js_cmd = 	"var canvas = document.getElementById('{}');".format(canvas_id) + \
    		"return canvas.toDataURL();"
    img_data = driver.execute_script(js_cmd)

    print("Save {}".format(pages))
    img_data = (img_data[22:]).encode()

    with open("./output/image{}.png".format(pages), "wb") as fh:
        fh.write(base64.decodebytes(img_data))
