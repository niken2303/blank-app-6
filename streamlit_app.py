import pandas as pd
import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA (STYLING)
# ==============================================================================
# Mengatur halaman agar melebar penuh (wide mode) untuk memuat 18 kolom golongan
st.set_page_config(
    page_title="Tabel Periodik Unsur", page_icon="🧪", layout="wide"
)

# Kustomisasi CSS lewat Markdown untuk mengubah tombol default menjadi kotak presisi
st.markdown(
    """
    <style>
    /* Mengubah tombol elemen menjadi bentuk kotak seragam */
    div.stButton > button {
        width: 100%;
        height: 65px;
        padding: 0px;
        font-weight: bold;
        font-size: 13px;
        border-radius: 6px;
        border: 1px solid #4a4a4a;
        line-height: 1.2;
        background-color: #262730;
        color: #ffffff;
        transition: all 0.2s ease-in-out;
    }
    
    /* Efek saat kursor diarahkan ke tombol */
    div.stButton > button:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
        transform: scale(1.05);
    }

    /* Kotak informasi detail elemen di bagian bawah */
    .element-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #1e1e24;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🧪 Tabel Periodik Unsur Interaktif")
st.write(
    "Klik pada kotak elemen untuk melihat informasi detail dan karakteristik kimianya di panel bawah."
)
st.markdown("---")

# ==============================================================================
# 2. MEMUAT DATA DATABASE UNSUR (CACHED)
# ==============================================================================
# Fungsi di-cache agar data tidak di-download ulang setiap kali tombol diklik
@st.cache_data
def load_periodic_data():
    # Mengambil database resmi 118 elemen dalam format CSV dari repositori publik
    url = "https://gist.github.com/GoodmanSciences/c2c7c06f5b8734b1e994/raw/23304cc5f2ea8b8466e3bfd41d176319213ef301/Periodic%2520Table%2520of%2520Elements.csv"
    return pd.read_csv(url)


# Menyimpan data ke dalam variabel DataFrame (df)
df = load_periodic_data()

# Inisialisasi memori jangka pendek (session_state) untuk menyimpan elemen terpilih
if "selected_element" not in st.session_state:
    st.session_state.selected_element = (
        "Hydrogen"  # Elemen default saat pertama kali dibuka
    )

# ==============================================================================
# 3. MERENDER GRID TABEL PERIODIK (18 KOLOM)
# ==============================================================================
with st.container():
    # Membuat 18 kolom vertikal sesuai jumlah golongan tabel periodik
    cols = st.columns(18)

    # Perulangan untuk mengecek Baris/Periode (1 sampai 7)
    for period in range(1, 8):
        # Memfilter data yang hanya berada di periode aktif saat ini
        current_period_df = df[df["Period"] == period]

        # Perulangan untuk mengecek Kolom/Golongan (1 sampai 18)
        for group in range(1, 19):
            # Mencari apakah ada unsur kimia di koordinat Periode & Golongan ini
            element_row = current_period_df[current_period_df["Group"] == group]

            # Mengaktifkan kolom tujuan (Python menggunakan indeks berbasis 0, maka group - 1)
            with cols[group - 1]:
                if not element_row.empty:
                    # Ambil data spesifik unsur jika ditemukan
                    sym = element_row.iloc[0]["Symbol"]
                    num = element_row.iloc[0]["AtomicNumber"]
                    name = element_row.iloc[0]["Element"]

                    # Tampilkan tombol kotak elemen. \n digunakan untuk membuat baris baru di dalam tombol.
                    if st.button(f"{num}\n{sym}", key=f"btn_{sym}"):
                        # Jika diklik, update nama elemen di dalam memori aplikasi
                        st.session_state.selected_element = name
                else:
                    # Jika tidak ada unsur di koordinat tersebut, biarkan kosong agar spasi layout tetap rapi
                    st.write("")

st.markdown("---")

# ==============================================================================
# 4. PANEL INFORMASI DETAIL UNSUR YANG TERPILIH
# ==============================================================================
st.header("🔍 Detail Karakteristik Unsur")

# Mengambil data dari elemen yang namanya sedang tersimpan di memori (session_state)
selected_name = st.session_state.selected_element
element_info = df[df["Element"] == selected_name].iloc[0]

# Menampilkan Banner Nama Unsur dengan gaya CSS kustom
st.markdown(
    f"""
    <div class="element-box">
        <h2 style='margin:0; color:#FF4B4B;'>{element_info['Element']} ({element_info['Symbol']})</h2>
        <p style='margin:5px 0 0 0; opacity:0.8;'><b>Kategori:</b> {element_info['Type']} | <b>Wujud Zat (STP):</b> {element_info['Phase']}</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Membagi informasi angka/metrik utama menjadi 4 kolom berjejer
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="Nomor Atom", value=int(element_info["AtomicNumber"]))
with m_col2:
    st.metric(label="Massa Atom", value=f"{element_info['AtomicMass']} u")
with m_col3:
    st.metric(label="Golongan (Group)", value=int(element_info["Group"]))
with m_col4:
    st.metric(label="Periode (Period)", value=int(element_info["Period"]))

# Menampilkan informasi detail sekunder di bagian paling bawah
st.markdown("### 🧬 Informasi Tambahan")
info_col1, info_col2 = st.columns(2)

with info_col1:
    st.write(f"**Radius Atom:** {element_info['AtomicRadius']} Å")
    st.write(f"**Elektronegativitas:** {element_info['Electronegativity']}")
    st.write(f"**Titik Leleh:** {element_info['MeltingPoint']} K")

with info_col2:
    st.write(f"**Titik Didih:** {element_info['BoilingPoint']} K")
    st.write(f"**Kepadatan (Density):** {element_info['Density']} g/cm³")
    st.write(f"**Tahun Ditemukan:** {element_info['YearIntroduced']}")

# Menampilkan konfigurasi elektron dengan format box code komputer
st.write("**Konfigurasi Elektron:**")
st.code(element_info["ElectronConfiguration"], language="bash")
st.subheader("Konfigurasi Elektron")
st.code(element_info["ElectronConfiguration"], language="bash")
