import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(layout='wide')

# SQLite DB Setup
conn = sqlite3.connect('geoinformation_feedback.db')
c = conn.cursor()

# Function to read existing data from the SQLite database
def read_data(conn):
    df = pd.read_sql_query("SELECT * FROM population", conn)
    return df.dropna(how='all')  # Drop rows where all elements are missing.

existing_data = read_data(conn)
# st.dataframe(existing_data)
st.download_button('Download',existing_data.to_csv(),'data.csv')
st.dataframe(existing_data)