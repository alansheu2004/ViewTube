import pandas as pd
#import mysql
#import sqlalchemy 
import html
'''url_object = sqlalchemy.engine.URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="DataFun!",  
    host="localhost",
    database="search",
)
from sqlalchemy import create_engine
engine = create_engine(url_object)

search = mysql.connector.connect(
  host="localhost",
  user="root",
  password='DataFun!',
  database="search")

sc = search.cursor(buffered=True)'''

#for use with youtube's video list search function.

'''
def dict_to_data_search(db):
    df = pd.DataFrame(index=range(len(db['items'])),columns=['totalResults','resultsPerPage',
    'publishedAt','categoryId','videoId','channelId','channelTitle','vidTitle',
    'thumbnail hq','thumbnail mq','thumbnail lq'])

    for key in db.items():
        if key[0] == 'pageInfo':
            df['totalResults'][0] =  db['pageInfo']['totalResults']
            df['resultsPerPage'][0] =  db['pageInfo']['resultsPerPage']
        
        elif key[0] == 'items':
            itemcount = 0
            for vid in db['items']:
                for stat in vid:
                    if (stat == 'snippet'):
                        for i in vid['snippet']:
                            if i == 'publishedAt':
                                df['publishedAt'][itemcount] =  vid['snippet'][i]
                            #elif i == 'publishTime':
                                #df['publishTime'][itemcount] =  vid['snippet'][i]
                            elif i == 'channelId':
                                df['channelId'][itemcount] =  vid['snippet'][i]
                            elif i == 'channelTitle':
                                df['channelTitle'][itemcount] =  vid['snippet'][i]
                            elif i == 'title':
                                df['vidTitle'][itemcount] =  vid['snippet'][i]
                            #elif i == 'description':
                                #df['vidDescription'][itemcount] =  vid['snippet'][i]
                            elif i == 'thumbnails':
                                df['thumbnail hq'][itemcount] = vid['snippet'][i]['high']['url']
                                df['thumbnail mq'][itemcount] = vid['snippet'][i]['medium']['url']
                                df['thumbnail lq'][itemcount] = vid['snippet'][i]['default']['url']
                            elif i == 'tags':
                                df['tags'][itemcount] = vid['snippet']['tags']
                            elif i == 'categoryId':
                                df['categoryId'][itemcount] = vid['snippet']['categoryId']
                    elif stat == 'statistics':
                        df['viewCount'][itemcount] = vid['statistics']['viewCount']
                        df['likeCount'][itemcount] = vid['statistics']['likeCount']
                        if 'commentCount' in vid['statistics']:
                            df['commentCount'][itemcount] = vid['statistics']['commentCount']
                        elif 'commentCount' not in vid['statistics']:
                            df['commentCount'][itemcount] = 'DISABLED'
                    elif stat == 'id':
                        df['videoId'][itemcount] = vid['id']['videoId']
                itemcount += 1
        
        else:
            pass

    return df
'''

def dict_to_data_search2(res):
    df = pd.DataFrame(index=range(len(res['items'])),columns=['totalResults','resultsPerPage',
    'publishedAt','categoryId','videoId','channelId','channelTitle','vidTitle',
    'thumbnail hq','thumbnail mq','thumbnail lq'])
    df['totalResults'][0] =  res['pageInfo']['totalResults']
    df['resultsPerPage'][0] =  res['pageInfo']['resultsPerPage']
    for itemcount, vid in enumerate(res['items']):
        df['videoId'][itemcount] = vid['id']['videoId']
        df['vidTitle'][itemcount] = html.unescape(vid['snippet']['title'])
        df['channelId'][itemcount] = vid['snippet']['channelId']
        df['channelTitle'][itemcount] = vid['snippet']['channelTitle']
        df['publishedAt'][itemcount] = vid['snippet']['publishedAt']
        df['thumbnail hq'][itemcount] = vid['snippet']['thumbnails']['high']['url']
        df['thumbnail mq'][itemcount] = vid['snippet']['thumbnails']['medium']['url']
        df['thumbnail lq'][itemcount] = vid['snippet']['thumbnails']['default']['url']
    #df.to_sql('search', con = engine, if_exists='append')
    return df

'''def dict_to_data(db):
    df = pd.DataFrame(index=range(len(db['items'])),columns=['totalResults','resultsPerPage',
    'publishedAt','categoryId','channelId','channelTitle','vidTitle','tags',
    'viewCount','likeCount','commentCount',
    'thumbnail hq','thumbnail mq','thumbnail lq'])

    for key in db.items():
        if key[0] == 'pageInfo':
            df['totalResults'][0] =  db['pageInfo']['totalResults']
            df['resultsPerPage'][0] =  db['pageInfo']['resultsPerPage']
        
        elif key[0] == 'items':
            itemcount = 0
            for vid in db['items']:
                for stat in vid:
                    if (stat == 'snippet'):
                        for i in vid['snippet']:
                            if i == 'publishedAt':
                                df['publishedAt'][itemcount] =  vid['snippet'][i]
                            #elif i == 'publishTime':
                                #df['publishTime'][itemcount] =  vid['snippet'][i]
                            elif i == 'channelId':
                                df['channelId'][itemcount] =  vid['snippet'][i]
                            elif i == 'channelTitle':
                                df['channelTitle'][itemcount] =  vid['snippet'][i]
                            elif i == 'title':
                                df['vidTitle'][itemcount] =  vid['snippet'][i]
                            #elif i == 'description':
                                #df['vidDescription'][itemcount] =  vid['snippet'][i]
                            elif i == 'thumbnails':
                                df['thumbnail hq'][itemcount] = vid['snippet'][i]['high']['url']
                                df['thumbnail mq'][itemcount] = vid['snippet'][i]['medium']['url']
                                df['thumbnail lq'][itemcount] = vid['snippet'][i]['default']['url']
                            elif i == 'tags':
                                df['tags'][itemcount] = vid['snippet']['tags']
                            elif i == 'categoryId':
                                df['categoryId'][itemcount] = vid['snippet']['categoryId']

                    elif stat == 'statistics':
                        if 'viewCount' in vid['statistics']:
                            df['viewCount'][itemcount] = vid['statistics']['viewCount']
                        if 'likeCount' in vid['statistics']:
                            df['likeCount'][itemcount] = vid['statistics']['likeCount']
                        if 'commentCount' in vid['statistics']:
                            df['commentCount'][itemcount] = vid['statistics']['commentCount']
                itemcount += 1
        
        else:
            pass

    return df
'''

def dict_to_data_vids(db):
    df = pd.DataFrame(index=range(len(db['items'])),columns=['totalResults','resultsPerPage',
    'publishedAt','categoryId','channelId','channelTitle','vidTitle','tags',
    'viewCount','likeCount','commentCount',
    'thumbnail hq','thumbnail mq','thumbnail lq'])
    df['totalResults'][0] =  db['pageInfo']['totalResults']
    df['resultsPerPage'][0] =  db['pageInfo']['resultsPerPage']
    for itemcount, vid in enumerate(db['items']):
        if 'categoryId' in vid['snippet']:
            df['categoryId'][itemcount] = vid['snippet']['categoryId']
        if 'channelId' in vid['snippet']:
            df['channelId'][itemcount] = vid['snippet']['channelId']
        if 'channelTitle' in vid['snippet']:
            df['channelTitle'][itemcount] = vid['snippet']['channelTitle']
        if 'title' in vid['snippet']:
            df['vidTitle'][itemcount] = html.unescape(vid['snippet']['title'])
        if 'tags' in vid['snippet']:
            df['tags'][itemcount] = vid['snippet']['tags']
        if 'viewCount' in vid['statistics']:
            df['viewCount'][itemcount] = vid['statistics']['viewCount']
        if 'likeCount' in vid['statistics']:
            df['likeCount'][itemcount] = vid['statistics']['likeCount']
        if 'commentCount' in vid['statistics']:
            df['commentCount'][itemcount] = vid['statistics']['commentCount']
        if 'thumbnails' in vid['snippet']:
            df['thumbnail hq'][itemcount] = vid['snippet']['thumbnails']['high']['url']
            df['thumbnail mq'][itemcount] = vid['snippet']['thumbnails']['medium']['url']
            df['thumbnail lq'][itemcount] = vid['snippet']['thumbnails']['default']['url']
        
    return df


'''def dict_to_data_channel(db):
    df = pd.DataFrame(index=range(len(db['items'])),columns=['channelId','viewCount','subscriberCount','videoCount'])
    db['items']
    for key in db.items():
        if key[0] == 'items':
            itemcount = 0
            for vid in db['items']:
                for stat in vid:
                    if stat == 'id':
                        df['channelId'][itemcount] = vid['id']
                    elif stat == 'statistics':
                        if 'viewCount' in vid['statistics']:
                            df['viewCount'][itemcount] = vid['statistics']['viewCount']
                        if 'subscriberCount' in vid['statistics']:
                            df['subscriberCount'][itemcount] = vid['statistics']['subscriberCount']
                        if 'videoCount' in vid['statistics']:
                            df['videoCount'][itemcount] = vid['statistics']['videoCount']
                itemcount += 1
        
        else:
            pass
    return df
'''

def dict_to_data_channel(db):
    if 'items' in db:
        df = pd.DataFrame(index=range(len(db['items'])),columns=['channelId','channelViewCount','subscriberCount','videoCount'])
        for itemcount, vid in enumerate(db['items']):
            df['channelId'][itemcount] = vid['id']
            if 'viewCount' in vid['statistics']:
                df['channelViewCount'][itemcount] = vid['statistics']['viewCount']
            if 'subscriberCount' in vid['statistics']:
                df['subscriberCount'][itemcount] = vid['statistics']['subscriberCount']
            if 'videoCount' in vid['statistics']:
                df['videoCount'][itemcount] = vid['statistics']['videoCount']
    else:
        df = pd.DataFrame(columns=['channelId','channelViewCount','subscriberCount','videoCount'])
    #df.to_sql('channels', con = engine, if_exists='append')
    #engine.execute("SELECT * FROM channels").fetchall()
    return df

    
