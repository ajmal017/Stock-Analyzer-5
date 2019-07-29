# -*- coding: utf-8 -*-
"""
A file with helper functions to create and Excel file with the associated
analysis previously performed.

Created on Fri Jul 12 12:03:48 2019Created on Mon Jul 15 10:01:37 2019

@author: sdtaylor
"""

# imports
import pandas as pd
import xlsxwriter
import itertools
import os
from datetime import datetime
from django.conf import settings



def write_xlsx(combined_api_data):
    """
    A function to write the data to an Excel file, by sheet.
    
    Parameters
    ----------
    combined_api_data : dict
        Data as a dictionary, where the keys are the tab names and the values are DataFrames of which will
        be added as the data in each tab.
    """
    
    api_data_df = combined_api_data

    """
    ADJUST HEADING NAME FOR EXPORT TO EXCEL
    """


    # create Excel file on Desktop
    #new_file_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', "stock_data.xlsx")
    
    # create Excel file in media folder (strip first slash off)
    new_file_path = settings.MEDIA_URL[1:] + 'stock_data.xlsx'
    writer = pd.ExcelWriter(new_file_path, engine='xlsxwriter', datetime_format='dd/mm/yy')
    
    # create list of sheet names
    sheets_xlsx = []
    num_rows_by_sheet = []
    
    for key, value in api_data_df.items():
        value.to_excel(writer, sheet_name=key)
        sheets_xlsx.append(key)
        num_rows_by_sheet.append(len(value))
        
    # format Excel file
    format_xlsx(writer, sheets_xlsx, num_rows_by_sheet)
    
    writer.save()

def format_xlsx(writer, sheets_xlsx, num_rows):
    """
    A function to format the Excel document.
    
    """
    
    # get xlsxwriter workbook object for formatting
    workbook = writer.book
    
    # get the xlsx worksheet objects for formatting
    worksheets = []
    for i in sheets_xlsx:
        worksheets.append(writer.sheets[i])
    
    # create formats
    bolded_text = workbook.add_format({'bold': True})
    whole_nums = workbook.add_format({'num_format': '#,##0.00'})
    currencies = workbook.add_format({'num_format': '$#,##0.00'})
    percentages = workbook.add_format({'num_format': '0.00%'})
    fx = workbook.add_format({'num_format': '#0.0000000'})                                         
                                   
    # format worksheets
    for i in worksheets:
        i.set_column('B:B', 30, bolded_text)
        i.set_column('D:D', 9, whole_nums)
        i.set_column('E:E', 15, currencies)
        i.set_column('F:F', 15, currencies)
        i.set_column('G:G', 15, currencies)
        i.set_column('H:H', 15, currencies)
        i.set_column('I:I', 15, percentages)
        i.set_column('J:J', 20, currencies)
        i.set_column('L:L', 12, currencies)
        i.set_column('M:M', 12, currencies)
        i.set_column('N:N', 12, percentages)
        i.set_column('O:O', 12)
        i.set_column('P:P', 12, currencies)
        i.set_column('Q:Q', 12, currencies)
        i.set_column('R:R', 15)
        i.set_column('S:S', 15)
        i.set_column('T:T', 25)
        i.set_column('U:U', 25)
        i.set_column('V:V', 25)
        i.set_column('W:W', 15, currencies)
        i.set_column('X:X', 15, currencies)
        i.set_column('Y:Y', 15)
        i.set_column('Z:Z', 15)
        i.set_column('AA:AA', 15)
        i.set_column('AB:AB', 18, percentages)
        i.set_column('AC:AC', 18)
        i.set_column('AD:AD', 18)
        i.set_column('AE:AE', 18)
        i.set_column('AF:AF', 18, fx)
        i.set_column('AG:AG', 18, fx)
    
    # conditonally format worksheets
    counter = 0
    for i in worksheets:
        
        # colour code gain/loss
        i.conditional_format('G2:G' + str(1 + num_rows[counter]), {'type': '3_color_scale'})
        
        # add icon to 24hr change
        i.conditional_format('H2:H' + str(1 + num_rows[counter]), {'type': 'icon_set',
                                     'icon_style': '3_arrows',
                                     'icons': [{'criteria': '>=', 'type': 'number', 'value': 0.00001}, 
                                               {'criteria': '>=', 'type': 'number', 'value': -0.00001}]})
        i.conditional_format('I2:I' + str(1 + num_rows[counter]), {'type': 'icon_set',
                                     'icon_style': '3_arrows',
                                     'icons': [{'criteria': '>=', 'type': 'number', 'value': 0.00001}, 
                                               {'criteria': '>=', 'type': 'number', 'value': -0.00001}]})
    
    
    # format Excel
    print("Formatting Excel ...")


def add_charts():
    """
    A function to add charts to the Excel document.
    
    """
    
    # add charts to Excel
    print("Adding charts to Excel ...")

