# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:50:51 2019

@author: sdtaylor
"""

# imports
import pandas as pd
import copy
from Analyze import get_current_holdings
from Analyze import get_api_data
from Analyze import perform_data_analysis
from Analyze import convert_to_dataframe
from Analyze import save_xlsx


class driver():

    def run_analytics(excel_file, iex_key):
        """
        Base function to call required helper functions and modules to get
        API Data from the IEX Cloud API and output an Excel file.
        
        """
        
        # IEX Cloud authorization token
        auth_key_IEX = iex_key
        
        # create data frame of stock holdings
        print("\nGathering current holdings ...")
        current_holdings_df, current_holdings_symbols =  get_current_holdings.get_holdings_data(excel_file)
        print("\nCurrent holdings successfully gathered!")
        
        # get data via api and return dictionary
        print("\nObtaining data from API's ...")
        api_data_dict = get_api_data.get_data(current_holdings_symbols, current_holdings_df, auth_key_IEX)
        print("API data successfully gathered!")
        
        # perform analysis on the data & format for web output
        print("\nAnalyzing data ...")
        analyzed_data_dict, analyzed_data_dict_web, analyzed_charts_list = perform_data_analysis.calculate_totals(api_data_dict)
        print("Data successfully analyzed!")
        
        # convert to dataframe 
        print("\nPerforming conversions on data ...")
        analyzed_data_dict = copy.deepcopy(analyzed_data_dict)
        analyzed_data_dict_df = convert_to_dataframe.perform_conversion(analyzed_data_dict)
        print("Data conversions completed!")
        
        # save data to Excel
        print("\nWriting data to Excel ...")
        save_xlsx.write_xlsx(analyzed_data_dict_df)  
        print("Excel formatting completed!")
        
        return analyzed_data_dict_df, analyzed_data_dict_web, analyzed_charts_list
        

# run program as driver
if __name__ == "__main__":
    driver.run_analytics()
