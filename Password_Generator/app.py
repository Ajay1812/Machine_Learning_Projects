import streamlit as st
import random
import string
import time

st.set_page_config("Password Generator 🔐")

logo = "./Logo/logo.png"

st.title("Password Generator 🔐")
st.markdown("""
### About

Welcome to Password Generator 🔐 – your go-to solution for strong and secure passwords. Our app generates random and complex passwords, tailored to your needs. Enjoy a user-friendly interface, customizable options, and enhanced online security.

**How to Use:**
1. Set your preferences.
2. Click **Generate Password**.
3. Copy and use with confidence.

**Developer:**
**CodeNFInite**

**Feedback:**
Contact us at *a.kumar01c@gmail.com.*

Stay secure with Password Generator 🔐!

""")

st.sidebar.image(logo)
st.sidebar.markdown("# CodeNFInite")


with st.sidebar:
    
    punctuation = string.punctuation
    digits = string.digits
    whitespace = string.whitespace[0]
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    # generate_pass = st.multiselect("Generate Password", options=["Punctuation", "Digits", "Whitespace", "Letters"], default=["Letters", "Digits"])
    generate_pun = st.toggle("Punctuation")
    generate_dig = st.toggle("Digits")
    generate_white = st.toggle("Whitespace")
    generate_lower = st.toggle("Lower")
    generate_upper = st.toggle("Upper")
    # st.write(generate_pass)
    Length = st.slider(
        'Select a range of values',
        8, 64, step=4)

all_ = ""
if generate_pun:
    all_ += punctuation
if generate_dig:
    all_ += digits
if generate_white:
    all_ += whitespace
if generate_lower:
    all_ += lower
if generate_upper:
    all_ += upper


if st.button("Generate Password"):
    with st.spinner('please wait...'):
        time.sleep(1.2)
        password = "".join(random.choices(all_, k=Length))
    st.code(password)
    st.success('Done!')
