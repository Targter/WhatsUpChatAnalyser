# for creating the function whihc helps in hte app.py
from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
extractor = URLExtract()
def fetchStatus(selected_user,df):
    if selected_user != 'All_':
        df = df[df['user']== selected_user]
    total_media_message = df[df['message'] == '<Media omitted>\n']
    urls_len =[]
    for message in df['message']:
        urls_len.extend(extractor.find_urls(message))
    # len(urls)

    # extract urls with date
    urls_by_date = []

# Loop over each row in the dataframe and extract URLs and dates
    for index, row in df.iterrows():
        # Extract URLs from the message
        urls = extractor.find_urls(row['message'])
        
        # Get the corresponding date
        date = row['date']
        
        # If URLs are found, store them with their corresponding date
        for url in urls:
            urls_by_date.append({'Date': date, 'URL': url})

    # Convert the list of URLs and dates into a DataFrame
            df_urls_by_date = pd.DataFrame(urls_by_date)

            # Convert the 'Date' column to datetime for sorting
            df_urls_by_date['Date'] = pd.to_datetime(df_urls_by_date['Date'])

            # Sort by date in descending order to get the most recent dates first
            df_urls_by_date = df_urls_by_date.sort_values(by='Date', ascending=False)

            # Extract the first 30 URLs based on the most recent dates
            df_recent_urls = df_urls_by_date.head(30)

    # return 
    return df.shape[0],len(total_media_message),len(urls_len),df_recent_urls


def most_busy_user(df):
    x = df['user'].value_counts().head()
    newRow = round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns = {'user':'name','message':'percentage'})
    return x , newRow

def wordCloudd(selected_user , df):
    if selected_user != 'All_':
        df = df[df['user']==selected_user]
    # 
    wc = WordCloud(width = 400, height = 200, background_color ='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_used_word(selected_user,df):
    if selected_user != 'All_':
        df = df[df['user']==selected_user]

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']
    # removing stop words using file stop_hinglish.txt:
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                # counter helps us to count the total number of words : or data
    df_new = pd.DataFrame(Counter(words).most_common(30))

    return df_new

def emoji_analysis(selected_user, df):
    if selected_user != 'All_':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

# timeline
def monthly_timeline(selected_user ,df):
    if selected_user != 'All_':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'All_':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'All_':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'All_':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user ,df):
    if selected_user != 'All_':
        df = df[df['user'] == selected_user]
        
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap