import pandas as pd
import re
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

def preprocessing(data):
    data = data.replace('\u202f', ' ')
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s*\d{1,2}:\d{1,2}\s*(?:am|pm)\s*'
    time_stamp = re.findall(pattern, data)
    message = re.split(rf"{pattern}-\s*", data)[1:]

    df = pd.DataFrame({'time': time_stamp, 'message': message})
    df['time'] = pd.to_datetime(df['time'], format = '%d/%m/%y, %I:%M %p ')


    users = []
    messages = []
    for message in df['message']:
        text = re.match(r'^(.+?):\s(.+)', message)
        if text:
            users.append(text[1])
            messages.append(text[2])
        else:
            users.append('Watsapp Notification')
            messages.append(message)
    df['user'] = users
    df['message'] = messages

    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    df['day'] = df['time'].dt.day
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute
    df.drop(columns=['time'], inplace=True)
    return df[df['user'] != 'Watsapp Notification']





