# -*- coding: utf-8 -*-
"""
A module to perform financial analysis on the API Data gathered.

Created on Wed Jul 17 11:35:23 2019

@author: sdtaylor
"""

import copy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import urllib, base64


def calculate_totals(api_data_dict):
    """
    Function to reorder the dictionary prior to converting to dataframe.
    
    Parameters
    ----------
        api_data_dict : dict
            dictionary of the sheets (keys) and the associated data to fill the 
            rows as a dictionary where keys are header names and values are the
            row values.
    
    Returns
    -------
        rearranged_dict : dict
            rearranged dictionary with newly created columns for totals.
    """
    
    api_data_dict_updated = copy.deepcopy(api_data_dict)

    """
    Adjust latestPrice for currency purchased in
    """
    for key, value in api_data_dict_updated.items():

        # create temp lists
        temp_list = []
        temp_list_price = []
        temp_list_fx = []
        temp_list_curr = []

        # add values to temp arrays
        for part_key, part_value in value.items():
            if part_key == 'latestPrice':
                for i in value[part_key]:
                    temp_list_price.append(i)

            if part_key == 'fx_USDCAD_current':
                for i in value[part_key]:
                    temp_list_fx.append(i)

            if part_key == 'purchase_currency':
                for i in value[part_key]:
                    temp_list_curr.append(i)

        # adjust prices
        counter = 0
        for i in temp_list_curr:
            if i == 'CAD':
               adj_value = temp_list_price[counter] * temp_list_fx[counter]
            else:
               adj_value = temp_list_price[counter]

            temp_list.append(adj_value)
            counter += 1

        api_data_dict_updated[key]['latestPrice'] = temp_list
    
    """
    Adjust current dividend for currency
    """
    for key, value in api_data_dict_updated.items():

        # create temp lists
        temp_list = []
        temp_list_div = []
        temp_list_fx = []
        temp_list_curr = []

        # add values to temp arrays
        for part_key, part_value in value.items():
            if part_key == 'currentDividend':
                for i in value[part_key]:
                    temp_list_div.append(i)

            if part_key == 'fx_USDCAD_current':
                for i in value[part_key]:
                    temp_list_fx.append(i)

            if part_key == 'purchase_currency':
                for i in value[part_key]:
                    temp_list_curr.append(i)

        # adjust prices
        counter = 0
        for i in temp_list_curr:
            if i == 'CAD':
               adj_value = temp_list_div[counter] * temp_list_fx[counter]
            else:
               adj_value = temp_list_div[counter]

            temp_list.append(adj_value)
            counter += 1

        api_data_dict_updated[key]['currentDividend'] = temp_list
      
    """
    Adjust YTD Dividend for investment not in native currency
    """
    for key, value in api_data_dict_updated.items():

        # create temp lists
        temp_list = []
        temp_list_div_income = []
        temp_list_adjdivcurr = []
        temp_list_fx = []
        temp_list_curr = []
        temp_list_ytddiv = []
        temp_list_divcurr = []
        temp_list_qty = []

        # add values to temp arrays
        for part_key, part_value in value.items():
            if part_key == 'qty':
                for i in value[part_key]:
                    temp_list_qty.append(i)
            
            if part_key == 'fx_USDCAD_current':
                for i in value[part_key]:
                    temp_list_fx.append(i)

            if part_key == 'purchase_currency':
                for i in value[part_key]:
                    temp_list_curr.append(i)
                    
            if part_key == 'ytdDividendIncome':
                for i in value[part_key]:
                    temp_list_ytddiv.append(i)
                    
            if part_key == 'divCurrency':
                for i in value[part_key]:
                    temp_list_divcurr.append(i)

        # adjust prices
        counter = 0
        for i in temp_list_curr:
            if i == 'CAD':
                if temp_list_divcurr[counter] == 'USD':
                    adj_value = temp_list_ytddiv[counter] * temp_list_fx[counter]
                    adj_div_curr = 'CAD'
                elif temp_list_divcurr[counter] == 'CAD':
                    adj_value = temp_list_ytddiv[counter]
                    adj_div_curr = 'CAD'
                else:
                    adj_value = 0
                    adj_div_curr = ''
            else:
                if temp_list_divcurr[counter] == 'CAD':
                    adj_value = temp_list_ytddiv[counter] / temp_list_fx[counter]
                    adj_div_curr = 'USD'
                elif temp_list_divcurr[counter] == 'USD':
                    adj_value = temp_list_ytddiv[counter]
                    adj_div_curr = 'USD'
                else:
                    adj_value = 0
                    adj_div_curr = ''

            temp_list.append(adj_value)
            temp_list_adjdivcurr.append(adj_div_curr)
            counter += 1
            
        counter = 0
        for i in temp_list:
            total_div_income = i * temp_list_qty[counter]
            temp_list_div_income.append(total_div_income)
            counter += 1
        
        api_data_dict_updated[key]['ytdDividendIncome'] = temp_list_div_income
        api_data_dict_updated[key]['adjustedDividendCurrency'] = temp_list_adjdivcurr

    """
    Calculate purchase value
    """
    for key, value in api_data_dict_updated.items():

        # create temp lists
        temp_list = []
        temp_list_book_price = []
        temp_list_qty = []

        # add values to temp arrays
        for part_key, part_value in value.items():
            if part_key == 'book_price':
                for i in value[part_key]:
                    temp_list_book_price.append(i)

            if part_key == 'qty':
                for i in value[part_key]:
                    temp_list_qty.append(i)

        # create book value
        counter = 0
        for i in temp_list_book_price:
            book_price = i * temp_list_qty[counter]
            temp_list.append(book_price)
            counter += 1

        api_data_dict_updated[key]['book_value'] = temp_list

    """
    Calculate current value
    """
    for key, value in api_data_dict_updated.items():

        # create temp lists
        temp_list = []
        temp_list_price = []
        temp_list_qty = []

        # add values to temp arrays
        for part_key, part_value in value.items():
            if part_key == 'latestPrice':
                for i in value[part_key]:
                    temp_list_price.append(i)

            if part_key == 'qty':
                for i in value[part_key]:
                    temp_list_qty.append(i)

        # create book value
        counter = 0
        for i in temp_list_price:
            latestPrice = i * temp_list_qty[counter]
            temp_list.append(latestPrice)
            counter += 1

        api_data_dict_updated[key]['current_value'] = temp_list
        
    """
    Calculate total gain/loss
    """
    for key, value in api_data_dict_updated.items():

        # create temp lists
        temp_list = []
        temp_list_bv = []
        temp_list_cv = []

        # add values to temp arrays
        for part_key, part_value in value.items():
            if part_key == 'book_value':
                for i in value[part_key]:
                    temp_list_bv.append(i)

            if part_key == 'current_value':
                for i in value[part_key]:
                    temp_list_cv.append(i)

        # create book value
        counter = 0
        for i in temp_list_bv:
            gain_loss = temp_list_cv[counter] - i
            temp_list.append(gain_loss)
            counter += 1

        api_data_dict_updated[key]['total_gain_loss'] = temp_list

    """
    Calculate dividend yield
    """
    for key, value in api_data_dict_updated.items():

        # create temp lists
        temp_list = []
        temp_list_price = []
        temp_list_div = []

        # add values to temp arrays
        for part_key, part_value in value.items():
            if part_key == 'latestPrice':
                for i in value[part_key]:
                    temp_list_price.append(i)

            if part_key == 'currentDividend':
                for i in value[part_key]:
                    temp_list_div.append(i)

        # create book value
        counter = 0
        for i in temp_list_price:
            divYield = temp_list_div[counter] / i
            temp_list.append(divYield)
            counter += 1

        api_data_dict_updated[key]['dividend_yield'] = temp_list

    api_data_dict_copy = copy.deepcopy(api_data_dict_updated)
    
    # create charts
    web_formatted_list_charts = create_charts(api_data_dict_copy)
    
    web_formatted_dict = format_web_output(api_data_dict_copy)
    rearranged_dict, rearranged_dict_web = rearrange_dictionary(api_data_dict_updated, web_formatted_dict)
    
    return rearranged_dict, rearranged_dict_web, web_formatted_list_charts


def format_web_output(analyzed_data_dict):
    """
    Function to perform simple formatting on data points for output
    to web based views such as placing comma's between long numbers,
    adding dollar/percent signs and rounding off to two decimal places.
    """

    text_headers = ['companyName', 'symbol', 'issueType', 'purchase_currency', 'exchange', 'industry', 'sector', 'adjustedDividendCurrency', 'divCurrency', 'divFrequency']
    currency_headers = ['latestPrice', 'current_value', 'total_gain_loss', 'change', 'week52High', 'week52Low', 'book_price', 'book_value', 'currentDividend', 'ytdDividendIncome']
    decimal_headers = ['peRatio', 'fx_USDCAD_purchase', 'fx_USDCAD_current']
    datetime_headers = ['purchase_date', 'divDate', 'exDivDate', 'divPaidDate']
    percent_headers = ['changePercent', 'ytdChange', 'dividend_yield']
    whole_headers = ['qty']
    large_whole_headers = ['marketCap']
    
    
    for key, value in analyzed_data_dict.items():

        # add values to temp arrays
        for part_key, part_value in value.items():
            
            # create temp lists
            temp_list = []              
                
            if (part_key in text_headers):
                for i in value[part_key]:
                    if i:
                        temp_list.append(i)
                    else:
                        temp_list.append("N/A")
            elif (part_key in currency_headers):
                for i in value[part_key]:
                    if i:
                        if i >= 0:
                            rounded_value = "${:,.2f}".format(i)
                            temp_list.append(rounded_value)
                        else:
                            rounded_value = "-${:,.2f}".format(-i)
                            temp_list.append(rounded_value)
                    else:
                        temp_list.append("N/A")
            elif (part_key in decimal_headers):
                for i in value[part_key]:
                    if i:
                        rounded_value = "{:-,.2f}".format(i)
                        temp_list.append(rounded_value)
                    else:
                        temp_list.append("N/A")
            elif (part_key in datetime_headers):
                for i in value[part_key]:
                    if i:
                        adjusted_date = i
                        temp_list.append(adjusted_date)
                    else:
                        temp_list.append("N/A")
            elif (part_key in percent_headers):
                for i in value[part_key]:
                    if i:
                        if i >= 0:
                            rounded_value = "{:,.2f}%".format(i*100)
                            temp_list.append(rounded_value)
                        else:
                            rounded_value = "-{:,.2f}%".format(-(i*100))
                            temp_list.append(rounded_value)
                    else:
                        temp_list.append("N/A")
            elif (part_key in whole_headers):
                for i in value[part_key]:
                    if i:
                        temp_list.append("{:,}".format(i))
                    else:
                        temp_list.append("N/A")
            elif (part_key in large_whole_headers):
                for i in value[part_key]:
                    if i:
                        temp_list.append("${:,}".format(i))
                    else:
                        temp_list.append("N/A")
            else:
                for i in value[part_key]:
                    temp_list.append(i)

            analyzed_data_dict[key][part_key] = temp_list
        
    return analyzed_data_dict


def rearrange_dictionary(api_data_dict, web_formatted_dict):
    """
    Function to reorder the dictionary prior to converting to dataframe.
    
    Parameters
    ----------
        api_data_dict : dict
            dictionary of the sheets (keys) and the associated data to fill the 
            rows as a dictionary where keys are header names and values are the
            row values.
    
    Returns
    -------
        api_data_dict_rearranged : dict
            dictionary rearranged for properly ordering output.
    """
    
    ordered_dict = dict()
    web_ordered_dict = dict()
    
    ordered_headers = ['companyName', 'symbol', 'qty', 'latestPrice', 'current_value', 'total_gain_loss', 'change', 'changePercent', 'marketCap', 'peRatio', 'week52High', 'week52Low', 'ytdChange', 'issueType',  'book_price', 'book_value', 'purchase_date', 'purchase_currency', 'exchange', 'industry', 'sector', 'currentDividend','ytdDividendIncome', 'adjustedDividendCurrency', 'divCurrency', 'divFrequency', 'dividend_yield', 'divDate', 'exDivDate', 'divPaidDate',  'fx_USDCAD_purchase', 'fx_USDCAD_current']
    ordered_headers_clarified = ['Company Name', 'Ticker', 'Quantity', 'Current Price', 'Current Value', 'Total Gain/Loss', '24hr Change $', '24hr Change %', 'Market Capitalization', 'PE Ratio', '52 Week High', '52 Week Low', 'YTD Change', 'Issue Type', 'Book Price', 'Book Value', 'Purchase Date', 'Purchase Currency', 'Company\'s Home Exchange', 'Industry', 'Sector', 'Current Dividend', 'YTD Dividend Income', 'Adjusted Dividend Currency', 'Dividend Paid Currency', 'Dividend Frequency', 'Dividend Yield', 'Dividend Date', 'Ex-Dividend Date', 'Dividend Payout Date',  'FX USD/CAD Purchase Date', 'FX USD/CAD Current']


    # reorder dictionary for data purposes
    for key, value in api_data_dict.items():
        
        ordered_values = dict()
        
        for s in ordered_headers_clarified:
            ordered_values[s] = []

        counter = 0
        
        for i in ordered_headers_clarified:
            ordered_values[i] = api_data_dict[key][ordered_headers[counter]]
            counter += 1
        
        ordered_dict[key] = ordered_values
        
    # reorder dictionary for web purposes
    for key, value in web_formatted_dict.items():
        
        ordered_values = dict()
        
        for s in ordered_headers_clarified:
            ordered_values[s] = []

        counter = 0
        
        for i in ordered_headers_clarified:
            ordered_values[i] = web_formatted_dict[key][ordered_headers[counter]]
            counter += 1
        
        web_ordered_dict[key] = ordered_values
    
    return ordered_dict, web_ordered_dict


def create_charts(api_data_dict):
    """
    A function to create charts for output to the Excel file. The following
    charts are created:
        1. Pie chart - US/CAD asset by value
        2. Pie chart - US/CAD sector allocation by value
        3. Pie chart - US/CAD sector allocation by dividend income
        4. 
        5. 
        6. 
    
    """
    
    charts_by_acct = dict()
    
    for key, value in api_data_dict.items():
        
        # assign empty dictionary to key
        charts_by_acct[key] = dict()
        
        temp_list_symbol = []
        temp_list_current_value = []
        temp_list_book_value = []
        temp_list_purchase_currency = []
        temp_list_sector = []
        temp_list_divinc = []
        

        # add values to temp arrays
        for part_key, part_value in value.items():
            if part_key == 'symbol':
                for i in value[part_key]:
                    temp_list_symbol.append(i)

            if part_key == 'current_value':
                for i in value[part_key]:
                    temp_list_current_value.append(i)
                    
            if part_key == 'book_value':
                for i in value[part_key]:
                    temp_list_book_value.append(i)
            
            if part_key == 'purchase_currency':
                for i in value[part_key]:
                    temp_list_purchase_currency.append(i)
            
            if part_key == 'sector':
                for i in value[part_key]:
                    temp_list_sector.append(i)
                    
            if part_key == 'ytdDividendIncome':
                for i in value[part_key]:
                    temp_list_divinc.append(i)
    
        # create lists to separate by currency
        us_list_symbol = []
        us_list_current_value = []
        us_list_book_value = []
        us_list_sector = []
        us_list_divinc = []
        cad_list_symbol = []
        cad_list_current_value = []
        cad_list_book_value = []
        cad_list_sector = []
        cad_list_divinc = []
        
        counter = 0;
        for i in temp_list_purchase_currency:
            if (i == "USD"):
                us_list_symbol.append(temp_list_symbol[counter])
                us_list_current_value.append(temp_list_current_value[counter])
                us_list_book_value.append(temp_list_book_value[counter])
                us_list_sector.append(temp_list_sector[counter])
                us_list_divinc.append(temp_list_divinc[counter])
                
            elif (i == "CAD"):
                cad_list_symbol.append(temp_list_symbol[counter])
                cad_list_current_value.append(temp_list_current_value[counter])
                cad_list_book_value.append(temp_list_book_value[counter])
                cad_list_sector.append(temp_list_sector[counter])
                cad_list_divinc.append(temp_list_divinc[counter])
            
            counter += 1

        # create USD charts
        if us_list_symbol:
        
            # create US current value by asset pie chart
            df = pd.DataFrame(
                    data = {'symbol': us_list_symbol, 'value': us_list_current_value}
                    ).sort_values('value', ascending = False)
            df = df.groupby(['symbol'])['value'].sum()
            print(df)
            fig = plt.figure(figsize = (3,3))
            df.plot(kind = 'pie', y = 'value', autopct='%1.1f%%', labels = list(df.index.values), startangle=90, legend = False, fontsize = 8)
            plt.axes().set_ylabel('')
            plt.tight_layout()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            charts_by_acct[key]['Current Value by Asset (USD)'] = uri
            plt.clf()
            
            # create US sector allocation by value pie chart
            df = pd.DataFrame(
                    data = {'sector': us_list_sector, 'value': us_list_current_value}
                    ).sort_values('value', ascending = False)
            df = df.groupby(['sector'])['value'].sum()
            print(df)
            fig = plt.figure(figsize = (3,3))
            df.plot(kind = 'pie', y = 'value', autopct='%1.1f%%', labels = list(df.index.values), startangle=90, legend = False, fontsize = 8)
            plt.axes().set_ylabel('')
            #plt.legend(loc="lower center")
            plt.tight_layout()
            #plt.imshow(fig, cmap=plt.cm.get_cmap('cubehelix', 6))
            #plt.colorbar()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            charts_by_acct[key]['Value by Sector (USD)'] = uri
            plt.clf()
            
            # create US sector allocation by dividend income pie chart
            df = pd.DataFrame(
                    data = {'sector': us_list_sector, 'value': us_list_divinc}
                    ).sort_values('value', ascending = False)
            df = df.groupby(['sector'])['value'].sum()
            
            print(df)
            
            fig = plt.figure(figsize = (3,3))
            df.plot(kind = 'pie', y = 'value', autopct='%1.1f%%', labels = list(df.index.values), startangle=90, legend = False, fontsize = 8)
            plt.axes().set_ylabel('')
            plt.tight_layout()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            charts_by_acct[key]['Dividend Income by Sector (USD)'] = uri
            plt.clf()
            
        # create CAD charts
        if cad_list_symbol:
        
            # create CAD current value by asset pie chart           
            df = pd.DataFrame(
                    data = {'symbol': cad_list_symbol, 'value': cad_list_current_value}
                    ).sort_values('value', ascending = False)
            df = df.groupby(['symbol'])['value'].sum()
            
            print(df)
            
            fig = plt.figure(figsize = (3,3))
            df.plot(kind = 'pie', y = 'value', autopct='%1.1f%%', labels = list(df.index.values), startangle=90, legend = False, fontsize = 8)
            plt.axes().set_ylabel('')
            plt.tight_layout()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            charts_by_acct[key]['Current Value by Asset (CAD)'] = uri
            plt.clf()
            
            # create US sector allocation by value pie chart
            df = pd.DataFrame(
                    data = {'sector': cad_list_sector, 'value': cad_list_current_value}
                    ).sort_values('value', ascending = False)
            df = df.groupby(['sector'])['value'].sum()
            
            print(df)
            
            fig = plt.figure(figsize = (3,3))
            df.plot(kind = 'pie', y = 'value', autopct='%1.1f%%', labels = list(df.index.values), startangle=90, legend = False, fontsize = 8)
            plt.axes().set_ylabel('')
            plt.tight_layout()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            charts_by_acct[key]['Value by Sector (CAD)'] = uri
            plt.clf()
            
            # create US sector allocation by dividend income pie chart
            df = pd.DataFrame(
                    data = {'sector': cad_list_sector, 'value': cad_list_divinc}
                    ).sort_values('value', ascending = False)
            df = df.groupby(['sector'])['value'].sum()
            
            print(df)
            
            fig = plt.figure(figsize = (3,3))
            df.plot(kind = 'pie', y = 'value', autopct='%1.1f%%', labels = list(df.index.values), startangle=90, legend = False, fontsize = 8)
            plt.axes().set_ylabel('')
            plt.tight_layout()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            charts_by_acct[key]['Dividend Income by Sector (CAD)'] = uri
            plt.clf()       
        
    
    #print(charts_by_acct)
    return charts_by_acct
    
    
    


if __name__ == "__main__":
    pass
