import pandas as pd
import streamlit as st
df = pd.read_feather('db.feather')

col1, col2, col3 = st.columns([1, 1, 1])
name = col1.text_input("Enter your name: ")
username = col2.text_input("Enter your username: ")
password = col3.text_input("Enter your password: ")

if st.button('Add User'):
    df2 = {'name': name, 'username': username, 'password': password}
    df = df.append(df2, ignore_index = True).reset_index(drop=True)
else:
    st.write('Goodbye')

df.to_feather('db.feather')
st.dataframe(df.loc[:,['name','username']])

