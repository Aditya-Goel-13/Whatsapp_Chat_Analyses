from urlextract import URLExtract
from wordcloud import WordCloud, STOPWORDS
import string
from collections import Counter
import pandas as pd
import emoji
extractor = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]

    links = []
    words = []
    num_media = 0
    for message in df['message']:
        if message != '<Media omitted>':
            words.extend(message.split(' '))
            links.extend(extractor.find_urls(message))
        else:
            num_media += 1
    num_words = len(words)
    num_links = len(links)
    return num_messages, num_words, num_media, num_links


def fetch_active_users(df):
    x = df['user'].value_counts()
    df = round(x/df.shape[0] * 100, 2).reset_index().rename(columns={'index': 'user', 'value': 'percent'})
    return x.head(), df

def create_word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['message']!='<Media omitted>']
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    words = []

    with open("data/stop_hinglish.txt", 'r') as f:
        hinglish_stopwords = (f.read()).split()
    for message in df['message']:
        message = message.lower().strip()
        for word in message.split(' '):
            word = word.strip()
            if word!= '' and word not in hinglish_stopwords and not word.isnumeric():
                words.append(word)

    text = ' '.join(words)
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    df_wc = wc.generate(text)

    word_count = pd.DataFrame(Counter(words).most_common(20))

    return df_wc, word_count


def emoji_counter(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(len(emojis)), columns=['emoji', 'count'])





