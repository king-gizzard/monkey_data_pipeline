import pandas as pd
import os
import time

#read filenames in directories, return list.
def file_list(state):
    path = os.path.join(os.pardir,'data',state)
    files = []
#    for root, dirs, xlsx in os.walk(path):
#        print(root,xlsx)
    for folder in os.listdir(path):
        files += os.listdir(os.path.join(path,folder))
    return(files)

#make sure that a directory for rectified data exists.
def ensure_rec_dir(subdir=''):
    recdir = os.path.join(os.pardir,'data','rectified',subdir)
    if not os.path.exists(recdir):
        os.makedirs(recdir)


ensure_rec_dir()
#make list of files in raw
raw_files = file_list('raw')
#make list of files in detangled
rec_files = file_list('rectified')

#with open(os.path.join(os.pardir,'misc_files','monkey_list.txt'),'r') as f:
#    monkey_list = f.read().split('\n')[:-1]

monkey_list = pd.read_csv(os.path.join(os.pardir,'misc_files','monkey_list.csv'))
monkey_list = list(monkey_list['id'])

action_list = pd.read_csv(os.path.join(os.pardir,'misc_files','action_list.csv'))
action_list = list(action_list['id'])

mod_list = pd.read_csv(os.path.join(os.pardir,'misc_files','mod_list.csv'))
mod_list = list(mod_list['id'])

#make list of difference
difflist = sorted(list(set(raw_files).difference(set(rec_files))))
for xlsx in difflist[:10]:  #TODO remove the training wheels
    print(xlsx)
    #reverse engineer dir name from file name :/
    d = xlsx[:10]
    #path in data/raw
    file_path = os.path.join(os.pardir,'data','raw',d,xlsx)
    #open file from difference list
    cont = pd.read_excel(file_path,sheet_name='Cont')#,dtype={'M1':str,'M2':str})
    #check for umo focal in header
    head = pd.read_excel(file_path,sheet_name='Header',header=None)
    focal = head.iloc[2,1]
    #ignore files with default 'unknown monkey' as focal
    #as those have not been used for data collection
    if focal == 'umo':
        continue
    #discard rows with neither time nor action (basically empty)
    cont = cont[ (~cont['Time'].isna()) & (cont['Action'] != '') ]
    #discard rows with 1L., 1R. or iun in act/rec
    #only useful if data was 'aufdröslert'.
#    shape = cont.shape
    cont = cont[ (cont['Actor'] != '1L.') & (cont['Receiver'] != '1R.') ]
    cont = cont[ (cont['Actor'] != 'iun') & (cont['Receiver'] != 'iun') ]
#    dröselt = (cont.shape == shape)
    #make empty 'copy' of sheet, to fill iteratively
    rect = pd.DataFrame(columns=cont.columns)
    #TODO entirely fucked
    for i,row in cont.iterrows():
        flag = False
        #bonus behaviours here?
        #TODO make actual modifications in rect
        if not pd.isna(row['M1']) and row['M1'] not in mod_list:
            print(row,end='\nm1\n')
        #additional monkeys here?
        if not pd.isna(row['M2']) and row['M2'] not in monkey_list:
            print(row,end='\nm2\n')
        #TODO refactor into for-loop
        if not row['Actor'] in monkey_list:
            flag = True
            if pd.isna(row['Actor']):
                row['Actor'] = 'none'
                rect = rect.append(row)
            else:
                val = [i for i in row['Actor'].split(' ') if i]
                if len(val) == 1:
                    row['Actor'] = val[0]
                    rect = rect.append(row)
                else:
                    for i in val:
                        row['Actor'] = i
                        rect = rect.append(row)
        if not row['Action'] in action_list:
            flag = True
            if pd.isna(row['Action']):
                row['Action'] = 'none'
                rect = rect.append(row)
            else:
                val = [i for i in row['Action'].split(' ') if i]
                if len(val) == 1:
                    row['Action'] = val[0]
                    rect = rect.append(row)
                else:
                    for i in val:
                        row['Action'] = i
                        rect = rect.append(row)
                    print(row,end='\nactions to split\n')
        #TODO ISSUE: can happen after previous appends
        #e.g. nar, ap de, don+
        #ap, de get split into lines, then don+
        #results in new line with last used row values...
        if not row['Receiver'] in monkey_list:
            flag = True
            if pd.isna(row['Receiver']):
                row['Receiver'] = 'none'
                rect = rect.append(row)
            else:
                val = [i for i in row['Receiver'].split(' ') if i]
                if len(val) == 1:
                    row['Receiver'] = val[0]
                    rect = rect.append(row)
                else:
                    for i in val:
                        row['Receiver'] = i
                        rect = rect.append(row)
                    print(row,end='\nreceivers to split\n')
        if flag == False:
            rect = rect.append(row)
    #save the rectified dataframe in file,
    #corresponding to 'cont' file path

    ensure_rec_dir(d)
    #TODO merge filepath and src (ie replace filepath)
    src = os.path.join(os.pardir,'data','raw',d,xlsx)
    dest = os.path.join(os.pardir,'data','rectified',d,xlsx)
    if os.name == 'posix':
        os.popen('cp '+src+' '+dest)
        time.sleep(1)
    #TODO check for windows name & build case
    elif os.name == 'idk':
        pass
    else:
        print('unknown operating system!')
    with pd.ExcelWriter(dest, mode='a') as w:
        rect.to_excel(w, sheet_name='Cont',index=False)
#check for multiple (space-seperated)
    #actor
        #split
    #action
        #split
    #receiver?
        #split - modifier maybe





#TODO implement: drops=[i for i in cont.columns if all(cont[i].isnull())]
    # -> cont.drop(columns=drops)
    #finds and drop empty columns - might be e.g. comment col though -_-
    #put into error.py, and check with data_shape.*
#save file in data/detang
#warn if file would be overwritten
#same folders/files or better?
    #same useful for difference
    #other better for manual review?

#    ensure_rec_dir(d)
#TODO: ensure encodings? maybe raw is non-utf8 -.-
