from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
#2190 2303
#2303 2416
#2416 2531

chrome = webdriver.Chrome('./chromedriver_win32\chromedriver.exe')
chrome.get("https://www.freemaptools.com/elevation-finder.htm")

def getData():
    global f, long, lati
    textbox = chrome.find_element_by_id("locationSearchTextBox")
    textbox.clear()
    textbox.send_keys(str(long/100)+', '+str(lati/100))
    textbox.send_keys(Keys.ENTER)
            
    time.sleep(0.4)
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
                
    string = str(soup)
    regex = re.search(r'\d+\.\d+ m or', string)
    f.write(str(long)+" "+str(lati)+' '+regex.group()[:-5]+"\n")

with open("data.txt", "a") as f:
    for long in range(2378, 2400):
        for lati in range(12003, 12202):
            try:
                getData()
            except AttributeError:
                try:
                    time.sleep(1)
                    getData()
                except AttributeError:
                    time.sleep(5)
                    getData()
            print(long, lati)
