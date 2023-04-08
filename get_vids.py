from googleapiclient.discovery import build
import pandas as pd
import os
from dict_to_data import *

#API keys
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
    
    #statistics are not part of youtube api list search. need to use video search:
    vidids = db['videoId'].tolist()

    #youtube api video search call in chunks of 50
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
    #add video statistics to search dataframe
    db['tags'] = save2['tags']
    db['viewCount'] = save2['viewCount']
    db['likeCount'] = save2['likeCount']
    db['commentCount'] = save2['commentCount']
    db['categoryId'] = save2['categoryId']
    
    #save results to spreadsheet after 5 calls (so about 250 results)
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
