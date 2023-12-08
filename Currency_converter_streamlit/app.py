import streamlit as st
import pandas as pd
import requests
import time

headers = {
    "authorization": st.secrets["API_KEY"],
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
        try:
            response = requests.get(url)
            data = response.json()
            return data['data']
        except:
            print("Invalid Currency.")
            return None
        
    def currency_converter(base_amount, base_currency):
        data_EX_rate = get_exchange_rate(base_currency)
        if data_EX_rate is not None:  # Check if data_EX_rate is not None
            for i in data_EX_rate:
                data_EX_rate[i] = data_EX_rate[i] * float(base_amount)
            return data_EX_rate
        else:
            return None

    with st.spinner(text='In progress'):
        time.sleep(1)
        col1, col2 = st.columns(2)
        with col1:
            st.write("Exchange Rate")
            exchange_rate = get_exchange_rate(base_currency=base_currency)
            if exchange_rate is not None:  # Check if exchange_rate is not None
                exchange_rate_df = pd.DataFrame.from_dict(exchange_rate, orient='index', columns=['Exchange Rate'])
                st.table(exchange_rate_df)
            else:
                st.warning("Failed to retrieve exchange rates.")
        with col2:
            st.write("Converted Amount")
            converted_amount = currency_converter(base_amount, base_currency)
            if converted_amount is not None:  # Check if converted_amount is not None
                converted_amount_df = pd.DataFrame.from_dict(converted_amount, orient='index', columns=['Converted Amount'])
                st.table(converted_amount_df)
            else:
                st.warning("Failed to convert amounts.")
        st.success('Done')
