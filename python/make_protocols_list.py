import pandas as pd
import os
from pipeline_utils import *

#HARDCODE - config options, kinda ------------------------------------
#
#make debug print show entire frame
pd.set_option('display.max_rows', None)
protocols_csv_path = os.path.join(os.pardir,'misc_files','protocols_list.csv')
#
#---------------------------------------------------------------------

#focal_info = get_or_make_csv(protocols_csv_path,
header = ['file','date','time','focal','duration'])
focal_info = pd.Dataframe(columns=header)
#make list of files in raw
raw_files = file_list()

for xlsx in raw_files:
    print(xlsx)
    src = get_file_path(xlsx)
    #open file from ALL file list
    if not has_rect_sheet(src):
        continue
    rect = pd.read_excel(src,sheet_name='Rect')
    head = pd.read_excel(src,sheet_name='Header',header=None)
    date = head.iloc[0,1]
    time = head.iloc[1,1]
    focal = head.iloc[2,1]
    #ignore files with default 'unknown monkey' as focal
    #as those have not been used for data collection
#    if focal == 'umo':
#        continue
    #ignore files which would be empty after time&actor-nan-removal
    #i.e. empty protocol which had a focal animal entered and nothing else.
#    if all(rect['Time'].isna()) and all(rect['Action'].isna()):
#        continue
    #update_csv(focal_info,protocols_csv_path,[xlsx,date,time,focal,list(rect['Time'])[-1]])
    focal_info.to_csv(protocols_csv_path,index=False)
