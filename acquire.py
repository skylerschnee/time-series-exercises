#!/usr/bin/env python
# coding: utf-8

# In[35]:


import requests
import numpy as np
import pandas as pd
import math

def get_api_resources(root_url):
    '''
    get_api_resources takes in a root url, and will parse the available
    resources within and display them to the user
    '''
    response = requests.get(root_url)
    resources = response.json()
    for key, value in resources.items():
        print(f'{key}: {value}\n')

def get_api_df(url):
    '''
    get_api_df takes in a url for an api, uses a for loop to go through
    each page and create a df from the concatenated data from each page,
    then returns the df
    '''
    response = requests.get(url)

    data = response.json()

    df = pd.DataFrame(data['results'])

    response = requests.get(url)
    data = response.json()

    data_len = data['count']
    next_page = data['next']
    number_of_results = len(data['results'])
    max_page = math.ceil(data_len / number_of_results)

    df = pd.DataFrame(data['results'])

    for page in range(2, max_page+1):
        response = requests.get(next_page)
        data = response.json()
        df = pd.concat([df, pd.DataFrame(data['results'])])
        next_page = data['next']

    df.reset_index(drop=True, inplace=True)
    
    return df

def get_germany_ops_data():
    '''
    get_germany_ops_data reads the .csv from the source website,
    produces a df from that data, and returns the df
    '''
    url='https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
    df = pd.read_csv(url)
    return df
    

