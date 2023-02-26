#importing dependecies
import pandas as pd
import streamlit as st
import openai
import re
import numpy as np


# Set the API key for the Chat GPT
openai.api_key = "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"

#import dataset
df = pd.read_csv('startups.csv')

data = df
# Removing null values based on (Startup Name) column
# data = df.dropna(subset=['Startup Name'], how='all')

# Creating dropdown/search menu
st.subheader('RH Startup Data')
select = st.selectbox('Select Startup Name',data['company_short_name'],index=1)

tag_prompt = f'give me list of 10 important tags or keywords related {select} startup.'

response_tags = openai.Completion.create(
engine="text-davinci-003",
prompt= tag_prompt,
max_tokens=1024,
n=1,
temperature=0.5)

# Selecting multiple tags for articles
multi_tags = response_tags['choices'][0]['text']

text = multi_tags
pattern = re.compile(r"\d+\.(.*)")
matches = pattern.findall(text)

list_of_startup_tags = []
for match in matches:
    list_of_startup_tags.append(match.strip())
        

st.markdown(multi_tags)

pd.DataFrame(list_of_startup_tags)

if list_of_startup_tags:
    # List of tags for selected startup 
    list_of_selected_tags = st.selectbox("Choose a tag from ChatGPT",list_of_startup_tags)


# Submit button
button = st.checkbox('Check',label_visibility="visible")


# Select country column for tagging it will provide the better result in article
HQ_country = data['city']

if button is True:

    # Displaying Table for selected Startup
    # st.table(data[data['company_short_name'] == select])  

    # website = data[data['linked_in_company_page'] == select]
    
    col1, col2 = st.columns(2,gap="large")
    
    st.markdown('Defaults RH Dataset')

    dataframe_1 = data[['company_short_name','company_description', 'owner']]
    details = st.table(dataframe_1[dataframe_1['company_short_name']==select])
    # if dataframe_1['company_short_name'] == select:

    # with col1:
    #     # Using Regular expression for extract email from the text
    #     text = display
    #     text = str(text)
    #     urls = re.findall(r'(https?://[^\s]+)', text)
    #     urls = urls[0]
    #     # print(urls)
    #     # st.markdown("['sda'](urls)")
    #     st.markdown(urls)


    #     # storing linkedin column to display_lurl
    #     display_lurl = display['Linkedin URL']

    #     text = display_lurl
    #     text = str(text)
    #     url = re.findall(r'(https?://[^\s]+)', text)
    #     url = url[0]
    #     st.markdown(url)

    # with col2:

    #     founder = display['Founder Name'].to_string()
    #     st.markdown(founder[2 : ])

    #     text = display['Contact Email']
    #     text = str(text)
    #     email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    #     email = email[0]
    #     st.markdown(email)


    msg = f"Tell me somthing about {select} startup in 50 words: \n"

    # Set the API key for the Chat GPT
    openai.api_key = "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"

    # Define the prompt for the Chat GPT
    prompt = msg

    # Generate a response from the Chat GPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt= prompt,
        max_tokens=1024,
        n=1,
        temperature=0.1)
#----------------------------------------------------------------
    Founder = f"Tell me who are the Founder/Owner of {select}? \n"
    st.markdown(Founder)
    st.subheader('Founder')

    # Set the API key for the Chat GPT
    openai.api_key = "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"

    # Generate a response from the Chat GPT
    response_Founder = openai.Completion.create(
        engine="text-davinci-003",
        prompt= Founder,
        max_tokens=1024,
        n=1,
        temperature=0.1)

    #Displaying response from Chat GPT
    st.markdown(response_Founder['choices'][0]['text'])
#-------------------------------------------------------------------

    # Displaying response from Chat GPT
    About = f"Tell me somthing about {select} startup in 50 words: \n"
    st.markdown(About)
    st.subheader(f'About {select}')
    st.markdown(response['choices'][0]['text'])

#---------------------------------------------------------------------

#-----------------------------------------------------------------
    
    select = str(select)
    HQ_country = data.loc[(data.company_short_name == select)].city.values[0]
    # HQ_country = df[df['city'] == df['company_short_name']]
    # aricle_tags= st.selectbox('')  topic is **{aricle_tags}**
    article= f'write an article about {select} startup headquatered in {HQ_country} using these keywords {list_of_selected_tags} and use bold **headings** and italic **sub-headings**.'

    response_article = openai.Completion.create(
    engine="text-davinci-003",
    prompt= article,
    max_tokens=1024,
    n=1,
    temperature=0.5)

#--------------------------------------------------------------------
    # Displaying response from Chat GPT
    st.markdown(article)
    st.header(f'Article:')
    st.markdown(response_article['choices'][0]['text'])

