import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
# import seaborn as sns
import plotly.express as px

headers = {
    'authorization' : st.secrets['api_key']
}

youtube = build('youtube', 'v3', developerKey=headers)

def get_cateogories():
    all_data = []
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode="US"
    )
    response = request.execute()
    
    for i in range(len(response['items'])):
        data = dict(categories_names = response['items'][i]['snippet']['title'])
#                     channel_id = response['items'][i]['snippet']['channelId']
    
        all_data.append(data)
    
    return all_data

st.header('Top 5 YouTube Channels!')

items = get_cateogories()
categories = [d['categories_names'] for d in items]
# categories
selected_category = st.selectbox('Select any category 🍰',categories)

import requests
SEARCH_QUERY = selected_category
MAX_RESULTS = 5

# Make a GET request to search for channels in the food category
url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={SEARCH_QUERY}&maxResults={MAX_RESULTS}&key={headers}"
response = requests.get(url)

# Parse the response and extract the channel IDs
data = response.json()
channels = data['items']
channel_ids = [channel['id']['channelId'] for channel in channels]

# # Print the top 10 channel IDs in the food category
# print("Top 10 Channel IDs in the Food Category:")
# for channel_id in channel_ids:
#     print(channel_id)


def get_Channel_data():
    channel_data = []

    request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id = ','.join(channel_ids)
        )
    response = request.execute()
    for i in range(len(response['items'])):
        data = dict(Channel_names =  response['items'][i]['snippet']['title'],
                    Subscribers   =  response['items'][i]['statistics']['subscriberCount'],
                    Views         =  response['items'][i]['statistics']['viewCount'],
                    Total_videos  =  response['items'][i]['statistics']['videoCount']) 
        channel_data.append(data)
    
    return channel_data

# channel_statistics
channel_statistics = get_Channel_data()
channel_df = pd.DataFrame(channel_statistics)

# convert object type to integer in columns -> Subscribers, Views, Total_videos
channel_df['Subscribers'] = pd.to_numeric(channel_df['Subscribers'])
channel_df['Views'] = pd.to_numeric(channel_df['Views'])
channel_df['Total_videos'] = pd.to_numeric(channel_df['Total_videos'])

channel_data = st.table(channel_df)

# who has the highest number of subscriber
st.subheader('Number of subscribers')
fig = px.bar(data_frame= channel_df, x='Channel_names', y = 'Subscribers',color="Channel_names",width=900, height=500)
st.write(fig)

# # Who has the highest number of views
st.subheader('Number of views')
fig = px.bar(data_frame= channel_df, x='Channel_names', y = 'Views',color="Views",width=900, height=500)
st.write(fig)

# # who posted the highest number of videos
st.subheader('Total Videos Posted')
fig = px.bar(data_frame= channel_df, x='Channel_names', y = 'Total_videos',color="Total_videos",width=900, height=500)
st.write(fig)
