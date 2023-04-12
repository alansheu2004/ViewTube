#writing information from youtube api search result (dictionary/json format) into dataframe

import pandas as pd
import html

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
    return df

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
    return df

    
