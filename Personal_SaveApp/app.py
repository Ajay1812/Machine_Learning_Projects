import os 
import streamlit as st
import pandas as pd
# File processing packages
from PIL import Image
import docx2txt
# import textract
from PyPDF2 import PdfFileReader
import pdfplumber

import base64


@st.cache_data
def load_img(img_file):
    img = Image.open(img_file)
    return img

# Read Pdf file
def read_pdf(file):
    pdfReader = PdfFileReader(file)
    count = pdfReader.numPages
    all_page_text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        all_page_text += page.extractText()

    return all_page_text



# Function to save csv file to Saved/Dataset folder
def save_uploaded_file(uploadfile):
        with open(os.path.join('Saved/Datasets', uploadfile.name), 'wb') as f:
            f.write(uploadfile.getbuffer())
        return st.success(f'Saved file :"{uploadfile.name}" in Dataset Directory')

# Function to save PDF/Docs file Saved/PDF_DOCS folder 
def save_uploaded_file_pdf_docs(uploadfile):
        with open(os.path.join('Saved/Documents', uploadfile.name), 'wb') as f:
            f.write(uploadfile.getbuffer())
        return st.success(f'Saved file :"{uploadfile.name}" in Documents Directory')


def main():
    st.title('File Upload & Saved File to Directory App')

    menu = ['Images','Dataset','Documnets']
    st.sidebar.header('Upload!')
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Images':
        st.subheader('Upload Images')
        image_file = st.file_uploader('Upload an Image', type=['png','jpeg','jpg'])
        if image_file is not None:
            file_details = {'FileDetails': image_file.name, 'FileType': image_file.type}
            st.write(file_details)
            img = load_img(image_file)
            st.image(img,width=500) # Display the image file
            # Save Images to Dictory
            with open(os.path.join('Saved/Images',image_file.name), 'wb') as f:
                f.write(image_file.getbuffer())

            st.success('File Saved')
            



    elif choice == 'Dataset':
        st.subheader('Upload Dataset')
        dataFile = st.file_uploader('Upload a Dataset', type=['csv'])
        if dataFile is not None:
            file_details = {'FileDetails': dataFile.name, 'FileType': dataFile.type}
            st.write(file_details)
            df = pd.read_csv(dataFile)
            st.dataframe(df)
            save_uploaded_file(dataFile)


    elif choice == 'Documnets':
        st.subheader('Upload Document File')
        docx_file = st.file_uploader('Upload Documents', type=['pdf', 'docx','txt'])
        if st.button('Process'):
            if docx_file is not None:
                file_details = {'FileDetails': docx_file.name, 'FileType': docx_file.type}
                st.write(file_details)
                if docx_file.type == 'text/plain':
                    # Read as bytes
                    # raw_text = docx_file.read()
                    # st.write(raw_text) # Works in bytes
                    # Read as string (decode bytes to string)
                    raw_text = str(docx_file.read(), 'utf-8')
                    st.write(raw_text) # works
                    # st.text(raw_text) # works
                    save_uploaded_file_pdf_docs(docx_file)


                elif docx_file.type == 'application/pdf':

                    #using pdfplumber
                    # try:
                    #     with pdfplumber.open(docx_file) as pdf:
                    #         pages = pdf.pages[0]
                    #         st.write(pages.extract_text())
                    # except:
                    #     None

                    # using PyPDF
                    raw_text = read_pdf(docx_file)
                    st.write(raw_text)
                    save_uploaded_file_pdf_docs(docx_file)

                    # Try to display PDF on streamlit
                    # with open(docx_file,"rb") as f:
                    #     base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    #     pdf_display =  f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                    #     st.markdown(pdf_display, unsafe_allow_html=True)
                else:
                    raw_text = docx2txt.process(docx_file)
                    st.markdown(raw_text) 
                    # st.text(raw_text) 
                    save_uploaded_file_pdf_docs(docx_file)



main()