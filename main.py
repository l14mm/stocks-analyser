import os
import numpy as np
from datetime import datetime
import smtplib
import time
from selenium import webdriver
# Prediction
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import cross_validate
# Stock Data
from iexfinance.stocks import Stock
from iexfinance import *

def getStocks(n):
    # Go to Yahoo stock screener
    url = 'https://finance.yahoo.com/screener/predefined/aggressive_small_caps?offset=0&count=202'
    driver.get(url)

    # Dismiss silly dialog
    btn = driver.find_element_by_xpath('/html/body/div/div/div/form/div/button[2]')
    btn.click()

    stock_list = []
    n += 1
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[1]/a
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[3]/td[1]/a
    for i in range(1, n):
        ticker = driver.find_element_by_xpath(
            f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{str(i)}]/td[1]/a')
        stock_list.append(ticker.text)

    print(stock_list)

if __name__ == "__main__":
    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'])
    getStocks(5)
    driver.close()

