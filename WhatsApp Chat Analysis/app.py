import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt


st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue() #its a byte data stream
    st.sidebar.success('File Uploaded')

    # So we have to convert byte data into string
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')

    user_list.sort() # sort in ascending order in userlist
    user_list.insert(0, 'Overall') 

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):

        #Stats Area
        num_messages, words,num_media_messages, links = helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)   
        with col4:
            st.header("Total Links")
            st.title(links)      

        # Timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color = 'g')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Finding the busiest user in the group
        if selected_user == 'Overall':
            st.title('Most Busy User')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color ='r')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        #WordCloud
        df_wc = helper.create_wordcloud(selected_user, df) 
        st.title('Word Cloud')
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words
        most_common_df = helper.most_common_words(selected_user,df)
        st.title('Most Common Words')

        fig,ax = plt.subplots()
        plt.xticks(rotation = 'vertical')
        
        ax.bar(most_common_df[0],most_common_df[1], color=['red', 'yellow', 'black', 'blue', 'orange','green','pink'])
        # ax.barh(most_common_df[0],most_common_df[1], color=['red', 'yellow', 'black', 'blue', 'orange','green','pink'])
        st.pyplot(fig)
        # st.dataframe(most_common_df)


        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title('Emojis Analysis')

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct="%0.2f")    
            st.pyplot(fig)