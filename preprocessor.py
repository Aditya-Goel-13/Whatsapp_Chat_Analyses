import pandas as pd
import re

def preprocessing(data):
    # Don't remove \n — we need them to detect multi-line messages
    data = data.replace('\u202f', ' ').replace('\xa0', ' ')

    # Regex for full timestamp
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{1,2}(?:\s*(?:am|pm)))\s*-\s*'
    matches = list(re.finditer(pattern, data, flags=re.IGNORECASE))

    if not matches:
        raise ValueError("No timestamps found. Check file formatting.")

    messages = []
    time_stamps = []

    for i in range(len(matches)):
        start = matches[i].end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(data)
        raw_message = data[start:end].strip()

        # Normalize multi-line spacing
        raw_message = raw_message.replace('\r\n', '\n').replace('\r', '\n')

        time_stamps.append(matches[i].group(1))
        messages.append(raw_message)

    df = pd.DataFrame({'time': time_stamps, 'message': messages})

    try:
        df['time'] = pd.to_datetime(df['time'], format='%d/%m/%y, %I:%M %p')
    except:
        df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y, %I:%M %p')

    # Separate user from message
    users, texts = [], []
    for msg in df['message']:
        match = re.match(r'([^:]+?):\s(.*)', msg, flags=re.DOTALL)
        if match:
            users.append(match.group(1))
            texts.append(match.group(2).strip())
        else:
            users.append('Watsapp Notification')
            texts.append(msg.strip())

    df['user'] = users
    df['message'] = texts
    df['message'] = df['message'].apply(lambda m: m.replace('\n', '').replace('<This message was edited>', ''))

    # Time parts
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    df['day'] = df['time'].dt.day
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute
    df.drop(columns=['time'], inplace=True)
    df = df[df['message']!= 'You deleted this message']
    df = df[df['message'] != 'This message was deleted']
    return df[df['user'] != 'Watsapp Notification'].reset_index(drop=True)





