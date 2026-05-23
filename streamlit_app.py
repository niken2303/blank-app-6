import pandas as pd
import streamlit as st

# 1. Konfigurasi Halaman & Tema Dasar
st.set_page_config(
    page_title="Tabel Periodik Modern", page_icon="🧪", layout="wide"
)

st.title("🧪 Tabel Periodik Unsur (Native Streamlit)")
st.write(
    "Dibuat menggunakan layouting kolom bawaan dokumentasi resmi Streamlit."
)

# Kustomisasi CSS agar tampilan tombol elemen berbentuk kotak presisi dan estetik
st.markdown(
    """
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        padding: 0px;
        font-weight: bold;
        font-size: 14px;
        border-radius: 5px;
    }
    /* Warna pembeda untuk informasi detail */
    .element-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #262730;
        border-left: 5px solid #FF4B4B;
    }
    </style>
""",
    unsafe_allow_allowed=True,
    # Jika versi streamlit kamu terbaru, gunakan parameter dasar:
    unsafe_allow_html=True,
)


# 2. Mengambil Data Unsur (Dataset Publik Resmi)
@st.cache_data
def load_periodic_data():
    url = "https://gist.github.com/GoodmanSciences/c2c7c06f5b8734b1e994/raw/23304cc5f2ea8b8466e3bfd41d176319213ef301/Periodic%2520Table%2520of%2520Elements.csv"
    return pd.read_csv(url)


df = load_periodic_data()

# Inisialisasi state untuk menyimpan elemen yang sedang diklik (fitur interaktif dokumentasi)
if "selected_element" not in st.session_state:
    st.session_state.selected_element = (
        "Hydrogen"  # Elemen default saat pertama dibuka
    )

# 3. Membuat Grid Tabel Periodik (18 Kolom Sesuai Golongan)
# Sesuai standard dokumentasi, kita bungkus di dalam container utama
with st.container():
    # Membuat 18 kolom horizontal
    cols = st.columns(18)

    # Lakukan perulangan untuk setiap Periode (Baris 1 sampai 7)
    for period in range(1, 8):
        # Ambil data unsur yang ada di periode ini
        current_period_df = df[df["Period"] == period]

        # Cek setiap Golongan (Kolom 1 sampai 18)
        for group in range(1, 19):
            # Cari apakah ada unsur di koordinat Baris & Kolom ini
            element_row = current_period_df[current_period_df["Group"] == group]

            with cols[group - 1]:  # Index kolom Python dimulai dari 0
                if not element_row.empty:
                    # Jika unsur ditemukan, ambil datanya
                    sym = element_row.iloc[0]["Symbol"]
                    num = element_row.iloc[0]["AtomicNumber"]
                    name = element_row.iloc[0]["Element"]

                    # Tampilkan tombol pembentuk kotak tabel periodik
                    # Menggunakan st.session_state untuk menangkap aksi klik
                    if st.button(f"{num}\n{sym}", key=f"btn_{sym}"):
                        st.session_state.selected_element = name
                else:
                    # Jika kosong (seperti celah di antara Hidrogen dan Helium), tampilkan teks kosong agar layout rapi
                    st.write("")

# 4. Panel Informasi Detail (Tampil di bagian bawah tabel)
st.markdown("---")
st.header("🔍 Detail Informasi Unsur")

# Mengambil data dari elemen yang sedang aktif di session_state
selected_name = st.session_state.selected_element
element_info = df[df["Element"] == selected_name].iloc[0]

# Tampilan Card Detail menggunakan HTML+CSS di Streamlit
st.markdown(
    f"""
    <div class="element-box">
        <h2>{element_info['Element']} ({element_info['Symbol']})</h2>
        <p><b>Kategori Unsur:</b> {element_info['Type']} | <b>Fase Wujud:</b> {element_info['Phase']}</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Menampilkan statistik angka menggunakan komponen st.metric bawaan Streamlit
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Nomor Atom", value=int(element_info["AtomicNumber"]))
with col2:
    st.metric(label="Massa Atom", value=f"{element_info['AtomicMass']} u")
with col3:
    st.metric(label="Periode", value=int(element_info["Period"]))
with col4:
    st.metric(label="Golongan", value=int(element_info["Group"]))

# Detail Tambahan teks menggunakan st.help atau st.code untuk konfigurasi elektron
st.subheader("Konfigurasi Elektron")
st.code(element_info["ElectronConfiguration"], language="bash")
