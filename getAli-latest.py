import sys
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import PySimpleGUI as sg
limit = 2

def get_items(search, page):
    search = search.replace(" ", "_")
    url = "https://aliexpress.com/af/{}.html?trafficChannel=af&d=y&CatId=0&SearchText={}&ltype=affiliate&SortType=default&page={}".format(
        search, search, page
    )
    driver.get(url)

    # sleep for two second then scroll to the bottom of the page
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)  # sleep between loadings

    items = driver.find_elements(By.CLASS_NAME, "_3t7zg")
    print(len(items))

    #print(items[0].find_element(By.XPATH, "//h3[@class='product-name']/a").get_attribute('href')) #use for testing
    output = []

    for i in items:

        try:
            name = i.find_element(By.CLASS_NAME, "_18_85").text
        except:
            name = None

        try:
            price = i.find_element(By.CLASS_NAME, "mGXnE").text
        except:
            price = None

        try:
            product_url = i.get_attribute('href')
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
# we will call the function get_items
sg.theme('DarkAmber')
layout = [[sg.Text('', size=(50, 1), relief='sunken', font=('Courier', 11),
    text_color='yellow', background_color='black',key='TEXT')]]
window = sg.Window('Loading...', layout, finalize=True)
text = window['TEXT']
state = 0

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
json.dump(all_items, open("productsAli.json", "w"), indent=2)
window.close()
driver.close()
