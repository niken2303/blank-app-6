import streamlit as st

st.title("Materi Kimia")

st.markdown("""
# Tabel Periodik

Tabel periodik adalah susunan unsur-unsur kimia berdasarkan nomor atom.
""")
st.title("Tabel Periodik")
import streamlit as st
import pandas as pd

df = pd.read_csv("data/elements.csv")

st.dataframe(df)
import streamlit as st
import pandas as pd

df = pd.read_csv("data/elements.csv")

st.title("Tabel Periodik")

cari = st.text_input("Cari unsur")

if cari:

    hasil = df[
        df["name"].str.contains(
            cari,
            case=False
        )
    ]

    st.dataframe(hasil)

else:

    st.dataframe(df)
  unsur = st.selectbox(
    "Pilih Unsur",
    df["name"]
)

detail = df[
    df["name"] == unsur
].iloc[0]

st.write("Nama:", detail["name"])
st.write("Simbol:", detail["symbol"])
st.write("Nomor Atom:", detail["atomic_number"])
st.write("Golongan:", detail["group"]) 
import streamlit as st

st.title("Kuis")

jawaban = st.radio(
    "Simbol Oxygen adalah?",
    ["O","H","N","C"]
)

if st.button("Periksa"):

    if jawaban == "O":

        st.success("Benar")

    else:

        st.error("Salah")
      if "score" not in st.session_state:
    st.session_state.score = 0
st.write(
    "Skor:",
    st.session_state.score
)
import streamlit as st
import random

data = {
    "O":"Oxygen",
    "H":"Hydrogen",
    "Na":"Sodium"
}

simbol = random.choice(
    list(data.keys())
)

jawaban = st.text_input(
    f"Apa nama unsur {simbol} ?"
)

if st.button("Cek"):

    if jawaban.lower() == data[simbol].lower():

        st.success("Benar")

    else:

        st.error(
            f"Jawaban benar {data[simbol]}"
        )
     import streamlit as st

score = st.session_state.get(
    "score",
    0
)

st.metric(
    "Nilai Quiz",
    score
) 
