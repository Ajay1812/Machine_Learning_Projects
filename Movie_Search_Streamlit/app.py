import streamlit as st
import requests
from api import movieApi

st.title('Movie Search App!')
title = st.text_input('**User Input**')
st.write('#')
if title:
    try:
        url = f'https://www.omdbapi.com/?t={title}&apikey={movieApi}'
        r = requests.get(url)
        r = r.json()
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(r['Poster'])
        with col2:    
            st.subheader(r['Title'])
            st.caption(f"Genre: {r['Genre']} Year: {r['Year']}")
            st.write(r['Plot'])
            st.subheader(f"IMDB Rating: {r['imdbRating']}")
            st.progress(float(r['imdbRating'])/10)

    except:
        st.error("Movie doesn't exist")
