import re
import pandas as pd

def pre(data):
    pattern = re.compile(r'(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?[apm]{2}) - (.*?): ')
    matches = re.findall(pattern, data)
    messages = pattern.sub('', data).split('\n')

    data_list = []
    for i, match in enumerate(matches):
        date_time = match[0]
        sender = match[1]
        message = messages[i]
        data_list.append([date_time, sender, message])
    
    df = pd.DataFrame(data_list, columns=['Date', 'Sender', 'Message'])
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y, %I:%M %p')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day_name'] = df['Date'].dt.day_name()
    df['Month_num'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    
    return df
