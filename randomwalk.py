﻿# randomwalk.py
# input parameters are: number of MC runs, index in the s&p500./cv file, Quandl API key
# the file s&p500.csv should be in the same directory
# the output file is produced in the directory /tmp/outdata in the format <stock symbol>.csv
# each output file includes a random position (number of shares) between 1000 and 10000




import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
#import pandas_datareader.data as web
import csv
import sys
import linecache
from StringIO import StringIO
import random
import quandl
import time


#stock=sys.argv[1]
#parameters: MC runs, index, quandl key 
runs=sys.argv[1]
index=sys.argv[2]
qkey=sys.argv[3]


#offset = random.randint(4,100)


theline = linecache.getline("./sp500.csv", int(index))
f = StringIO(theline)
reader = csv.reader(f, delimiter=',')


for symbol in reader:
    stock=symbol[0]


#download price data into DataFrame
#quandl.ApiConfig.api_key = "K6gi-vvj-_T9AFhk2rpW"


quandl.ApiConfig.api_key = qkey
qstock = 'WIKI/'+stock


marketd = []


def getmd():
        try:        
                sleep(random.randint(0, 4))
                    print('quandl  '+stock+'   '+index)
                   marketd = quandl.get(qstock, start_date='2018-01-01')
        except:
                    return -1


        #calculate the compound annual growth rate (CAGR) which
        #will give us our mean return input (mu)
        days = (marketd.index[-1] - marketd.index[0]).days
        cagr = ((((marketd['Close'][-1]) / marketd['Close'][1])) ** (365.0/days)) - 1
        print ('CAGR =',str(round(cagr,4)*100)+"%")
        mu = cagr


        #create a series of percentage returns and calculate
        #the annual volatility of returns
        marketd['Returns'] = marketd['Close'].pct_change()
        vol = marketd['Returns'].std()*np.sqrt(252)
        print ("Annual Volatility =",str(round(vol,4)*100)+"%")


        #Define Variables
        S = marketd['Close'][-1] #starting stock price (i.e. last available real stock price)
        T = 252 #Number of trading days
        #mu = 0.2309 #Return
        #vol = 0.4259 #Volatility


        #set up empty list to hold our ending values for each simulated price series


        price_list = []


        position = random.randint(10,1000) * 10


        filename = "/tmp/outdata/"+stock+".csv"
        outfile = open(filename, 'wb')
        wr = csv.writer(outfile)


        for i in range(int(runs)):
                    #create list of daily returns using random normal distribution
                    daily_returns=np.random.normal(mu/T,vol/math.sqrt(T),T)+1


                    #set starting price and create price series generated by above random daily returns
                    price_list = [S]


                    for x in daily_returns:
                        price_list.append(price_list[-1]*x)


                    #plot data from each individual run which we will plot at the end
                     #plt.plot(price_list)


                    price_list.insert(0, stock)
                    price_list.insert(1, position)
                    price_list.insert(2, i)
                    wr.writerow(price_list)


        outfile.close()


if(getmd() > 0):
        print('done:  '+stock)
