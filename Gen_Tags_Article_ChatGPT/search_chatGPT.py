#importing dependecies
import pandas as pd
import streamlit as st
import openai
import re

#import dataset
df = pd.read_csv('startups.csv')

# Removing null values based on (Startup Name) column
# data = df.dropna(subset=['Startup Name'], how='all')
data = df

openai.api_key = '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'


# Creating dropdown/search menu
st.subheader('RH Startup Data')
select = st.selectbox('Select Startup Name',data['company_short_name'],index=1)
# startup_button = st.button('Submit', type="primary")

# Tags for startups
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
        

st.markdown(list_of_startup_tags)
# List of tags for selected startup

# Selecting multiple tags for articles
selected_tags = st.selectbox('Choose tags from ChatGPT',list_of_startup_tags, index=2)
st.markdown(selected_tags)