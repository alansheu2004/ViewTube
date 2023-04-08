from googleapiclient.discovery import build
import pandas as pd
import os
from dict_to_data import *
#from langdetect import detect
#import openpyxl
api_key_list = ['AIzaSyDummkJoF2_vdu2o4hjFS-bCz4I-4LIC3I',
'AIzaSyDR4hEsk1z3BfZxiKWK56Ngq7FDUYaA6hM',
'AIzaSyDXvfj1Sb9g1RLqv65lty504dwvu9c6qko',
'AIzaSyDvn3JLyVw2xxnX9V4qCEt9cdrC1-dk9cE',
'AIzaSyCAAh8Por6tq94Nf_pFzUszyg9iUHLech4',
'AIzaSyBQUXvS6h4lueTnotmMfnWlPpe9I66BkPs']

youtube = build('youtube','v3',developerKey=api_key_list[5])

def search_all_results(part, order, datatype, publishedBefore, maxResults, videoCategoryId=None, videoDuration = 'any',
relevanceLanguage = 'en', location=None, locationRadius=None, token=None, 
db=(pd.DataFrame(columns=['totalResults','resultsPerPage',
    'publishedAt','categoryId','channelId','channelTitle','videoId','vidTitle','tags',
    'viewCount','likeCount','commentCount',
    'thumbnail hq','thumbnail mq','thumbnail lq'])), calls=1, sheet_name = 'data1'):

    #youtube api search call
    call = youtube.search().list(part=part, order=order, type=datatype, publishedBefore=publishedBefore, 
    maxResults=maxResults, videoCategoryId=videoCategoryId, relevanceLanguage = relevanceLanguage, 
    location=location, locationRadius=locationRadius, videoDuration = videoDuration, pageToken=token)
    res = call.execute()
    save = dict_to_data_search2(res)

    db = pd.concat([db, save],ignore_index=True)
    
    #statistics are not part of youtube api list search. need to use video search.

    vidids = db['videoId'].tolist()
    #channels = db['channelId'].tolist()

    #THIS GAVE ME ERROR FOR SO LONG!! said it was invalid parameter
    # turns out it's bc vidids parameter can't be more than 50 vids long.
    #thanks stack overflow.
    if len(vidids) > 50:
        chunknums = -(len(vidids) // -50) #ceiling division
        for i in range(chunknums):
            start = i*50
            end = 49 + (i*50)
            chunk = vidids[start:end+1]
            call2 = youtube.videos().list(part=['snippet','statistics'], id=chunk, maxResults = maxResults)
            res2 = call2.execute()
            if i == 0:
                save2 = dict_to_data_vids(res2)
            else:
                save2_5 = dict_to_data_vids(res2)
                save2 = pd.concat([save2, save2_5], ignore_index= True)
    else:
        call2 = youtube.videos().list(part=['snippet','statistics'], id=vidids, maxResults = maxResults)
        res2 = call2.execute()
        save2 = dict_to_data_vids(res2)

    db['tags'] = save2['tags']
    db['viewCount'] = save2['viewCount']
    db['likeCount'] = save2['likeCount']
    db['commentCount'] = save2['commentCount']
    db['categoryId'] = save2['categoryId']

    #print('***CHANNEL ID OF THE MAIN DB***')    
    #print(db['channelId'])
    #db = pd.merge(db, save3, on='channelId')
    #print('***CHANNEL ID OF CHANNEL DATAFRAME***')
    #print(save3['channelId'])
    #print('***AFTER MERGE TO MAIN DB***')    
    #print(db['channelId'])
    #two databases
    #video ids (primary key), video info (views, likes, comments), channel id
    #channel ids (primary key), channel info (subs, views, video count)
    #separate dataframe with the thumbnail jpgs (separate?)
    #1 script for videos, 1 script for videos -> channels, 1 script for thumbnails, 1 script for assembly
    if calls >= 5:
        if os.path.exists('/Users/trac.k.y/Documents/yt_project/search_data.xlsx') == True: 
            #append to file, if it already exists
            with pd.ExcelWriter('/Users/trac.k.y/Documents/yt_project/search_data.xlsx', 
            mode = 'a', engine = 'openpyxl', if_sheet_exists = 'overlay') as writer:  
                db.to_excel(writer, sheet_name = sheet_name, index=False)
                return db
        else:
            with pd.ExcelWriter('/Users/trac.k.y/Documents/yt_project/search_data.xlsx') as writer:  
                db.to_excel(writer, sheet_name = sheet_name, index=False)
         
    else:
        calls += 1
        if 'nextPageToken' in res:
            search_all_results(part, order, datatype='video', publishedBefore=publishedBefore, maxResults=maxResults,
            videoCategoryId=videoCategoryId, relevanceLanguage = relevanceLanguage, 
            location=location, locationRadius=locationRadius, videoDuration = videoDuration,
            token=res['nextPageToken'], db=db, calls=calls, sheet_name = sheet_name)

if __name__ == '__main__':
    sheet_name = 'data'
    date = [2023,4,5]
    for i in range(10):
        sheet_name = f'data{i}'
        if date[2] != 1:
            date[2] = date[2] - 1
        else:
            date[2] = 28
            if date[1] != 1:
                date[1] = date[1] - 1
            else:
                date[0] = date[0] - 1
        search_all_results(part='snippet', order='viewCount', datatype = 'video', videoDuration = 'any', 
        publishedBefore= f'{date[0]}-{date[1]}-{date[2]}T00:00:00Z', relevanceLanguage = 'en', maxResults = 50, sheet_name = sheet_name)

        print(f'done{i+1}')


'''
df_new = df[df.input_text.apply(detect).eq('en')]
filter out non english results
'''
#11/18/22: my current quota count ran out bc i was ambitious enough to call the 
#search quota method 100 times which was a mistake 
#so now i need to try this new query tomorrow
# BUT
#they don't seem to let me get all the million results in this search
#set type to video bc i forgot statistics is only a parameter that applies to videos, 
#which was why i wasn't getting likes and view and comment coutns oops

#so uh it seems that using search is 100 times less conveient than using vid search
#see each call is 100. i have a quota of 10000. i want 1000000 results
#each call can bring back a max of 50 results. 1000000 results thus requires 200 calls
#AAAAAAA

#update i added a little if clause to stop and save data immediately before i go over limit :'))))
#hopefully i can test it out tomorrow and it works


'''
with pd.ExcelWriter(path) as writer:
    writer.book = openpyxl.load_workbook(path)
    df.to_excel(writer, sheet_name='new_sheet1')

'''