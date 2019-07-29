# -*- coding: utf-8 -*-
"""
A module to convert dictionary items to Pandas Dataframes.

Created on Fri Jul 19 09:55:00 2019

@author: sdtaylor
"""


import pandas as pd

def perform_conversion(dictionary_to_convert):
    """
    Function to convert the dictionary values, formatted as dictionaries
    to Pandas Dataframes.
    
    Parameters
    ----------
        dictionary_to_convert : dict
            dictionary of the sheets (keys) and the associated data to fill the 
            rows as a dictionary where keys are header names and values are the
            row values.
    
    Returns
    -------
        dictionary_converted : dict
            dictionary where keys are the sheet names of the excel sheet and
            the values are Pandas Dataframes.
    """
    
    # print dictionary to command line
    print(dictionary_to_convert)
    
    dictionary_converted = dict()
    
    # convert to dataframe for export to excel
    for key, value in dictionary_to_convert.items():
        dictionary_converted[key] = pd.DataFrame.from_dict(value)
    
    return dictionary_converted
