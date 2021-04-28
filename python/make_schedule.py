import pandas as pd
import os
import datetime

#remake/reverse engineer what has been foolishly lost:
#receives
#   id_df:              df for a specific focal animal
#   time_slices[i]:     from what time onward is considered
#   time_slices[i+1]:   to what time is considered
#returns single int (number of prots in time slice)
def slice_sub_df(focal,from_time,to_time):
    low_bound  = focal[focal['time'] >= from_time]
    high_bound = focal[focal['time'] < to_time]
    both_bound = pd.merge(low_bound, high_bound, how='inner')
    return(both_bound.shape[0])

protocol_list_path = os.path.join(os.pardir,'misc_files','protocols_list.csv')
schedule_path = os.path.join(os.pardir,'misc_files','schedule.csv')

#columns: [date, time, focal]
df = pd.read_csv(protocol_list_path)
#TODO: warning, this could be slightly insane.
#was done to remove jw/sh duplicate protocols
df = df.drop_duplicates()
#make dates actual dates, not strings
df['date']=pd.to_datetime(df['date'],format='%Y-%m-%d').dt.date
#make time col string of always 4 digits
df['time'] = df['time'].astype(str).str.zfill(4)
#convert to actual datetime times
df['time'] = pd.to_datetime(df['time'],format='%H%M').dt.time


schedule = pd.DataFrame(columns=[
        'ID',
        'obs_latest',
        '6-9','9-12',
        '12-15',
        '15-18',
        '18-22',
        'obs_total'
        ])

time_slices = pd.Series([
        datetime.time(6,0),
        datetime.time(9,0),
        datetime.time(12,0),
        datetime.time(15,0),
        datetime.time(18,0),
        datetime.time(22,0)
        ])

#TODO: put +15 on time, to account for protocol length
individuals = df['focal'].unique()

for ID in individuals:
    id_df = df[df['focal']==ID]
    row = []
    row.append(ID)
    latest=id_df['date'].sort_values(ascending=False).iloc[0]
    row.append(latest)
    #sum(df['time'][0] > pd.Series(time_slices))
    #slice_counts = []
    all_obs = 0
    #ie 0:5 for 6 slices, so there is no overflow on highest 'to'
    for i in range(len(time_slices)-1):
        #slice_df = slice_sub_df(id_df,time_slices[i-1],time_slices[i])
        #slice_counts.append(len(slice_sub_df(id_df,time_slices[i],time_slices[i+1])))
        #x=len(slice_sub_df(id_df,time_slices[i],time_slices[i+1])) #old and lost
        x=slice_sub_df(id_df,time_slices[i],time_slices[i+1]) #new and cool
        row.append(x)
        all_obs += x
    #row.append(slice_counts)
    #row.append(sum(slice_counts))
    row.append(all_obs)
    schedule.loc[len(schedule)] = row

#reorder the columns
schedule = schedule[[
        'ID',
        'obs_total',
        '6-9',
        '9-12',
        '12-15',
        '15-18',
        '18-22',
        'obs_latest'
        ]]

schedule.to_csv(schedule_path,index=False)
