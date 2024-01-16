import random
import string
import streamlit as st


Length = int(input("Length of your password? "))

# all_ = "".join(string.punctuation + string.digits + string.ascii_letters + string.whitespace)
all_ = "".join(string.punctuation)
print(all_)

password = "".join(random.choices(all_,k=Length))
print(password)