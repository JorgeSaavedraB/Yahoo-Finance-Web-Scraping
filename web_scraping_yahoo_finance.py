#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup

import requests
import numpy as np
import time
from time import sleep
import pandas as pd

#Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from lxml import html
import lxml


# In[2]:


def get_html(url):
    #my user agent
    Chrome_driver = 'Chrome/114.0.5735.90 Safari/537.36'
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' + Chrome_driver}
    response = requests.get(url, headers = header)
    
    if response.status_code == 200:
        return response.text
    else:
        return None


# In[3]:


def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text
    
    price = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find('fin-streamer').text
    
    return title, price


# ### Basic information

# In[4]:


def basic_inf(symbol):
    
    #Get url
    url = 'https://finance.yahoo.com/quote/' + symbol
    print(url)
    
    #Get html
    html = get_html(url)
    
    title, price = parse_data(html)
    print('Title: ' + title)
    print('Price: ' + price)


# ### Price

# In[5]:


def stock_price(symbol):
    #Get url
    url = 'https://finance.yahoo.com/quote/' + symbol
    
    #Get html
    html = get_html(url)
    
    title, price = parse_data(html)
    s_price = price
    return float(s_price.replace(',', ''))


# ### Financial Statements

# In[1]:


def Financial_Statements(ticker, statement, anual_quarterly):

    chrome_path = Service(r"C:\Users\hybri\Downloads\chromedriver_win32\chromedriver.exe")
    driver = webdriver.Chrome(service = chrome_path, options = webdriver.ChromeOptions())
    
    if(statement == 'balance sheet'):
        url = 'https://finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker
    elif(statement == 'income statement'):
        url = 'https://finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
    elif(statement == 'cash flow'):
        url = 'https://finance.yahoo.com/quote/' + ticker +  '/cash-flow?p=' + ticker
    else:
        None
    driver.get(url)
    driver.implicitly_wait(5)

    
    if(anual_quarterly == 'quarterly'):
        #clicking "Expand All"
        btnclick0 = driver.find_elements(By.XPATH, "//section[@data-test='qsp-financial']//span[text()='Quarterly']")
        btnclick0[0].click()
        time.sleep(0.5)
        btnclick = driver.find_elements(By.XPATH, "//*[@id='Col1-1-Financials-Proxy']/section/div[2]/button")
        btnclick[0].click()
        time.sleep(0.5)
    elif(anual_quarterly == 'anual'):
        #clicking "Expand All"
        btnclick = driver.find_elements(By.XPATH, "//*[@id='Col1-1-Financials-Proxy']/section/div[2]/button")
        btnclick[0].click()
    else:
        None

    #parsing into lxml
    tree = html.fromstring(driver.page_source)

    #searching table financial data
    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

    # Ensure that some table rows are found
    assert len(table_rows) > 0

    parsed_rows = []

    for table_row in table_rows:
        parsed_row = []
        el = table_row.xpath("./div")

        none_count = 0

        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
            except ValueError:
                parsed_row.append(np.NaN)
                none_count += 1

        if (none_count < 4):
            parsed_rows.append(parsed_row)

    return parsed_rows


# In[ ]:


def Financial_Statements_2(ticker, statement, anual_quarterly):
    
    F_S = Financial_Statements(ticker , statement, anual_quarterly)
    
    all_rows = []
    
    for k in range(len(F_S)):
        new_row = []
        new_row.append(F_S[k][0])
        
        for i in range(len(F_S[k][:]) - 1, 0, -1):
            new_row.append(F_S[k][i])
            
        all_rows.append(new_row)

    return all_rows

