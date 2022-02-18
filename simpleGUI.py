import sys
import os
import PySimpleGUI as sg
sg.theme('DarkAmber')
sites = ["Watani", "Ajeeb", "Shein", "AliExpress", "Mart.ps"]
font = ("Arial, 13")

layout = [[sg.Text('Website Scraping Tool', size=(30, 1), font=font)],
         [sg.Text('Birzeit Univerity - Natural lanuage processing\n', font=font)],
          [sg.Text('Enter keyword\t\t', size=(20,1), font=font), sg.Text('      Enter pages',size=(20,1), font=font)],
          [sg.InputText(key='-INWEB-', size=(30,1)), sg.InputText(key='-INPAGES-', size=(15,1))],
          [sg.Combo(sites, size=(28,1), default_value='Watani', key='-combo-'), ],
          [sg.Submit(), sg.Cancel()]]


window = sg.Window('NLP scraping project', layout)

event, values = window.read()
window.close()

website = values['-INWEB-']
pages = values['-INPAGES-']
comboval = values['-combo-']

if(comboval == "Watani"):
    print("fetching data from "+comboval + pages)
    os.system("python getwatani-latest.py "+website+" "+pages)
elif(comboval== "Ajeeb"):
    print("fetching data from " + comboval + pages)
    os.system("python getajeeb-latest.py " + website + " " + pages)
elif (comboval == "Shein"):
    print("fetching data from " + comboval + pages)
    os.system("python getShein-latest.py " + website + " " + pages)
elif (comboval == "AliExpress"):
    print("fetching data from " + comboval + pages)
    os.system("python getAli-latest.py " + website + " " + pages)
elif (comboval == "Mart.ps"):
    print("fetching data from " + comboval + pages)
    os.system("python getMart-latest.py " + website + " " + pages)
