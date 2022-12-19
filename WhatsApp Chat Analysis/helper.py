from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # 1. Fetch number of messages
    num_messages = df.shape[0]

    # 2. Number of workds
    words = []
    for message in df['message']:
        words.extend(message.split())
        
    #3. Fetch number of media messages(images, memes)
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #4. Fetch number of links shared
    from urlextract import URLExtract
    extractor = URLExtract()

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_user(df):
    # import matplotlib.pyplot as plt

    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0]) * 100,1).reset_index().rename(columns = {'index': 'name', 'user':'percent %' })
    return x,df


def create_wordcloud(selected_user, df):

    f = open('Stop_words_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove group notification message fitering 
    temp = df[df['user'] != 'group_notification']
    # Remove media omitted
    temp = temp[temp['message'] != '<Media omitted>\n']     

    def remove_stop_words(message):
        Y = []
        for word in message.lower().split():
            if word not in stop_words:
                Y.append(word)
        return " ".join(Y)        
                

    wc = WordCloud(width = 500, height= 500, min_font_size=10, background_color ='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep= ' '))

    return df_wc    

def most_common_words(selected_user, df):

    f = open('Stop_words_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove group notification message fitering 
    temp = df[df['user'] != 'group_notification']
    # Remove media omitted
    temp = temp[temp['message'] != '<Media omitted>\n'] 
    
    # Remove Stop words
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(15))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(10)) #(len(Counter(emojis)
    return emoji_df


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()    
    
    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i] + '-' + str(timeline['year'][i])))
    
    timeline['time'] = time
    return timeline