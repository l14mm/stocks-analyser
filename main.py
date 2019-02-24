import os
import numpy as np
from datetime import datetime
import smtplib
import time
from selenium import webdriver
# Prediction
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
# Stock Data
from iexfinance.stocks import Stock, get_historical_data


def getStocks(n):
    # Go to Yahoo stock screener
    url = 'https://finance.yahoo.com/screener/predefined/aggressive_small_caps?offset=0&count=202'
    driver.get(url)

    # Dismiss silly dialog
    btn = driver.find_element_by_xpath(
        '/html/body/div/div/div/form/div/button[2]')
    btn.click()

    stock_list = []
    n += 1
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[1]/a
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[3]/td[1]/a
    for i in range(1, n):
        ticker = driver.find_element_by_xpath(
            f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{str(i)}]/td[1]/a')
        stock_list.append(ticker.text)

    return stock_list


def predictData(stock, days):
    start = datetime(2017, 1, 1)
    end = datetime.now()
    # Outputting the Historical data into a .csv for later use
    df = get_historical_data(
        stock, start=start, end=end, output_format='pandas')
    csv_name = ('Exports/' + stock + '_Export.csv')
    df.to_csv(csv_name)
    df['prediction'] = df['close'].shift(-1)
    df.dropna(inplace=True)
    forecast_time = int(days)

    X = np.array(df.drop(['prediction'], 1))
    Y = np.array(df['prediction'])
    X = preprocessing.scale(X)
    X_prediction = X[-forecast_time:]
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.5)

    # Performing the Regression on the training data
    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))

    # Print if the predicted price of the stock is at least 1 greater than the previous closing price
    last_row = df.tail(1)
    if (float(prediction[4]) > (float(last_row['close']))):
        if prediction[4] > prediction[0]*1.1:
            print('\n*********\n')
            print(f'Stock: {str(stock)}')
            print(f"Prior Close: {str(last_row['close'])}")
            print(f'Prediction in 1 Day: {str(prediction[0])}')
            print(f'Prediction in 5 Days: {str(prediction[4])}')
            print(f'Increase: {prediction[4]/prediction[0]*100}%')


if __name__ == "__main__":
    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'])
    stock_list = getStocks(100)
    driver.close()

    # Using the stock list to predict the future price of the stock a specificed amount of days
    for i in stock_list:
        try:
            predictData(i, 5)
        except Exception as e:
            print("Stock: " + i + " was not predicted", e)
