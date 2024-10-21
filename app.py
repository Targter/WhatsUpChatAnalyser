# pip install streamlit first to install the streamlit app 
import streamlit as st
import AppFunction,helperfile
import matplotlib.pyplot as plt
import io
import seaborn as sns
from PIL import Image
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.sidebar.title("Chat Analyzer")

import pandas as pd



# Set the title of the app
# Create a sidebar for file upload
st.sidebar.title("Upload Section")
with st.expander("Upload Section (for smaller screens)", expanded=False):
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt', 'csv', 'xlsx'])
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text_area(data)
    df = AppFunction.prebuiltfunction(data)


    # st.dataframe(df)
    #fetch unique user
    user_list = df['user'].unique().tolist()
    # user_list.remove('None')
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'All_')
    selected_user = st.sidebar.selectbox('Show analysis wrt:',user_list)
    # print(selected_user)
    
        
    # st.dataframe(df)
    if st.sidebar.button('show Analysis'):
        Total_message ,Total_MediaMessages, Total_urls , Urls_withDates= helperfile.fetchStatus(selected_user,df)
        
        # st.dataframe(Urls_withDates)
        st.title('Top Statictics')
        # NOW I AM FINDING THE NUMBER OF MESSAGE WERE SEND IN THE GROUP NUMBER OF MEDIA FILES AND NUMBER OF LINKS
        col1, col2, col3= st.columns(3)
        
        with col1:
            col1.header("Total Messages")
            col1.title(Total_message)
        # fetch number of media messages: 
        with col2:
            col2.header('Total Media Messages')
            col2.title(Total_MediaMessages)
        with col3:
            col3.header('Total_Urls')
            col3.title(Total_urls)
            with st.expander("Show Recent URLs", expanded=False):
                st.write("Here are the most recent URLs:")
                # for url in Urls_withDates: 
                st.write(Urls_withDates)
        # 
        #timeline
        st.title("Monthly timeline")
        timeline = helperfile.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        plt.xticks(rotation ='vertical')
        ax.plot(timeline['time'],timeline['message'] )
        st.pyplot(fig)

# daily timeline
        st.title("Daily timeline")
        daily_timeline = helperfile.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        plt.xticks(rotation ='vertical')
        ax.plot(daily_timeline['only_date'],daily_timeline['message'] )
        st.pyplot(fig)

# weekly activity: 

        st.title('Weekly timeline')
        col1, col2 = st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day = helperfile.week_activity_map(selected_user,df)
            fig ,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helperfile.month_activity_map(selected_user,df)
            fig ,ax = plt.subplots()
            plt.xticks(rotation="vertical")
            ax.bar(busy_month.index,busy_month.values)
            st.pyplot(fig)

# heatmap:
        st.title("Weekly Activity Map")
        user_heatmap = helperfile.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        # finding the most busy user or most active user in the group : 
        if selected_user == 'All_':
            st.title('Most Active User')
            x ,percent_count_user = helperfile.most_busy_user(df)
            fig ,ax = plt.subplots()
            
            col1, col2 = st.columns(2)
            with col1 :
                ax.bar(x.index, x.values)
                plt.xticks(rotation ='vertical')
                st.pyplot(fig)
            with col2:
                col2.title('Percentage of Active User')
                st.dataframe(percent_count_user)

        # wordcloud:
        wc_img = helperfile.wordCloudd(selected_user , df)
        
# Convert WordCloud object to an image
        
        wc_img = helperfile.wordCloudd(selected_user, df)

# Create a new figure for the word cloud
        fig_wc, ax_wc = plt.subplots(figsize=(8, 2))  # Adjust the size here
        ax_wc.imshow(wc_img, interpolation='bilinear')
        ax_wc.axis('off')

        # Save to a BytesIO buffer
        buf_wc = io.BytesIO()
        plt.savefig(buf_wc, format='png', bbox_inches='tight')
        buf_wc.seek(0)  # Rewind the buffer to the beginning

        # Display the word cloud image

        col1 , col2 = st.columns(2)
        with col1:
            st.image(buf_wc, width=800)  # Specify width for display
            

        # remove group_notification and media omitted like words: 
        # with col2:
        df_new = helperfile.most_common_used_word(selected_user,df)
        # st.dataframe(df_new)
        # create a bar graph instead of this 
        fig , axis = plt.subplots()
        axis.bar(df_new[0],df_new[1])
        plt.xticks(rotation ="vertical")
        st.title("Most Common Words")
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helperfile.emoji_analysis(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig , ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

else:
    st.header("Welcome to Abhay Chat Analysis App")
    st.warning("please upload a file to proceed with the analytics")
    st.info("Please upload the WhatsApp chat file without media (txt, csv, or xlsx) to analyze the chat data.")
