    for col in ['Actor','Action','Receiver']:
        #i.e. make sure no empty cells exist in tangle-cols
        rect[col] = rect[col].fillna('none')
        #untangle, duh
        rect = untangle(rect,col)

    '''
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
    '''

