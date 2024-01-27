import requests
import json
# import config
import streamlit as st
from streamlit_card import card
import base64
from streamlit_option_menu import option_menu
from rembg import remove
from PIL import Image
from io import BytesIO
from datetime import datetime

def display(thumbnail,url):
    cards = card(
    title="",
    text="",
    image=f"{thumbnail}",
    url=f"{url}",
    styles={
        "card": {
            "width": "390px",
            "height": "450px",
            "border-radius": "40px",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)"
            },
        "filter":{
            "background-color": "rgb(0, 0, 0, 0)"
        }
    }
)
    return cards

headers = {
    'authorization':st.secrets["API_KEY"],
}


def get_image(search,page):
    # response = requests.get(f"https://api.unsplash.com/search/photos?page={page}&per_page=12&query={search}&client_id={config.api_access_key}")
    response = requests.get(f"https://api.unsplash.com/search/photos?page={page}&per_page=12&query={search}&client_id={headers['authorization']}")
    # response = requests.get(f"https://api.unsplash.com/search/photos?page={page}&per_page=12&query={search}", headers=headers)
    data = response.json()
    return data


def main():
    st.set_page_config("Unsplash Photo Gallery",initial_sidebar_state="collapsed",layout="wide")


    selected = option_menu(
        menu_title=None,
        options=["Gallery App", "Background Remover", "About"],
        icons=["book","book","house"],
        menu_icon=["cast"],
        default_index=0,
        orientation='horizontal',
    )

    if selected == "Gallery App":
        st.title("Unsplash Photo Gallery 🌄")
        st.write("Welcome to the Unsplash Photo Search app! Enter a search term to find beautiful photos.")
        if 'page' not in st.session_state:
            st.session_state.page = 1
        search = st.text_input("Search")
        data = get_image(search,st.session_state.page)

        height = 400
        width = 600
        col1, col2, col3 = st.columns(3)
        for i, result in enumerate(data['results']):
            urls = result['urls']
            full_url = urls['full']
            thumbnail = urls['thumb'] + f'&q={height}&w={width}'
            
            if i % 3 == 0:
                with col1:
                    display(thumbnail, full_url)
            elif i % 3 == 1:
                with col2:
                    display(thumbnail, full_url)
            else:
                with col3:
                    display(thumbnail, full_url)

        st.markdown(
        """
        <style>
            div[data-testid="column"]:nth-of-type(1)
            {
            } 
            div[data-testid="column"]:nth-of-type(2)
            {
                text-align: end;
            } 
        </style>
        """,unsafe_allow_html=True
        )

        prev, next = st.columns(2)
        with prev:
            previous_btn = st.button("Prev Page")
            if previous_btn:
                st.session_state.page -= 1
        # get_image(search,st.session_state.page)
        with next:
            next_btn = st.button("Next Page")
            if next_btn:
                st.session_state.page += 1
        # get_image(search,st.session_state.page)
    
    if selected == "Background Remover":
        st.markdown("# Background Remover App 🎆")

        st.markdown("Effortlessly remove backgrounds with precision. Transform photos instantly. Elevate your visuals with our intuitive Background Remover App!")
        # st.write("##")
        st.write("### Upload and download :gear:")
        my_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

        MAX_FILE_SIZE = 5 * 1024 * 1024

        def convert_image(img):
            buf = BytesIO()
            img.save(buf, format="PNG")
            byte_img = buf.getvalue()
            return byte_img


        def remove_background(upload):
            image = Image.open(upload)
            col1.write("Original Image :camera:")
            col1.image(image)

            fixed = remove(image)
            col2.write("Fixed Image :wrench:")
            col2.image(fixed)
            st.markdown("\n")
            current_datetime = datetime.now().date()
            st.download_button("Download fixed image", convert_image(fixed), f"{current_datetime}_fixed.png", "image/png")

        col1,col2 = st.columns(2)
        if my_upload is not None:
            if my_upload.size > MAX_FILE_SIZE:
                st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
            else:
                remove_background(upload=my_upload)
        else:
            remove_background("images/img1.jpg")
    
    if selected == "About":
        logo = "images/logo.png"
        portfolio_url = "https://codenfinite.streamlit.app"
        twitter_gif = "images/icons8-twitter.gif"
        twitter_url = "https://twitter.com/Code_NFInite"
        github_gif = "images/icons8-github.gif"
        github_url = "https://github.com/Ajay1812"

        st.markdown("# About")
        # st.markdown("*A simple project leveraging the Unsplash API to fetch and showcase high-quality photos. Unsplash's vast collection of free, high-resolution images enhances the app's visual appeal and versatility for various purposes.*")
        st.markdown("##### *I'm **Ajay Kumar**, a passionate data analyst who is excited about leveraging data to gain insights and drive informed decision-making. As a fresher in the field, I am eager to apply my skills and contribute to meaningful data-driven projects. I am motivated to learn and grow in the dynamic field of data analysis.*")

        st.markdown("""
            ## 🛠 Skills
            - Data analysis and visualization
            - SQL And Python
            - Machine learning and Statistical analysis
            - Data cleaning and preprocessing
            - Creating interactive dashboards
                    """)

        col_1,col_2,col_3 = st.columns(3)
        with col_1:
            with open(logo, "rb") as f:
                logo_data = f.read()
            encoded_logo = base64.b64encode(logo_data).decode()
            width = 190
            height = 150
            link_code =f'<a href="{portfolio_url}" target="_blank"><img src="data:image/png;base64,{encoded_logo}" style="width:{width}px;height:{height}px;"></a>'
            st.markdown(link_code, unsafe_allow_html=True)

        with col_2:
            with open(twitter_gif, "rb") as f:
                gif_data = f.read()
            encoded_gif = base64.b64encode(gif_data).decode()
            link_code = f'<a href="{twitter_url}" target="_blank"><img src="data:image/gif;base64,{encoded_gif}" style="width:110px;height:110px;"></a>'
            st.markdown(link_code, unsafe_allow_html=True)

        with col_3:
            with open(github_gif, "rb") as f:
                gif_data = f.read()
            encoded_gif = base64.b64encode(gif_data).decode()
            link_code = f'<a href="{github_url}" target="_blank"><img src="data:image/gif;base64,{encoded_gif}" style="width:130px;height:130px;"></a>'
            st.markdown(link_code, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
