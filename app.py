import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyser")

st.set_page_config(layout="wide")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessing(data)

    st.dataframe(df)

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
