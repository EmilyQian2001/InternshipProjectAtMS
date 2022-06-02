import pandas as pd
import csv
import re 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from random import randint
from time import sleep

header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'}
data = pd.read_csv('res.tsv', delimiter='\t')
urls = data.iloc[600:700,0]

# 添加selenium反反爬机制(undefined)

s = Service("C:\\Users\\t-yichunqian\\Desktop\\website\\msedgedriver.exe")
options =  webdriver.EdgeOptions()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # suppress warnings in console(don't work)
driver = webdriver.Edge(service=s, options=options)
driver.set_page_load_timeout(20)
driver.set_script_timeout(20)
driver.execute_script("window.alert = function() {};") # don't work
driver.maximize_window()

i = 598
fail_pattern = re.compile(r"can't reach this page")
for url in urls:
    i+=1
    status = "success"
    print(i)

    try:
        driver.get(url)
    except:
        status = "fail"
    if url == "https://sa.www4.irs.gov/irfof/lang/en/irfofgetstatus.jsp":
        wait = WebDriverWait(driver,6)
        alert = wait.until(expected_conditions.alert_is_present())
        alert.accept()
    driver.implicitly_wait(15)
    sleep(randint(2,4))
    
    html = driver.page_source
    if re.search(fail_pattern, html):
        status = "fail"
    # soup = BeautifulSoup(html,'lxml')
    # # print(soup.prettify())
    # text = soup.get_text(separator=' ')
    # text = re.sub(r'[\ \n\t]{2,}', r' ', text)
    # rule = re.compile(r'[^a-zA-Z0-9\ \n\t]') # English literal and number only
    # new_text = rule.sub('',text)
    # if(len(text)> 500 and len(new_text)/len(text)>0.85):
    #     print(url)
    #     print(i)
    #     print("----------------------------------")
    #     list.append([url, text])
    # time.sleep(5)
    with open('rawdata/file%s.txt'%i, 'w', newline='', encoding='utf-8') as f:
        f.write(url)
        f.write("\n")
        f.write(status)
        f.write("\n")
        f.write(html)
        f.close()
print(i)
driver.quit()


