import streamlit as st
import preprocess
import Helper
import matplotlib.pyplot as plt
import emoji
from wordcloud import WordCloud
import seaborn as sns
st.sidebar.title('Whatsapp Chat Analysis')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    dataset = preprocess.pre(data)
    st.dataframe(dataset)
    
    user_list = dataset['Sender'].unique().tolist()
    if 'Group Notification' in user_list:
        user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox('Show Analysis wrt', user_list)
    
    if st.sidebar.button("Show Analysis"):
        st.write(f"Selected User: {selected_user}")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write("Total Messages")
            num_messages = Helper.fetch_stats(selected_user, dataset)
            st.write(num_messages)
        with col2:
            st.write("Total Words")
            st.write(Helper.words(selected_user, dataset))
        with col3:
            st.write("Total Media Shared")
            st.write(Helper.media_shared(selected_user, dataset))
        with col4:
            st.write("Total Urls")
            st.write(Helper.url_extr(selected_user, dataset))
        st.title("Monthly Timeline")
        timeline = Helper.monthly_timeline(selected_user,dataset)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = Helper.daily_timeline(selected_user, dataset)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Date'], daily_timeline['Message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = Helper.week_activity_map(selected_user,dataset)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = Helper.month_activity_map(selected_user, dataset)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = Helper.activity_heatmap(selected_user,dataset)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = Helper.busy_users(dataset)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        if selected_user == "Overall":
            st.title("Top Busy Users")
            x, new_dataset = Helper.busy_users(dataset)
            fig, ax = plt.subplots()
            col1, col2,col3 = st.columns(3)
            names = x.index
            with col1:
                values = x.values
                ax.bar(names, values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig, ax)
            with col2:
                st.dataframe(new_dataset)
            # with col3:
            #     emoji_dataset = Helper.emoji_helper(selected_user, dataset)
            #     st.dataframe(emoji_dataset)
        st.title("Wordcloud")
        df_wc = Helper.create_wordcloud(selected_user,dataset)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = Helper.most_common_words(selected_user,dataset)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        # emoji_df = Helper.emoji_helper(selected_user,dataset)
        # st.title("Emoji Analysis")

        # col1,col2 = st.columns(2)

        # with col1:
        #     st.dataframe(emoji_df)
        # with col2:
        #     fig,ax = plt.subplots()
        #     ax.pie(emoji_dataset['count'].head(),labels=emoji_dataset['emoji'].head(),autopct="%0.2f")
        #     st.pyplot(fig)

# pandas 2.2.2
# numpy 1.26.4
# matplotlib 3.9.1
# emoji 2.12.1
# wordcloud 1.9.3
# seaborn 0.13.2
# urlextract 1.9.0
# joblib 1.4.2
# streamlit 1.36.0
# skikit_learn 1.5.1
