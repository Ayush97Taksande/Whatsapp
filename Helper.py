from urlextract import URLExtract
import emoji
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import joblib
def fetch_stats(selected_user, dataset):
    if selected_user == "Overall":
        total_messages = dataset.shape[0]
    else:
        total_messages = dataset[dataset['Sender'] == selected_user].shape[0]
    return total_messages

def url_extr(selected_user, dataset):
    extractor = URLExtract()
    if selected_user == "Overall":
        urls = [url for message in dataset['Message'] for url in extractor.find_urls(message)]
    else:
        user_data = dataset[dataset['Sender'] == selected_user]
        urls = [url for message in user_data['Message'] for url in extractor.find_urls(message)]
    return len(urls)

def words(selected_user, dataset):
    if selected_user == "Overall":
        words = [word for message in dataset['Message'] for word in message.split()]
    else:
        user_data = dataset[dataset['Sender'] == selected_user]
        words = [word for message in user_data['Message'] for word in message.split()]
    return len(words)

def media_shared(selected_user, dataset):
    if selected_user == "Overall":
        media = dataset[dataset['Message'] == "<Media omitted>"].shape[0]
    else:
        user_data = dataset[dataset['Sender'] == selected_user]
        media = user_data[user_data['Message'] == "<Media omitted>"].shape[0]
    return media

def busy_users(dataset):
    x = dataset['Sender'].value_counts().head()
    new_dataset = round((dataset['Sender'].value_counts() / dataset.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'Sender': 'percent'})
    return x, new_dataset
def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    temp = df[df['Sender'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc
# def emoji_helper(selected_user, dataset):
#     print("Columns in the dataset:", dataset.columns)
    
#     if selected_user != 'Overall':
#         dataset = dataset[dataset['Sender'] == selected_user]

#     # Debug: Check the first few rows of the filtered dataset
#     print("First few rows of the filtered dataset:", dataset.head())

#     emojis = []
#     for message in dataset['Message']:
#         emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

#     emoji_dataset = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])

#     return emoji_dataset



def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    temp = df[df['Sender'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time

    return timeline
def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    daily_timeline = df.groupby('Date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    return df['Day'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    user_heatmap = df.pivot_table(index='Day', values='Message', aggfunc='count').fillna(0)

    return user_heatmap

