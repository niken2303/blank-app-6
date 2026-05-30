import streamlit as st

st.title("Aplikasi Pembelajaran Tabel Periodik")

st.write("Selamat datang")
import streamlit as st
import pandas as pd

st.title("Tabel Periodik")

df = pd.read_csv("data/elements.csv")

st.dataframe(df)
