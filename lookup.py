
import requests
import json

from tkinter import *

import numpy as np

import os
os.system('cls')

api_key = '44a83c23-8fd2-4c20-abb2-fb2c0803e235'

def api_call(api_key, start, limit):
    url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY='
    params = '&start={start}&limit={limit}&convert=USD'.format(start=start, limit=limit)
    
    api = url+api_key+params
    return api

api_request = requests.get(api_call(api_key, 1, 5000))

api = json.loads(api_request.content)

data = api['data']

def red_green(amount):
    if amount >= 0:
        return "green"
    else:
        return "red"

root = Tk()

root.title('Crypto Currency Portfolio')
root.iconbitmap(r'C:\\Users\\moona\\Desktop\\logo-_2_.ico')

name = Label(root, text='Ian Moore', bg = 'white')
name.grid(row=0, column=0, sticky = N+S+E+W)

## create header ##
header = ['Name', 'Rank', 'Current Price', 'Price Paid', 'P\L Per', '1-Hour Change', '24-Hour Change', 
         '7-Day Change', 'Current Value', 'P\L Total']

for i in header:
    col = header.index(i)
    if col % 2:
        header_name = Label(root, text= i, bg='white', font= 'Verdana 8 bold')
        header_name.grid(row=0, column = col, sticky= N+S+E+W)
    else:
        header_name = Label(root, text= i, bg='silver', font= 'Verdana 8 bold')
        header_name.grid(row=0, column = col, sticky= N+S+E+W)


def lookup():
    #api_request = requests.get(api_call(api_key, 1, 5000))
    #api = json.loads(api_request.content)
    
    my_portfolio = [
    {
        'sym':'STEEM',
        'amount_owned': 100,
        'price_paid_per': .02
    },
    {
        'sym':'XRP',
        'amount_owned': 100,
        'price_paid_per': 1.35
    }, 
    {
        'sym':'EOS',
        'amount_owned': 100,
        'price_paid_per': 1.10
    },
    {
        'sym':'XLM',
        'amount_owned': 100,
        'price_paid_per': .10
    }
    ]
    
    portfolio_profit_loss = 0
    row_count = 1

    for i in data:
        for coin in my_portfolio:
            if coin['sym'] == i['symbol']:
                
                # variables 
                name = i['name']
                rank = i['cmc_rank']
                current_price  = round(float(i['quote']['USD']['price']), 2)
                price_paid = round(float(coin['price_paid_per']), 2)
                one_hr_chg = i['quote']['USD']['percent_change_1h']
                tf_hr_chg = i['quote']['USD']['percent_change_24h']
                seven_day_chg = i['quote']['USD']['percent_change_7d']
                
                amount_owned = coin['amount_owned']
                
                #run some calcs
                total_paid = float(amount_owned)*(float(price_paid))
                current_value = round(float(amount_owned)*float(current_price), 2)
                profit_loss = round(current_value - total_paid, 2)
                profit_loss_per_coin = round(float(current_price) - float(price_paid), 2)

                portfolio_profit_loss += profit_loss

                print(name)                   
                print(' Current Price: ${0:.2f}'.format(float(current_price)))
                print(' Profit/Loss per Coin: ${0:.2f}'.format(float(profit_loss_per_coin)))
                print(' Rank: {0:.0f}'.format(float(rank)))
                print(' Total Paid: ${0:.2f}'.format(float(total_paid)))
                print(' Current Value: ${0:.2f}'.format(float(current_value)))
                print(' Profit/Loss: ${0:.2f}'.format(float(profit_loss)))
                print('------------------------------')
                
                
                column_data_1 = Label(root, text= name, bg='silver')
                column_data_1.grid(row=row_count, column = 0, sticky= N+S+E+W)
                
                column_data_2 = Label(root, text= rank, bg='white')
                column_data_2.grid(row=row_count, column = 1, sticky= N+S+E+W)
                
                column_data_3 = Label(root, text= "${0:.2f}".format(current_price), bg='silver')
                column_data_3.grid(row=row_count, column = 2, sticky= N+S+E+W)
                
                column_data_4 = Label(root, text= "${0:.2f}".format(price_paid), bg='white')
                column_data_4.grid(row=row_count, column = 3, sticky= N+S+E+W)
                
                column_data_5 = Label(root, text= "${0:.2f}".format(profit_loss_per_coin), bg='silver', fg = red_green(profit_loss_per_coin))
                column_data_5.grid(row=row_count, column = 4, sticky= N+S+E+W)
                
                column_data_6 = Label(root, text= "{0:.2f}%".format(one_hr_chg), bg='white', fg = red_green(one_hr_chg))
                column_data_6.grid(row=row_count, column = 5, sticky= N+S+E+W)
                
                column_data_7 = Label(root, text= "{0:.2f}%".format(tf_hr_chg), bg='silver', fg = red_green(tf_hr_chg))
                column_data_7.grid(row=row_count, column = 6, sticky= N+S+E+W)
                
                column_data_8 = Label(root, text= "{0:.2f}%".format(seven_day_chg), bg='white', fg = red_green(seven_day_chg))
                column_data_8.grid(row=row_count, column = 7, sticky= N+S+E+W)
                
                column_data_9 = Label(root, text= "${0:.2f}".format(current_value), bg='silver')
                column_data_9.grid(row=row_count, column = 8, sticky= N+S+E+W)
                
                column_data_10 = Label(root, text= "${0:.2f}".format(profit_loss), bg='white', fg = red_green(profit_loss))
                column_data_10.grid(row=row_count, column = 9, sticky= N+S+E+W)
                
                
                row_count += 1

    print('Total Profit/Loss: ${0:.2f}'.format(float(portfolio_profit_loss)))

lookup()
root.mainloop()