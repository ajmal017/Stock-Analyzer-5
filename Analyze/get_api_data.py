# -*- coding: utf-8 -*-
"""
A file with helper functions to get the associated data from the IEX Cloud API, yfinance API and the
forex_python API and combine.

Created on Mon Jul 15 10:01:37 2019

@author: sdtaylor
"""

# library imports
import datetime
import copy
import pandas as pd
import requests
import yfinance as yf
from forex_python.converter import CurrencyRates


def get_data(current_stock_symbols, current_holdings_df, auth_key):
    """
    Function to get data from the IEX Cloud API, Yahoo Finance and 
    forex_python, returning a dictionary of the combined data.
    
    Parameters
    ----------
    current_stock_symbols : dict
        dictionary of the Excel sheets (keys) and the associated stock symbols appearing on that sheet (values).
    current_holdings_df : dict
        dictionary of the Excel sheets (keys) and the associated data rows appearing on that sheet (values). The values
        are key:value pairs, with the key being the column header and the value being the corresponding data for that
        row.
    auth_key : str
        authorization key for the IEX Cloud API.

    Returns
    -------
    combined_data_dict : dictionary
        dictionary with the appropriate Excel tabs and the associated requested data.
    """
    
    # initialize dictionary formatted for conversion to dataframe
    api_data_return = dict()
    api_data_return_div = dict()

    headers_df = ['companyName', 'symbol', 'latestPrice', 'exchange', 'fx_USDCAD_current', 'industry', 'sector', 'change', 'changePercent', 'marketCap', 'peRatio', 'week52High', 'week52Low', 'ytdChange', 'issueType', 'divDate', 'exDivDate', 'divPaidDate', 'currentDividend']
    
    headers_div = ['amount', 'currency', 'frequency']  
    
    # add current stock data to the appropriate list
    for key, value in current_stock_symbols.items():
        
        api_data_df = dict()
        api_data_div = dict()
        
        for s in headers_df:
            api_data_df[s] = []
            
        for s in headers_div:
            api_data_div[s] = []
        
        for symbol in value:

            # QUOTE
            # Gets quote data: symbol, companyName, change, changePercent, latestPrice, marketCap, peRatio, week52High, week52Low, ytdChange
            quote_json = "https://cloud.iexapis.com/beta/stock/" + symbol.lower() + "/quote?token=" + auth_key
            quote_response_jsonp = requests.get(quote_json)
            response_quote = quote_response_jsonp.json()
            headers_curr = ['symbol', 'companyName', 'change', 'changePercent', 'latestPrice', 'marketCap', 'peRatio', 'week52High', 'week52Low', 'ytdChange']
            
            print("Printing: quote_response_jsonp")
            print(quote_response_jsonp.content)
            print("Printing: response_quote")
            print(response_quote)
            print("------------------------------------------")
            
            # add data to dictionary api_data_df
            for j in headers_curr:
                for col, data in response_quote.items():
                    if j == col:
                        api_data_df[j].append(data)
                        break

            # COMPANY
            # Gets the exchange, industry, sector, issueType
            company_json = "https://cloud.iexapis.com/beta/stock/" + symbol.lower() + "/company?token=" + auth_key
            company_response_jsonp = requests.get(company_json)
            response_comp = company_response_jsonp.json()
            headers_curr = ['exchange', 'industry', 'sector', 'issueType']
            
            # add data to dictionary api_data_df
            for j in headers_curr:
                for col, data in response_comp.items():
                    if j == col:
                        api_data_df[j].append(data)

            # DIVIDEND YTD
            # Gets dividend data: amount, currency, frequency for YTD dividends from IEX
            dividends_json_ytd = "https://cloud.iexapis.com/beta/stock/" + symbol.lower() + "/dividends/ytd?token=" + auth_key
            dividends_response_jsonp_ytd = requests.get(dividends_json_ytd)
            response_divytd = dividends_response_jsonp_ytd.json()
            headers_curr = ['amount', 'currency', 'frequency']      
            
            # add data to dictionary api_data_df
            for j in headers_curr:
                temp_list = []
                for k in response_divytd:
                    for col, data in k.items():
                        if j == col:
                            temp_list.append(data)
                api_data_div[j].append(temp_list)

            # DIVIDEND NEXT
            # Gets next dividend date if declared, else, gets the most recent dividend date. Additionally, gets the
            # ex-dividend data and the date the dividend was/will be paid.

            headers_curr = ['divDate', 'exDivDate', 'divPaidDate', 'currentDividend']

            share_name = yf.Ticker(symbol)

            dividends = share_name.dividends
            dividends = pd.to_numeric(dividends.tail(1))
            dividends = dividends.to_frame()
            dividends = dividends.reset_index()

            # try to get dividends, fail nicely if no dividends are found.
            try:
                div_date = dividends.iloc[-1]['Date']
                current_dividend = dividends.iloc[-1]['Dividends']
                ex_div_date = div_date - pd.Timedelta(days=1)
                info = share_name.info
                div_date_paid = pd.Timestamp(datetime.datetime.fromtimestamp(info['dividendDate']))

            except IndexError as e:
                div_date = ''
                current_dividend = 0
                ex_div_date = ''
                div_date_paid = ''

            # add data to dictionary api_data_df
            api_data_df['divDate'].append(div_date)
            api_data_df['exDivDate'].append(ex_div_date)
            api_data_df['divPaidDate'].append(div_date_paid)
            api_data_df['currentDividend'].append(current_dividend)

            # FX RATES
            # Gets the USD/CAD FX rate as at today.
            USD_CAD_now = CurrencyRates()
            USD_CAD_now = USD_CAD_now.get_rate('USD', 'CAD')
            api_data_df['fx_USDCAD_current'].append(USD_CAD_now)

        api_data_return[key] = api_data_df
        api_data_return_div[key] = api_data_div

    combined_data_temp = combine_data(current_holdings_df, api_data_return)
    combined_data_temp = sum_ytd_divs(combined_data_temp, api_data_return_div, headers_div)
    combined_data_dict = copy.deepcopy(combined_data_temp)
    
    #print("Printing: combined_data_dict")
    #print(combined_data_dict)
    #print()

    return combined_data_dict


def combine_data(current_holdings_df, api_data_return):
    """
    Function to combine the data for the book values in the original Excel workbook (holdings.xlsx) and
    the data from the IEX Cloud API, Yahoo Finance API and Forex API.

    Parameters
    ----------
    current_holdings_df : dict
        dictionary of the Excel sheets (keys) and the associated data rows appearing on that sheet (values). The values
        are key:value pairs, with the key being the column header and the value being the corresponding data for that
        row.
    api_return_data : dict
        dictionary of the Excel sheets (keys) and the associated data rows appearing on that sheet (values). The values
        are key:value pairs, with the key being the column header and the value being the corresponding data for that
        row.

    Returns
    -------
    combined_holdings_dict : dict
        dictionary of the combined data.
    """

    combined_holdings_dict = api_data_return
    
    for keys, values in current_holdings_df.items():

        for key_part, value_part in values.items():
            temp = []
            if key_part == 'purchase_date' or key_part == 'book_price' or key_part == 'purchase_currency' or key_part == 'qty':
                
                for i in value_part.values():
                    temp.append(i)
                
                combined_holdings_dict[keys][key_part] = temp
                
                if key_part == 'purchase_date':
                    temp_FX = []

                    for i in value_part.values():
                        date_obj = i.to_pydatetime()
                        USD_CAD_purchase = CurrencyRates()
                        USD_CAD_purchase = USD_CAD_purchase.get_rate('USD', 'CAD', date_obj)
                        temp_FX.append(USD_CAD_purchase)
                    
                    combined_holdings_dict[keys]['fx_USDCAD_purchase'] = temp_FX
                
    return combined_holdings_dict
    
def sum_ytd_divs(combined_api_data, div_api_data, headers):
    """
    Function to sum up year to date amounts for dividends retrieved from the
    IEX Cloud API, and call a helper function to combine this into the main
    data container.

    Parameters
    ----------
    combined_api_data : dict
        dictionary of the Excel sheets (keys) and the associated data rows appearing on that sheet (values). The values
        are key:value pairs, with the key being the column header and the value being the corresponding data for that
        row.
    div_api_data : dict
        dictionary of the Excel sheets (keys) and the associated data rows appearing on that sheet (values). The values
        are key:value pairs, with the key being the column header and the value being the corresponding data for that
        row.
    headers : list
        list of the headers of the dividend columns.

    Returns
    -------
    combined_data_dict : dictionary
        dictionary of the combined data.
    """
    
    div_data = div_api_data
    div_data_new = dict()
    
    # sum up YTD dividends for conversion to dataframe
    for key, value in div_data.items():
        
        div_data_temp = dict()
        
        for s in headers:
            div_data_temp[s] = []
        
        for key_part, value_part in value.items():
            if key_part == "amount":
                
                # sum up YTD amount
                for i in value_part:
                    value_new = 0
                    if len(i) != 0:
                        for j in i:
                            value_new += j
                    
                    # add to dictionary list item
                    div_data_temp[key_part].append(value_new)
            
            elif key_part == "frequency":

                # get most recently reported frequency
                for i in value_part:
                    if len(i) == 0:
                        value_new = ""
                    else:
                        index = len(i) - 1
                        value_new = i[index]
                    
                    # add to dictionary list item
                    div_data_temp[key_part].append(value_new)
                
            elif key_part == "currency":
 
                # get currency (same for all)
                for i in value_part:
                    if len(i) == 0:
                        value_new = ""
                    else:
                        index = len(i) - 1
                        value_new = i[index]
                    
                    # add sheet line value to dictionary list
                    div_data_temp[key_part].append(value_new)                    
        
        # add sheet value to dictionary
        div_data_new[key] = div_data_temp 
    
    # update dividend headers for clarity 
    for key, value in div_data_new.items():
        value["ytdDividendIncome"] = value.pop("amount")
        value["divFrequency"] = value.pop("frequency")
        value["divCurrency"] = value.pop("currency")
    
    # combine again to include dividend values
    combined_data_dict = combine_divs(div_data_new, combined_api_data)

    return combined_data_dict

    
def combine_divs(div_data, current_data):
    """
    Helper function to combine the data from the dividend information via the IEX Cloud API, which required additional
    processing in the sum_ytd_divs function.
    
    div_data : dict
        dictionary of the dividend data with sheet names (key) and the associated values as key:value pairs, where the
        key is the column name and tbe value is the row value.
    current_data : dict
        dictionary of the data of which the div_data will be added to, where sheet names (key) and the associated
        values as key:value pairs, where the key is the column name and tbe value is the row value.

    Returns
    -------
    combined_holdings_dict : dict
        dictionary of the combined data, where sheet names (key) and the associated values as key:value pairs, where
        the key is the column name and tbe value is the row value.
    """
    
    combined_holdings_dict = current_data
    
    for keys, values in div_data.items():
        
        for key_part, value_part in values.items():
            temp = []
            if key_part == 'ytdDividendIncome' or key_part == 'divFrequency' or key_part == 'divCurrency':
                
                for i in value_part:
                    temp.append(i)
                
                combined_holdings_dict[keys][key_part] = temp

    return combined_holdings_dict 
