###Run imports###
import requests
import json
import random

from tkinter import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as clr

###file holds api_key###
from api_key import api_key

###clears out console log###
import os
os.system('cls')

###Variable###
path = 'data.json'  #json file path

###functions###
#api call
def api_call(api_key, start, limit):
    url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY='
    params = '&start={start}&limit={limit}&convert=USD'.format(start=start, limit=limit)
    
    api = url+api_key+params
    return api

#red and green color coding for text based on profit and loss of total value
def red_green(amount):
    if amount >= 0:
        return "green"
    else:
        return "red"

#creates x-tick range for "Current Value per Coin"
def y_ticks(m):
    factor = 4
    maxy = round(max(m), -2)

    mm = maxy/factor

    y_axis = []
    i = 0
    while i <= factor:
        y_label = mm * i
        y_axis.append(int(y_label))
        i = i + 1
    return y_axis

#creates x-tick range for "Current P/L per Coin"
def y_ticks_pl(value):
    mn = round(min(value), -1)
    mx = round(max(value), -1)

    y_ticks_pl = []

    factor = 2
#determines min range
    im = 1
    while im <= factor:
        y_label_min = mn * im * 0.5
        y_ticks_pl.append(int(y_label_min))
        im = im + 1
#determines max range
    ix = 0
    while ix <= factor:
        y_label = mx * ix * 0.5
        y_ticks_pl.append(int(y_label))
        ix = ix + 1

    y_ticks_pl.sort()
    
    return y_ticks_pl

#defines color range for charts
def colors_defined(value):
    colors = []

    for i in value:
        if i >= 0:
            r = round(float(random.randint(0,155)/255), 2)
            g = round(float(random.randint(155,205)/255), 2)
            b = round(float(random.randint(0,125)/255), 2)
            a = 0.8
            green = clr.to_rgba(tuple([r,g,b]))
            print('Green: ' + str(green))
            colors.append(tuple(green))
        else:
            colors.append((.97, .5, .5, 1))

    return colors

#creates portfolio path to json file for reading ticker data
def portfolio(path):    
    json_file_path = path

    with open(json_file_path, 'r') as j:
         contents = json.loads(j.read())
        
    my_portfolio = list(contents)
    return my_portfolio    

###tkinter GUI setup###    
root = Tk()

root.iconbitmap(r'C:\\Users\\moona\\Desktop\\logo-_2_.ico')

## create header ##
header = ['Name', 'Rank', 'Current Price', 'Price Paid', 'P\L Per', '1-Hour Change', '24-Hour Change', 
         '7-Day Change', 'Current Value', 'P\L Total']

#creates header list and column coloring
for i in header:
    col = header.index(i)
    if col % 2:
        header_name = Label(root, text= i, bg='white', font= 'Verdana 8 bold')
        header_name.grid(row=1, column = col, sticky= N+S+E+W)
    else:
        header_name = Label(root, text= i, bg='silver', font= 'Verdana 8 bold')
        header_name.grid(row=1, column = col, sticky= N+S+E+W)



### creates major load and update function for app###
def lookup():
    api_request = requests.get(api_call(api_key, 1, 5000))
    api = json.loads(api_request.content)
    data = api['data']
    
    my_portfolio = portfolio(path)
    
    portfolio_profit_loss = 0
    total_current_value = 0
    
    row_count = 2

    name_list = []
    sym_list = []
    size = []
    value = []
    
    for i in data:
        for coin in my_portfolio:
            if coin['sym'] == i['symbol']:
                
                # data variables 
                name = i['name']
                rank = i['cmc_rank']
                sym = i['symbol']
                current_price  = round(float(i['quote']['USD']['price']), 2)
                price_paid = round(float(coin['price_paid_per']), 2)
                one_hr_chg = i['quote']['USD']['percent_change_1h']
                tf_hr_chg = i['quote']['USD']['percent_change_24h']
                seven_day_chg = i['quote']['USD']['percent_change_7d']
                
                amount_owned = coin['amount_owned']
                
                #run some calcs with variables
                total_paid = float(amount_owned)*(float(price_paid))
                current_value = round(float(amount_owned)*float(current_price), 2)
                profit_loss = round(current_value - total_paid, 2)
                profit_loss_per_coin = round(float(current_price) - float(price_paid), 2)

                portfolio_profit_loss += profit_loss
                total_current_value += current_value
                
                #charting variables
                name_list.append(name)
                size.append(current_value)
                value.append(profit_loss)
                sym_list.append(sym)
                
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
                

    ###GUI build###            
    root.title('Crypto Currency Porfolio - Portfolio Current Value: ${0:.2f}'.format(float(total_current_value)))
    
    portfolio_profits = Label(root, text='Portfolio P/L: ${0:.2f}'.format(float(portfolio_profit_loss)), font= 'Verdana 8 bold', fg=red_green(portfolio_profit_loss)) 
    portfolio_profits.grid(row=0, column = 0, sticky = W, padx=10, pady=10)
    
    update_button = Button(root, text='Update Prices', command = lookup)
    update_button.grid(row=0, column = 1, sticky=W+S, padx = 10, pady = 10)
    
    ###Add elements to list
    input_label = Label(root, text='Add Crypto to your Portfolio:')
    input_label.grid(row=0,column=2, columnspan=2, sticky=W+S, padx = 10, pady = 10)

    input_symbol = Entry(root, width=20)
    input_symbol.grid(row=0, column = 4, sticky=W+S, padx = 3, pady = 10)
    input_symbol.get()
    input_symbol.insert(0, 'Enter coin symbol')

    input_holding = Entry(root, width=20)
    input_holding.grid(row=0, column = 5, sticky=W+S, padx = 3, pady = 10)
    input_holding.get()
    input_holding.insert(0, 'Enter amount held')

    input_purchase_price = Entry(root, width=20)
    input_purchase_price.grid(row=0, column = 6, columnspan=2, sticky = W+S, padx = 3, pady = 10)
    input_purchase_price.get()
    input_purchase_price.insert(0, 'Enter purchase price')

    #Adds crypto holdings to json file
    def add_crypto():
        my_portfolio = portfolio(path)
        dict_parse = []
        dict_elements = ['sym', 'amount_owned', 'price_paid_per']
        dict_parse.append(input_symbol.get())
        dict_parse.append(input_holding.get())
        dict_parse.append(input_purchase_price.get())

        dictty = dict(zip(dict_elements, dict_parse))
        print(input_symbol.get(), input_holding.get(), input_purchase_price.get())
        print(dictty)

        my_portfolio.append(dictty.copy())
        print(my_portfolio)
        jsonString = json.dumps(my_portfolio)
        jsonFile = open("data.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    myButton = Button(root, text='Add to list', command=add_crypto)
    myButton.grid(row=0, column=8, columnspan = 2, sticky = W+S, padx = 3, pady = 10)
    
    #generates randomize greens or red for chart colors
    color_list = colors_defined(value)

    #Pie chart build
    def pie(name_list, size, color_list):
        # Data to plot
        labels = name_list
        sizes = size
        #colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        #colors = colors_defined(value)

        fig=Figure(figsize=(3, 3), dpi=100)

        plt = fig.add_subplot(111)
        plt.pie(sizes, colors=color_list, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 9})
        fig.suptitle('Current Value per Coin (% of total)', fontsize=10)
        #fig.legend(labels, loc='lower left', fontsize=9)

        canvas = FigureCanvasTkAgg(fig, master = root)  
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=row_count+1, columnspan=3, rowspan=5, padx = 10, pady = 10)
 
    pie(sym_list, size, color_list)
    
    #bar chart build
    def bar(name_list, size, color_list):
        # Data to plot
        objects = name_list
        y = size
        #colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        #colors = colors_defined(value)

        fig=Figure(figsize=(3, 3), dpi=100)

        plt = fig.add_subplot(111)
        plt.bar(objects, y, align='center', color = color_list)
        
        plt.set_xticklabels(objects, fontsize=9, rotation = 45)
        plt.set_yticklabels(y_ticks(size),fontsize=9)

        fig.suptitle('Current Value per Coin ($)', fontsize=10)
        
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master = root)  
        canvas.draw()
        canvas.get_tk_widget().grid(column=3, row=row_count+1, columnspan=3, rowspan=5, padx = 10, pady = 10)
 
    bar(sym_list, size, color_list)
    
    #bar chart build
    def bar_pl(name_list, value, color_list):
        # Data to plot
        objects = name_list
        y = value
        #colors = p_l_colors(value)

        fig=Figure(figsize=(3, 3), dpi=100)

        plt = fig.add_subplot(111)
        plt.bar(objects, y, align='center', color = color_list)
        
        plt.set_xticklabels(objects, fontsize=9, rotation = 45)
        plt.axhline(0, color='black')
        plt.set_yticks(y_ticks_pl(value))
        plt.set_yticklabels(y_ticks_pl(value),fontsize=9)

        fig.suptitle('Current P/L per Coin ($)', fontsize=10)
        
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master = root)  
        canvas.draw()
        canvas.get_tk_widget().grid(column=6, row=row_count+1, columnspan=4, rowspan=5, padx = 10, pady = 10)
 
    bar_pl(sym_list, value, color_list)
    print(value)
    print(y_ticks_pl(value))
    print(sym_list)
    
lookup()
root.mainloop()   