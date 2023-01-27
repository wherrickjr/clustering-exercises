import pandas as pd
import numpy as np
import env
import os

def nulvals(df):
    loop = list(range(0,len(df.axes[1])))
    adf = []
    for i in loop:
        x = df.iloc[:, i].isna().sum()
        adf.append(x)
    cols = df.columns.values
    fjf = []
    for i in adf:
        x = i / len(df.axes[0])
        fjf.append(x)
    alltogether = pd.DataFrame({'column_name': cols, 'number_of_nulls': adf, 'percent_null': fjf})
    return alltogether


def drops(df, thresh1, thresh2):
    loop = list(range(0,len(df.axes[1])))
    adf = []
    for i in loop:
        x = df.iloc[:, i].isna().sum()
        adf.append(x)
    fjf = []
    for i in adf:
        x = i / len(df.axes[0])
        fjf.append(x)
    indices = np.array(fjf)
    indices2 = np.where(indices > thresh1)[0]
    df = df.drop(df.columns[indices2], axis = 1)
    
    ddd = []
    x = df.isnull().sum(axis = 1)
    for i in x:
        you = i / len(x)
        ddd.append(you)
    indices3 = np.array(ddd)
    indices4 = np.where(indices > thresh2)[0]
    df = df.drop(indices4)
    return df
# function that takes removes all columns that have more that 60% nulls and then rows that have
# more than 75% nulls

def get_connection(db, user=env.username, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


def get_zillow_data(query):
    filename = 'zillow.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        df = pd.read_sql(query, get_connection('zillow'))
        df.to_csv(filename)
        return df