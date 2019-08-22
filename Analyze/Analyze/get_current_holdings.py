# -*- coding: utf-8 -*-
"""
A function to get the currently held stocks, along with purchase information from the provided Excel sheet.

Created on Mon Jul 15 10:01:37 2019

@author: sdtaylor
"""

import pandas as pd
import os


def get_holdings_data(excel_file):
    """
    Function to create a dictionary of current holdings by sheet per the 
    holdings.xlsx file located on the desktop.

    Returns
    -------
        dictionary
            a dictionary containing key of the sheet name
            and value of the current holding data as a dictionary.
        dictionary
            a dictionary containing key of the sheet name
            and value of the ticker symbols as a list.
    
    """
    
    # find filepath of holdings.xlsx
    #current_holdings_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', "holdings.xlsx")
    
    # initialize list variable for holdings.xlsx tabs
    current_holdings_all = dict()
    
    # get currennt stock holdings from holdings.xls on desktop
    #print("\nOpening: " + current_holdings_path + " ...")
    xls = pd.ExcelFile(excel_file)
    #print("Successfully Opened: " + current_holdings_path)
    
    # get tab names
    xls_tabs = xls.sheet_names
    # print("\nTabs: " + str(xls_tabs) + "\n")
    
    # add dictionary items to current_holdings_all
    for i in xls_tabs:
        tab_data_df = pd.read_excel(excel_file, sheet_name=i)
        current_holdings_all[i] = tab_data_df.to_dict()

    current_holdings_symbols = get_holdings_symbols(current_holdings_all)
    return current_holdings_all, current_holdings_symbols


def get_holdings_symbols(current_holdings_all_data):
    """
    Helper function to create a dictionary of current ticker symbols by sheet per the
    holdings.xlsx file located on the desktop.

    Parameters
    ----------
    current_holdings_all_data : dict
        a dictionary containing key of the sheet name and value of the current holdings data as a dictionary.

    Returns
    -------
        current_holdings_symbols : dictionary
            a dictionary containing key of the sheet name and value of the currently held stock symbols as a list.
    
    """

    # initialize dict variable for holdings.xlsx tabs
    current_holdings_symbols = dict()

    # loop through and create new dictionary of sheet name and ticker symbol
    for key, value in current_holdings_all_data.items():
        
        temp = []
        for part_key, value_part in value.items():
            
            if part_key == 'symbol':
                
                for j in value_part.values():
                    temp.append(j)
                    
        current_holdings_symbols[key] = temp

    return current_holdings_symbols


# for testing purposes
if __name__ == "__main__":
    get_holdings_data()
