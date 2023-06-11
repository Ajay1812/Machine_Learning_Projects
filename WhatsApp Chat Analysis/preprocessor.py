import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s'
    
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # conver message_datatype
    df['message_date'] = pd.to_datetime(df['message_date'], format = '%m/%d/%y, %H:%M %p - ')
    df.rename(columns = {'message_date': 'date'}, inplace = True)
    df.head()


    # Separate users and mesaages
    users = []
    messages1 = []
    for messages in df['user_message']:
        entry = re.split('([\w\W]+?):\s', messages)
        if entry[1:]: #User Name
            users.append(entry[1])
            messages1.append(entry[2])
        else:
            users.append('group_notification')
            messages1.append(entry[0])
        
    df['user'] = users  
    df['message'] = messages1
    df.drop(columns = ['user_message'], inplace = True)
    

    # Extracting Year, month, day from df['date'] column
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day

    # Extracting time(hour & min) from df['date']
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df