import sys
import time
import json
import PySimpleGUI as sg
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

limit = 2

def get_items(search, page):
    search = search.replace(" ", "_")
    url = "https://eur.shein.com/pdsearch/{}/?ici=s1%60EditSearch%60{}%60_fb%60d0%60PagesSearchResult&scici=Search~~EditSearch~~1~~{}~~~~0&page={}".format(
        search, search, search, page
    )
    driver.get(url)

    # sleep for two second then scroll to the bottom of the page
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)  # sleep between loadings

    items = driver.find_elements(By.CLASS_NAME, "S-product-item")

    #print(items[0].find_element(By.XPATH, "//h3[@class='product-name']/a").get_attribute('href')) #use for testing
    output = []

    for i in items:

        try:
            name = i.find_element(By.CLASS_NAME, "S-product-item__name").text
        except:
            name = None

        try:
            price = i.find_element(By.CLASS_NAME, "S-product-item__price").text.replace('\u20ac', '')
        except:
            price = None

        try:
            product_url = i.find_element(By.CLASS_NAME, "S-product-item__link").get_attribute('href')
        except:
            product_url = None

        output_item = {"name": name, "price": price, "url": product_url}
        output.append(output_item)

    return output


# elements-offer-price-normal__price
chrome_options = Options()
chrome_options.add_argument("--headless")
ser = Service('C:\Program Files\webdriver\chromedriver.exe')
driver = webdriver.Chrome(options=chrome_options, executable_path='C:\Program Files\webdriver\chromedriver.exe')


if(len(sys.argv)>1):
    limit = int(sys.argv[2])
    search = sys.argv[1] # since we would like to search for Inflight Items
else:
    exit("bad argument")
all_items = []
# we will call the function get_items
page=1

sg.theme('DarkAmber')
layout = [[sg.Text('', size=(50, 1), relief='sunken', font=('Courier', 11),
    text_color='yellow', background_color='black',key='TEXT')]]
window = sg.Window('Loading...', layout, finalize=True)
text = window['TEXT']
state = 0

state = (state + int(50 / limit)) % 51
while True:
    print("getting page", page)
    results = get_items(search, page)
    all_items += results

    if len(results) == 0:
        break

    page += 1

    event, values = window.read(timeout=100)

    if event == sg.WINDOW_CLOSED:
        break
    state = (state + int(50 / limit)) % 51
    text.update('█' * state)

    if page >= limit:
        break

# save all the items to a json file
json.dump(all_items, open("productShein.json", "w"), indent=2)

driver.close()
