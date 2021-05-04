import pandas as pd
import os
from pipeline_utils import *

def make_adjacency_list(mon_list):
    return(pd.Series([pd.Series([[],[]],index=['time','action']) for i in m],index=m))

def append_action(adj_list,mon,time,action):
    adj_list[mon]['time'].append(time)
    adj_list[mon]['action'].append(action)
    return(adj_list)

def remove_action(adj_list,mon,action):
    #note: always removes FIRST occurence of action
    index = adj_list[mon]['action'].index(action)
    adj_list[mon]['time'].pop(index)
    adj_list[mon]['action'].pop(index)
    return(adj_list)

def check_legit_update(adj_list,mon,time,action):
    #get lists of behaviors that the action is within, matching or "bracketing":
    #bracket can be none, open or close, so the stack operation can be determined.
    within = action_list[action_list['id'] == action]['within'].to_list()[0].split(' ')
    match  = action_list[action_list['id'] == action]['match' ].to_list()[0].split(' ')
    bracket  = action_list[action_list['id'] == action]['bracket']
    if within != 'none':
        parent = [i for i in within if i in acting['aff']['action']]#should only ever be 1 or 0
        if len(parent) < 1:
            #ERROR: Behavior that this belongs within is not opened
            pass
        if len(parent) > 1:
            #ERROR?: Behavior that this belongs within is TOO open
            pass
    if match != 'none' and bracket == 'close':
        matching = [i for i in match if i in acting['aff']['action']]#should only ever be 1 or 0
        if len(matching) == 0:
            #ERROR: closing behavior where none is open
            pass
    if match != none and bracket == 'open':
        if action in acting['aff']['action']:
            #ERROR: behavior still on stack (-> previous was not closed)
            pass
    pass
    #

pd.set_option('display.max_rows', None)

#progress_csv_path = os.path.join(os.pardir,'misc_files','progress_list.csv')
monkey_csv_path = os.path.join(os.pardir,'misc_files','monkey_list.csv')
action_csv_path = os.path.join(os.pardir,'misc_files','action_list.csv')
mod_csv_path = os.path.join(os.pardir,'misc_files','mod_list.csv')
error_csv_path= os.path.join(os.pardir,'misc_files','error_list.csv')

#prog = pd.read_csv(progress_csv_path)

monkey_list = pd.read_csv(monkey_csv_path)#get_id_list(monkey_csv_path)
action_list = pd.read_csv(action_csv_path)#get_id_list(action_csv_path)
mod_list    = pd.read_csv(mod_csv_path)#get_id_list(mod_csv_path)

#to_check_list = list(prog[prog['status'] == 'rectified']['file'])

error_head= ['file','sheet','row','column','content','error']

e_csv = get_or_make_csv(error_csv_path,error_head)

raw_files = file_list()

for protocol in raw_files:#to_check_list:
    print(protocol)
    #time in former row, to check time continuity
    former_time = 0
    #adjacency lists for behavior context checks
#    acting    = make_adjacency_list(monkey_list)
#    receiving = make_adjacency_list(monkey_list)
    #load data
    path = get_file_path(protocol)
    if not has_rect_sheet(path):
        continue
    head = pd.read_excel(path,sheet_name='Header',header=None,dtype=str)
    cont = pd.read_excel(path,sheet_name='Rect',dtype=str)
#    prox = pd.read_excel(path,sheet_name='Prox')
#    adlib = pd.read_excel(path,sheet_name='Adlib')
    #---errors in header----------------------------------------------------------------
    if head.iloc[2,1] not in list(monkey_list['id']):
        e_csv.loc[len(e_csv)] = [protocol,'Header',2,1,head.iloc[2,1],'Invalid Focal name']
    if not head.iloc[1,1].isnumeric():#type(head.iloc[1,1]) == int:
        e_csv.loc[len(e_csv)] = [protocol,'Header',1,1,head.iloc[1,1],'Invalid Time format']
    #TODO check for duplicate
    #---errors in cont----------------------------------------------------------------
    for i,row in cont.iterrows():
        #TODO: throws actual error on empty cell, try to correct for that
        if not row['Time'].isnumeric():#type(row['Time']) == float:
            e_csv.loc[len(e_csv)] = [protocol,'Cont',i,'Time',row['Time'],'Invalid Time format']
        elif int(row['Time']) < former_time:
            e_csv.loc[len(e_csv)] = [protocol,'Cont',i,'Time',row['Time'],'Time is lower than last recorded time']
        if row['Actor'] not in list(monkey_list['id']):
            e_csv.loc[len(e_csv)] = [protocol,'Cont',i,'Actor',row['Actor'],'Invalid Actor name']
        if row['Action'] not in list(action_list['id']):
            e_csv.loc[len(e_csv)] = [protocol,'Cont',i,'Action',row['Action'],'Invalid Action name']
        elif int(action_list[action_list['id'] == row['Action']]['n_receiver']) == 0:
            if row['Actor'] != row['Receiver']:
                e_csv.loc[len(e_csv)] = [protocol,'Cont',i,'Actor',row['Actor'],'Self-directed with non-identical Actor/Receiver pairing']
        else:
            #seems somehow busted, refer to WA chat for examples.
            if row['Actor'] == row['Receiver']:
                e_csv.loc[len(e_csv)] = [protocol,'Cont',i,'Actor',row['Actor'],'Not Self-directed, but identical Actor/Receiver pairing']
        if row['Receiver'] not in list(monkey_list['id']):
            e_csv.loc[len(e_csv)] = [protocol,'Cont',i,'Receiver',row['Receiver'],'Invalid Receiver name']
        #---variables for next iteration comparisons-------------------------------------
        if row['Time'].isnumeric():
            former_time = int(row['Time'])
    e_csv.to_csv(error_csv_path,index=False)

#check cont for:
    #right columns
    #monke in actor not in monke_list
    #monke in receiver not in monke_list
    #invalid time format (non-number)
    #action not in action_list
    #receiver in "self-directed"
    #unmatched bracket action
    #incorrectly nested action
    #modifiers?
    #non-linear timecode
    #check for single "+" in actor/receiver

#check prox for:
    #right columns
    #not detangled yet?
    #monke in monke_list for
    #each space separated
    #or "n"

#check adlib for:

#write error message for each:
