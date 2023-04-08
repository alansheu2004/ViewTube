import os
from googleapiclient.discovery import build
import pandas as pd
from dict_to_data import *
api_key_list = ['AIzaSyDummkJoF2_vdu2o4hjFS-bCz4I-4LIC3I',
'AIzaSyDR4hEsk1z3BfZxiKWK56Ngq7FDUYaA6hM',
'AIzaSyDXvfj1Sb9g1RLqv65lty504dwvu9c6qko',
'AIzaSyDvn3JLyVw2xxnX9V4qCEt9cdrC1-dk9cE',
'AIzaSyCAAh8Por6tq94Nf_pFzUszyg9iUHLech4',
'AIzaSyBQUXvS6h4lueTnotmMfnWlPpe9I66BkPs']

youtube = build('youtube','v3',developerKey=api_key_list[0])

def channel_search(channels=None, maxResults=50):
    if channels == None:
        db = pd.read_excel('/Users/trac.k.y/Documents/yt_project/youtube_project_database.xlsx', sheet_name = 'data1nodupes')
        channels = db['channelId']
        channels = channels.to_list()

    if len(channels) > 50:
        chan_chunknums = -(len(channels) // -50) #ceiling division
        for i in range(chan_chunknums):
            start = i*50
            end = 49 + (i*50)
            channel_chunk = channels[start:end+1]
            call3 = youtube.channels().list(part=['statistics'], id=channel_chunk, maxResults = 50)
            res3 = call3.execute()
            if i == 0:
                save3 = dict_to_data_channel(res3)
            else:
                save3_5 = dict_to_data_channel(res3)
                save3 = pd.concat([save3, save3_5], ignore_index= True)
                #print(save3)
    else:
        call3 = youtube.channels().list(part=['statistics'], id=channels, maxResults = maxResults)
        res3 = call3.execute()
        save3 = dict_to_data_channel(res3)
    with pd.ExcelWriter('/Users/trac.k.y/Documents/yt_project/channels_info.xlsx') as writer:  
        save3.to_excel(writer, sheet_name = 'test', index=False)
        return save3
