import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('Startup Dashboard')
st.header('I am learning Streamlit')
st.subheader('And I am loving it')

st.write('This is a normal text')

st.markdown("""
### My favorite movies
- Jab We Met
- Mujhse Shaadi Karogi
- Chennai Express
""")

st.code("""
def foo(input):
    return foo**2

x = foo(2)
""")

st.latex('x^2 + y^2 + 2 = 0')

df = pd.DataFrame({
    'name': pd.Series(['Nitish', 'Ankit', 'Anupam']),
    'marks': pd.Series([50, 60, 70]),
    'package': pd.Series([10, 12, 14])
})

st.dataframe(df)

st.metric('Revenue', 'Rs 3L', '-3%')

st.json({
    'name': pd.Series(['Nitish', 'Ankit', 'Anupam']),
    'marks': pd.Series([50, 60, 70]),
    'package': pd.Series([10, 12, 14])
})

st.image('image.jpg')

st.sidebar.title('Sidebar ka Title')

col1, col2 = st.columns(2)

with col1:
    st.image('image.jpg')

with col2:
    st.image('image.jpg')

bar = st.progress(0)
for i in range(1, 101):
    bar.progress(i)

email = st.text_input('Enter email: ')
number = st.number_input('Enter age: ')
st.date_input('Enter Registration Date')


email = st.text_input('Enter email: ')
password = st.text_input('Enter password: ')
gender = st.selectbox('Select gender', ['male', 'female', 'others'])

btn = st.button('Login Karo')

# if the button is clicked

if btn:
    if email == 'vin@gmail.com' and password == '1234':
        st.success('Login Successful')
        st.balloons()
        st.write(gender)
    else:
        st.error('Login Failed')