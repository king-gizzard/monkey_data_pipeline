import pandas as pd
import os

#read filenames in directories, return list.
def file_list():
    path = os.path.join(os.pardir,'data','raw')
    files = []
    for folder in os.listdir(path):
        files += os.listdir(os.path.join(path,folder))
    return(files)

def untangle(df,col_name):
    col = df[col_name].str.split(' ').apply(pd.Series,1).stack()
    col.index = col.index.droplevel(-1)
    col.name = col_name
    del(df[col_name])
    return(df.join(col))
#    return(df.insert(i+1,col))

def get_or_make_csv(path,head):
    #load progress on which files are already detangled
    if os.path.exists(path):
        p = pd.read_csv(path)
    #or crete new if none found
    else:
        p = pd.DataFrame(columns=head)
    return(p)

#append new row to progress.csv and rewrite the latter
def update_csv(df,path,row):
    df.loc[len(df)] = row
    df.to_csv(path,index=False)

def get_id_list(csv_path):
    #read a support file
    data = pd.read_csv(csv_path)#os.path.join(os.pardir,'misc_files',csv_name))
    #make a list from the id column and return that
    return(list(data['id']))

def get_file_path(filename):
    #reverse engineer dir name from file name :/
    d = filename[:10]
    #path in data/raw
    return(os.path.join(os.pardir,'data','raw',d,filename))

#find out wether or not xlsx has a Rect sheet
#does not check for RECT<n> though, might be useful to.
def has_rect_sheet(path):
    df = pd.read_excel(path,sheet_name=None)
    if 'Rect' in df.keys():
        return(True)
    else:
        return(False)

#def write_error_line():
