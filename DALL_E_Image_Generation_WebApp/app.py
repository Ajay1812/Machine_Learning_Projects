import openai
import urllib.request
from PIL import Image
import streamlit as st
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://ajay1812-machine-learn-dall-e-image-generation-webappapp-4fc4na.streamlit.app/"

def generate_image(image_description):
    
    img_response = openai.Image.create(
        prompt = image_description,
        n = 1,
        size = '512x512' # 256x256 512x512 1024x1024
    )

    img_url = img_response['data'][0]['url']

    urllib.request.urlretrieve(img_url, 'image.png')

    image = Image.open('image.png')

    return image

# Page title 
st.title('DALL-E Image Generation App 👦🏻')

# input text for image recoginition
image_description = st.text_input('Image Description')

if st.button('Generate Image'):
    generate_image = generate_image(image_description)
    st.image(generate_image)
