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
#def ensure_rec_dir(subdir=''):
#    recdir = os.path.join(os.pardir,'data','rectified',subdir)
#    if not os.path.exists(recdir):
#        os.makedirs(recdir)

def untangle(df,col_name):
    col = df[col_name].str.split(' ').apply(pd.Series,1).stack()
    col.index = col.index.droplevel(-1)
    col.name = col_name
    del(df[col_name])
    return(df.join(col))

#HARDCODE - config options, kinda ------------------------------------
#
#value to 'fillna' in Actor/Action/Receiver
#used/searched also by error.py
empty_cell = 'none'
#name of sheet with detangled data
new_sheet = 'Rect'
#make debug print show entire frame
pd.set_option('display.max_rows', None)
progress_list = os.path.join(os.pardir,'misc_files','progress_list.txt')
#
#---------------------------------------------------------------------

#REFACTOR no rec dir
if os.path.exists(progress_list):
    with open(progress_list,'r') as f:
        prog = f.read().split('\n')
else:
    prog = []

#make sure a 'rectified' folder exists,
#to crawl and later save stuff in
#ensure_rec_dir()#KILL
#make list of files in raw
raw_files = file_list('raw')
#make list of files in detangled
#rec_files = file_list('rectified')#KILL
#make list of difference
#difflist = sorted(list(set(raw_files).difference(set(rec_files))))

difflist2 = sorted(list(set(raw_files).difference(set(prog))))

#read 'support files'
monkey_list = pd.read_csv(os.path.join(os.pardir,'misc_files','monkey_list.csv'))
action_list = pd.read_csv(os.path.join(os.pardir,'misc_files','action_list.csv'))
mod_list    = pd.read_csv(os.path.join(os.pardir,'misc_files','mod_list.csv'))

#make usable lists out of them
monkey_list = list(monkey_list['id'])
action_list = list(action_list['id'])
mod_list    = list(mod_list['id'])

for xlsx in difflist2:#[:2]:  #TODO remove the training wheels
    print(xlsx)
    #reverse engineer dir name from file name :/
    d = xlsx[:10]
    #path in data/raw
    src = os.path.join(os.pardir,'data','raw',d,xlsx)
    #open file from difference list
    cont = pd.read_excel(src,sheet_name='Cont')#,dtype={'M1':str,'M2':str})
    head = pd.read_excel(src,sheet_name='Header',header=None)
    focal = head.iloc[2,1]
    #ignore files with default 'unknown monkey' as focal
    #as those have not been used for data collection
    if focal == 'umo':
        continue
    #ignore files which would be empty after time&actor-nan-removal
    #i.e. empty protocol which had a focal animal entered and nothing else.
    if all(cont['Time'].isna()) and all(cont['Action'].isna()):
        continue
    #discard rows with neither time nor action (basically empty)
    #cont = cont[ (~cont['Time'].isna()) & (cont['Action'] != '') ] #old
    cont = cont[ (~cont['Time'].isna()) | (~cont['Action'].isna()) ]
    #discard rows with 1L., 1R. or iun in act/rec
    #only useful if data was 'aufdröslert'.
    cont = cont[ (cont['Actor'] != '1L.') & (cont['Receiver'] != '1R.') ]
    cont = cont[ (cont['Actor'] != 'iun') & (cont['Receiver'] != 'iun') ]
    #work copy here to be able to compare:
    rect = cont.copy()
    #TODO untangle receiver makes duplicate lines
    #when action got detangled
    #delete duplicate lines for now, but WTF
    for i,col in enumerate(['Actor','Action','Receiver']):
        #i.e. make sure no empty cells exist in tangle-cols
        #TODO fill actor, action and/or receiver nans with none.
        #MAKE SURE that it would be NANs, not empty strings or similar!
        #any() may help. isna() or == ''
        rect[col] = rect[col].fillna(empty_cell)
        #untangle, duh
        rect = untangle(rect,col)
        #move column to "proper" position
        #TODO maybe make this happen within untangle itself?
        rect.insert(i+1,col,rect.pop(col))
    #drop duplicate rows from detangling issue
    rect = rect.drop_duplicates()
    #drop rows without action - post detangle
    #should only apply to "xx " split rows
    #make sure of that!
    rect = rect[rect['Action'] != '']
    #M1 and M2 column correction: --------------------------------------------
    #swap M1 and M2 values whenever a monkey is in M1.
    #M1 is nan or whatever was in M2 erroneously afterwards.
    M2_temp = rect.loc[rect['M1'].isin(monkey_list),'M2']
    rect.loc[rect['M1'].isin(monkey_list),'M2'] = rect.loc[rect['M1'].isin(monkey_list),'M1']
    rect.loc[rect['M1'].isin(monkey_list),'M1'] = M2_temp
    #save the rectified dataframe in file,
    #corresponding to 'cont' file path
    #KILL
#    ensure_rec_dir(d)
#    dest = os.path.join(os.pardir,'data','rectified',d,xlsx)
#    if os.name == 'posix':
#        os.popen('cp ' + src + ' ' + dest)
#        #sleep to let file copy finish.
#        time.sleep(0.05)
#    elif os.name == 'idk':
#        pass
#    else:
#        print('unknown operating system!')
#    #
#    #
    with pd.ExcelWriter(src, mode='a') as w:
        rect.to_excel(w, sheet_name=new_sheet,index=False)

    prog.append(xlsx)
    with open(progress_list, 'w') as progfile:
        [progfile.write(str(filename) + '\n') for filename in prog]



#TODO implement: drops=[i for i in cont.columns if all(cont[i].isnull())]
    # -> cont.drop(columns=drops)
    #finds and drop empty columns - might be e.g. comment col though -_-
    #put into error.py, and check with data_shape.*
#TODO: ensure encodings? maybe raw is non-utf8 -.-
#TODO refactor, get rid of rectified/raw divide
#make rect_files.txt for progress info

#TODO log file with different verbosities?
