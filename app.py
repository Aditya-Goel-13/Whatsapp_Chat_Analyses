import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import plotly.graph_objects as go
st.sidebar.title("Whatsapp Chat Analyser")

st.set_page_config(layout="wide")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessing(data)

    #fetch unique user

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analyses wrt", user_list)

    if st.sidebar.button("Show Analyses"):
        col1, col2, col3, col4= st.columns(4)
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        if selected_user == "Overall":
            st.title("Most Active Users")
            x, new_df = helper.fetch_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #word cloud
        st.title("Wordcloud")
        df_wc, most_common_words = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common word
        st.title("Most Common Words")
        fig, ax = plt.subplots()
        print(most_common_words)
        ax.barh(most_common_words[0], most_common_words[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Emoji analyses
        st.title("Emojis Analysis")
        col1, col2 = st.columns(2)
        with col1:
            emoji_df = helper.emoji_counter(selected_user, df)
            st.dataframe(emoji_df)

        with col2:
            # fig, ax = plt.subplots()
            # ax.pie(emoji_df['count'].head(7), labels=emoji_df['emoji'].head(7))
            # st.pyplot(fig)
            fig = go.Figure(data=[go.Pie(labels=emoji_df['emoji'].head(7), values=emoji_df['count'].head(7), textinfo='label+percent', textfont=dict(size=24), textposition='inside', showlegend=False)])
            fig.update_layout(width=500, height=500)
            st.plotly_chart(fig)
