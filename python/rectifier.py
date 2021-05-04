import pandas as pd
import os
from pipeline_utils import *

#HARDCODE - config options, kinda ------------------------------------
#
#value to 'fillna' in Actor/Action/Receiver
#used/searched also by error.py
empty_cell = 'none'
#name of sheet with detangled data
new_sheet = 'Rect'
#make debug print show entire frame
pd.set_option('display.max_rows', None)
#progress_csv_path = os.path.join(os.pardir,'misc_files','progress_list.csv')
monkey_csv_path = os.path.join(os.pardir,'misc_files','monkey_list.csv')
action_csv_path = os.path.join(os.pardir,'misc_files','action_list.csv')
mod_csv_path = os.path.join(os.pardir,'misc_files','mod_list.csv')
protocols_csv_path = os.path.join(os.pardir,'misc_files','protocols_list.csv')
#
#---------------------------------------------------------------------

#get a csv of already seen files and their statueses
#prog = get_or_make_csv(progress_csv_path,['file','status'])
focal_info = get_or_make_csv(protocols_csv_path,['file','date','time','focal','duration'])
#make list of files in raw
raw_files = file_list()
#get 'support files' lists
monkey_list = get_id_list(monkey_csv_path)#'monkey_list.csv')
action_list = get_id_list(action_csv_path)#'action_list.csv')
mod_list    = get_id_list(mod_csv_path)#'mod_list.csv')
#make list of difference
#i.e. files in raw that were not yet rectified
#difflist = sorted(list(set(raw_files).difference(set(prog['file']))))

for xlsx in raw_files:#difflist:
    print(xlsx)
    src = get_file_path(xlsx)
    data = pd.read_excel(src,sheet_name=None)
    #has been rectified already?
    if 'Rect' in data.keys():
        continue
    cont = data['Cont']
    #head = data['Header']
    #open file from difference list
    #cont = pd.read_excel(src,sheet_name='Cont')
    #head = pd.read_excel(src,sheet_name='Header',header=None)
#    date = head.iloc[0,1]
#    time = head.iloc[1,1]
#    focal = head.iloc[2,1]
    #ignore files with default 'unknown monkey' as focal
    #as those have not been used for data collection
#    if focal == 'umo':
#        update_csv(prog,progress_csv_path,[xlsx,'umo_focal'])
#        continue
    #ignore files which would be empty after time&actor-nan-removal
    #i.e. empty protocol which had a focal animal entered and nothing else.
    if all(cont['Time'].isna()) and all(cont['Action'].isna()):
#        update_csv(prog,progress_csv_path,[xlsx,'empty_cont'])
        continue
    #discard rows with neither time nor action (basically empty)
    cont = cont[ (~cont['Time'].isna()) | (~cont['Action'].isna()) ]
    #discard rows with 1L., 1R. or iun in act/rec
    #only useful if data was previously 'aufdröslert'.
    cont = cont[ (cont['Actor'] != '1L.') & (cont['Receiver'] != '1R.') ]
    cont = cont[ (cont['Actor'] != 'iun') & (cont['Receiver'] != 'iun') ]
    #TODO: fill empty time cells with empty_cell-value
    cont['Time'] = cont['Time'].fillna(empty_cell)
    #TODO untangle receiver makes duplicate lines
    #when action got detangled
    #delete duplicate lines for now, but WTF
    for i,col in enumerate(['Actor','Action','Receiver']):
        #i.e. make sure no empty cells exist in tangle-cols
        # ->fill actor, action and/or receiver nans with none.
        #TODO: MAKE SURE that it would be NANs, not empty strings or similar!
        #any() may help. isna() or == ''
        cont[col] = cont[col].fillna(empty_cell)
        #untangle, duh
        cont = untangle(cont,col)
        #move column to "proper" position
        #TODO maybe make this happen within untangle itself?
        cont.insert(i+1,col,cont.pop(col))
    #drop duplicate rows from detangling issue
    cont = cont.drop_duplicates()
    #drop rows without action - post detangle
    #should only apply to "xx " split rows
    #TODO: make sure of ^that!
    cont = cont[cont['Action'] != '']
    #swap M1 and M2 values whenever a monkey is in M1.
    #M1 is nan or whatever was in M2 erroneously afterwards.
    M2_temp = cont.loc[cont['M1'].isin(monkey_list),'M2']
    cont.loc[cont['M1'].isin(monkey_list),'M2'] = cont.loc[cont['M1'].isin(monkey_list),'M1']
    cont.loc[cont['M1'].isin(monkey_list),'M1'] = M2_temp
    #save the rectified dataframe in file,
    with pd.ExcelWriter(src, mode='a') as w:
        cont.to_excel(w, sheet_name=new_sheet,index=False)
    #rewrite the progress list once file is written
#    update_csv(prog,progress_csv_path,[xlsx,'rectified'])
    #append the protocol info to list of those
#    focal_info.loc[len(focal_info)] = [xlsx,date,time,focal,list(cont['Time'])[-1]]
#    update_csv(focal_info,protocols_csv_path,[xlsx,date,time,focal,list(cont['Time'])[-1]])


#TODO implement: drops=[i for i in cont.columns if all(cont[i].isnull())]
    # -> cont.drop(columns=drops)
    #finds and drop empty columns - might be e.g. comment col though -_-
    #put into error.py, and check with data_shape.*
#TODO: ensure encodings? maybe raw is non-utf8 -.-
#TODO refactor, get rid of rectified/raw divide
#make rect_files.txt for progress info

#TODO log file with different verbosities?
