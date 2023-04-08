from googleapiclient.discovery import build
import pandas as pd
from dict_to_data import *
from langdetect import detect

from get_vids import *
from channels import *

#taken from the videos gathering script
sheet_name = 'data'
date = [2023,4,7]

print("Welcome to Tracy's code for scraping data from YouTube API! (her pride and joy and also blood sweat and tears)")
print("Enter the number of times you want to run this code: ")
num = input()
print("Now fetching data...")

for i in range(int(num)):
    sheet_name = f'data{i+1}'
    '''
    DATE ITERATION: scrapping bc i think it's screwing w the amount of unique results i get??
    if date[2] != 1:
        date[2] = date[2] - 1
    else:
        date[2] = 28
        if date[1] != 1:
            date[1] = date[1] - 1
        else:
            date[0] = date[0] - 1'''
    search_all_results(part='snippet', order='viewCount', datatype = 'video', videoDuration = 'medium', 
    publishedBefore= f'{date[0]}-{date[1]}-{date[2]}T00:00:00Z', relevanceLanguage = 'en', maxResults = 50, sheet_name = sheet_name)
    #read the sheet back in
    search_db = pd.read_excel('/Users/trac.k.y/Documents/yt_project/search_data.xlsx', sheet_name = sheet_name)
    channels = search_db['channelId']
    channels = channels.tolist()
    channels_db = channel_search(channels)
    #merge channels info with search info
    search_merged = search_db.merge(channels_db, on='channelId')

    if os.path.exists('/Users/trac.k.y/Documents/yt_project/search_and_channel.xlsx') == True: 
        #append to file, if it already exists
        with pd.ExcelWriter('/Users/trac.k.y/Documents/yt_project/search_and_channel.xlsx', 
        mode = 'a', engine = 'openpyxl', if_sheet_exists = 'overlay') as writer:  
            search_merged.to_excel(writer, sheet_name = sheet_name, index=False)
    else:
        with pd.ExcelWriter('/Users/trac.k.y/Documents/yt_project/search_and_channel.xlsx') as writer:  
            search_merged.to_excel(writer, sheet_name = sheet_name, index=False)

    print(f'Progress: {i+1}/{num}')
    print("Time of info retrieval:", pd.Timestamp.now())
print("Done! :D")
