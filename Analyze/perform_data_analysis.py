# -*- coding: utf-8 -*-
"""
A module to perform financial analysis on the API Data gathered.

Created on Wed Jul 17 11:35:23 2019

@author: sdtaylor
"""

import copy


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
        temp_list_adjdivcurr = []
        temp_list_fx = []
        temp_list_curr = []
        temp_list_ytddiv = []
        temp_list_divcurr = []

        # add values to temp arrays
        for part_key, part_value in value.items():
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

        api_data_dict_updated[key]['ytdDividendIncome'] = temp_list
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

    rearranged_dict = rearrange_dictionary(api_data_dict_updated)
    
    return rearranged_dict


def rearrange_dictionary(api_data_dict):
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
    
    ordered_headers = ['companyName', 'symbol', 'qty', 'latestPrice', 'current_value', 'total_gain_loss', 'change', 'changePercent', 'marketCap', 'peRatio', 'week52High', 'week52Low', 'ytdChange', 'issueType',  'book_price', 'book_value', 'purchase_date', 'purchase_currency', 'exchange', 'industry', 'sector', 'currentDividend','ytdDividendIncome', 'adjustedDividendCurrency', 'divCurrency', 'divFrequency', 'dividend_yield', 'divDate', 'exDivDate', 'divPaidDate',  'fx_USDCAD_purchase', 'fx_USDCAD_current']
    ordered_headers_clarified = ['Company Name', 'Ticker', 'Quantity', 'Current Price', 'Current Value', 'Total Gain/Loss', '24hr Change $', '24hr Change %', 'Market Capitalization', 'PE Ratio', '52 Week High', '52 Week Low', 'YTD Change', 'Issue Type', 'Book Price', 'Book Value', 'Purchase Date', 'Purchase Currency', 'Company\'s Home Exchange', 'Industry', 'Sector', 'Current Dividend', 'YTD Dividend Income', 'Adjusted Dividend Currency', 'Dividend Paid Currency', 'Dividend Frequency', 'Dividend Yield', 'Dividend Date', 'Ex-Dividend Date', 'Dividend Payout Date',  'FX USD/CAD Purchase Date', 'FX USD/CAD Current']


    # add current stock data to the appropriate list
    for key, value in api_data_dict.items():
        
        ordered_values = dict()
        
        for s in ordered_headers_clarified:
            ordered_values[s] = []

        counter = 0
        
        for i in ordered_headers_clarified:
            ordered_values[i] = api_data_dict[key][ordered_headers[counter]]
            counter += 1
        
        ordered_dict[key] = ordered_values
    
    return ordered_dict


def create_charts():
    """
    A function to create charts for output to the Excel file.
    
    """
    
    pass



def testing_program():
    pass


if __name__ == "__main__":
    testing_program()
