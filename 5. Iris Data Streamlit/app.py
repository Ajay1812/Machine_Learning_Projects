import streamlit as st
import pandas as pd
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Iris Flower Prediction

This App will give you the **Iris Flower** type!
""")

st.sidebar.header('User Input Parameters')

def user_input_features():
    sepal_length = st.sidebar.slider('Sepal length', 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider('Sepal width', 2.0, 4.0, 3.4)
    petal_length = st.sidebar.slider('Petal length', 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)
    data = {
            'sepal_length': sepal_length,
            'sepal_width' : sepal_width,
            'petal_length': petal_length,
            'petal_width' : petal_width
    }
    features = pd.DataFrame(data=data, index=[0])
    return features

df = user_input_features()

st.subheader('User Input Parameters')
st.write(df)

iris = datasets.load_iris()
X = iris.data
Y = iris.target

classifier = RandomForestClassifier()
classifier.fit(X,Y)

pred = classifier.predict(df)
pred_probabilty = classifier.predict_proba(df)

st.subheader('Class labels and their corresponding index numbers')
st.write(iris.target_names)

st.subheader('Prediction')
st.write(iris.target_names[pred])
#st.write(prediction)

st.subheader('Prediction Probability')
st.write(pred_probabilty)