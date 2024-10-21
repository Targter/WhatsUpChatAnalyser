import pandas as pd
import re

def prebuiltfunction(data):
    # Pattern to match dates and timestamps
    pattern = r'\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}\s-\s'
    
    # Split the data based on the timestamp pattern
    messages = re.split(pattern, data)[1:]  # Ignore the first split part (usually empty)
    dates = re.findall(pattern, data)  # Extract all matching dates

    # Create a DataFrame with user messages and dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates}) 

    # Convert 'message_date' to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ') 
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Initialize lists to store users and messages separately
    users = []
    msgs = []

    for message in df['user_message']:
        # Split the message to extract user and message parts
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        
        if len(entry) > 1:  # If a user is found
            users.append(entry[1])
            msgs.append(entry[2])
        else:  # If it's a group notification
            users.append('group_notification')
            msgs.append(entry[0])

    # Add 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = msgs

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    # Convert 'date' column to datetime if not already
    df['date'] = pd.to_datetime(df['date'])

    # Extract year, month, day, and weekday name
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] =df['date'].dt.date


    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
