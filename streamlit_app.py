import pandas as pd
import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA (STYLING)
# ==============================================================================
st.set_page_config(
    page_title="Tabel Periodik Unsur", page_icon="🧪", layout="wide"
)

# Kustomisasi CSS lewat Markdown untuk merapikan tampilan tombol elemen
st.markdown(
    """
    <style>
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
    
    div.stButton > button:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
        transform: scale(1.05);
    }

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
@st.cache_data
def load_periodic_data():
    url = "https://gist.github.com/GoodmanSciences/c2c7c06f5b8734b1e994/raw/23304cc5f2ea8b8466e3bfd41d176319213ef301/Periodic%2520Table%2520of%2520Elements.csv"
    data = pd.read_csv(url)
    # Mengisi semua nilai kosong (NaN) dengan string strip '-' agar tidak menyebabkan error
    return data.fillna("-")


df = load_periodic_data()

# Inisialisasi memori jangka pendek (session_state)
if "selected_element" not in st.session_state:
    st.session_state.selected_element = "Hydrogen"

# ==============================================================================
# 3. MERENDER GRID TABEL PERIODIK (18 KOLOM)
# ==============================================================================
with st.container():
    cols = st.columns(18)

    for period in range(1, 8):
        current_period_df = df[df["Period"] == period]

        for group in range(1, 19):
            element_row = current_period_df[current_period_df["Group"] == group]

            with cols[group - 1]:
                if not element_row.empty:
                    sym = element_row.iloc[0]["Symbol"]
                    num = element_row.iloc[0]["AtomicNumber"]
                    name = element_row.iloc[0]["Element"]

                    # Mengubah format nomor atom menjadi integer yang aman untuk string teks tombol
                    num_display = int(num) if isinstance(num, (int, float)) else num

                    if st.button(f"{num_display}\n{sym}", key=f"btn_{sym}"):
                        st.session_state.selected_element = name
                else:
                    st.write("")

st.markdown("---")

# ==============================================================================
# 4. PANEL INFORMASI DETAIL UNSUR YANG TERPILIH
# ==============================================================================
st.header("🔍 Detail Karakteristik Unsur")

selected_name = st.session_state.selected_element
element_info = df[df["Element"] == selected_name].iloc[0]

# Tampilan Banner Nama Unsur
st.markdown(
    f"""
    <div class="element-box">
        <h2 style='margin:0; color:#FF4B4B;'>{element_info['Element']} ({element_info['Symbol']})</h2>
        <p style='margin:5px 0 0 0; opacity:0.8;'><b>Kategori:</b> {element_info['Type']} | <b>Wujud Zat (STP):</b> {element_info['Phase']}</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Pembersihan format data angka untuk tampilan st.metric agar terhindar dari tipe data pecahan (.0)
def clean_int(val):
    try:
        return str(int(float(val)))
    except:
        return str(val)

# Membagi informasi angka menjadi 4 kolom berjejer
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="Nomor Atom", value=clean_int(element_info["AtomicNumber"]))
with m_col2:
    st.metric(label="Massa Atom", value=f"{element_info['AtomicMass']} u")
with m_col3:
    st.metric(label="Golongan (Group)", value=clean_int(element_info["Group"]))
with m_col4:
    st.metric(label="Periode (Period)", value=clean_int(element_info["Period"]))

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

# Menampilkan konfigurasi elektron
st.write("**Konfigurasi Elektron:**")
st.code(element_info["ElectronConfiguration"], language="bash")
