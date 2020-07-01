import streamlit as st
import pandas as pd

st.title('Job ETL Dashboard')
st.text("TopN word frequency")

def load_data(df):
    df.rename(columns={'WordFrequency':'index'}).set_index('index')
    st.line_chart(df)

# Todo: chart of avg. salary