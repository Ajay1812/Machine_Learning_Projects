import streamlit as st
import pandas as pd
import requests
import time

headers = {
    "authorization": st.secrets["auth_token"],
    "content_type":"application/json"
}

BASE_URL = f'https://api.freecurrencyapi.com/v1/latest?apikey={headers}'

st.header("Currency Converter App 👻")

CURRENCIES =  [
    'EUR', 'USD', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON',
    'SEK', 'CHF', 'ISK', 'NOK', 'HRK', 'RUB', 'TRY', 'AUD', 'BRL', 'CAD',
    'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW', 'MXN', 'MYR', 'NZD', 'PHP',
    'SGD', 'THB', 'ZAR'
]
base_currency = st.selectbox(label='Select Base Currency', options=CURRENCIES)
base_amount = st.text_input("Enter your amount")

target_currencies = st.multiselect(label="Select Target Currencies", options=CURRENCIES)

if st.button("Click", type="secondary"):
    def get_exchange_rate(base_currency):
        currencies = ','.join(target_currencies)
        url = f'{BASE_URL}&base_currency={base_currency}&currencies={currencies}'
        # st.write(url)
        try:
            response = requests.get(url)
            data = response.json()
            return data['data']
        except:
            print("Invalid Currency.")
            return None
        
    def currency_converter(base_amount, base_currency):
        data_EX_rate=get_exchange_rate(base_currency)
        for i in data_EX_rate:
            data_EX_rate[i] = data_EX_rate[i]*float(base_amount)
            # st.write(converted_currency)
        return data_EX_rate



    with st.spinner(text='In progress'):
        time.sleep(1)
        col1, col2 = st.columns(2)
        with col1:
            st.write("Exchange Rate")
            exhange_rate = get_exchange_rate(base_currency=base_currency)
            exhange_rate_df = pd.DataFrame.from_dict(exhange_rate,orient='index', columns=['Exchange Rate'])
            st.table(exhange_rate_df)
        with col2:
            st.write("Converted Amount")
            converted_amount = currency_converter(base_amount, base_currency)
            converted_amount_df = pd.DataFrame.from_dict(converted_amount,orient='index', columns=['Converted Amount'])
            st.table(converted_amount_df)
        st.success('Done')

