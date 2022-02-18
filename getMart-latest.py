import sys
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import PySimpleGUI as sg

#https://mart.ps/search?controller=search&orderby=position&orderway=desc&search_query=phone&submit_search=%D8%A8%D8%AD%D8%AB

def get_items(search):
    search = search.replace(" ", "_")
    url = "https://mart.ps/search?controller=search&orderby=position&orderway=desc&search_query={}&submit_search=%D8%A8%D8%AD%D8%AB".format(
        search
    )
    driver.get(url)

    # sleep for two second then scroll to the bottom of the page
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)  # sleep between loadings

    items = driver.find_elements(By.CLASS_NAME, "ajax_block_product")
    output = []

    for i in items:

        try:
            name = i.find_element(By.CLASS_NAME, "product-name").text
        except:
            name = None

        try:
            price = i.find_element(By.CLASS_NAME, "price").text.replace('\u20aa', '')
        except:
            price = None

        try:
            product_url = i.find_element(By.CLASS_NAME, "product-name").get_attribute('href')
        except:
            product_url = None

        output_item = {"name": name, "price": price, "url": product_url}
        output.append(output_item)

    return output


# we will call the function get_items

# elements-offer-price-normal__price
chrome_options = Options()
chrome_options.add_argument("--headless")
ser = Service('C:\Program Files\webdriver\chromedriver.exe')
driver = webdriver.Chrome(options=chrome_options, executable_path='C:\Program Files\webdriver\chromedriver.exe')
sg.theme('DarkAmber')
layout = [[sg.Text('Please wait while data is harvested', size=(50, 1), relief='sunken', font=('Courier', 13),
    text_color='yellow',key='TEXT')]]
window = sg.Window('Loading...', layout, finalize=True)
text = window['TEXT']
state = 0
if(len(sys.argv)>1):
    limit = int(sys.argv[2])
    search = sys.argv[1] # since we would like to search for Inflight Items
else:
    exit("bad argument")
all_items = []

# we will call the function get_items
results = get_items(search)
all_items += results

# save all the items to a json file
json.dump(all_items, open("productsMart.json", "w"), indent=2)
window.close()
driver.close()
