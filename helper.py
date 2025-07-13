from urlextract import URLExtract
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


