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
# 2. DATA LOKAL (MANDIRI & BEBAS HTTP ERROR)
# ==============================================================================
@st.cache_data
def load_local_data():
    # Memasukkan data langsung agar aplikasi tidak bergantung pada internet/URL eksternal
    raw_data = [
        # Periode 1
        {"AtomicNumber": 1, "Symbol": "H", "Element": "Hydrogen", "AtomicMass": "1.008", "Period": 1, "Group": 1, "Type": "Reactive Nonmetal", "Phase": "Gas", "ElectronConfiguration": "1s¹"},
        {"AtomicNumber": 2, "Symbol": "He", "Element": "Helium", "AtomicMass": "4.0026", "Period": 1, "Group": 18, "Type": "Noble Gas", "Phase": "Gas", "ElectronConfiguration": "1s²"},
        # Periode 2
        {"AtomicNumber": 3, "Symbol": "Li", "Element": "Lithium", "AtomicMass": "6.94", "Period": 2, "Group": 1, "Type": "Alkali Metal", "Phase": "Solid", "ElectronConfiguration": "[He] 2s¹"},
        {"AtomicNumber": 4, "Symbol": "Be", "Element": "Beryllium", "AtomicMass": "9.0122", "Period": 2, "Group": 2, "Type": "Alkaline Earth Metal", "Phase": "Solid", "ElectronConfiguration": "[He] 2s²"},
        {"AtomicNumber": 5, "Symbol": "B", "Element": "Boron", "AtomicMass": "10.81", "Period": 2, "Group": 13, "Type": "Metalloid", "Phase": "Solid", "ElectronConfiguration": "[He] 2s² 2p¹"},
        {"AtomicNumber": 6, "Symbol": "C", "Element": "Carbon", "AtomicMass": "12.011", "Period": 2, "Group": 14, "Type": "Reactive Nonmetal", "Phase": "Solid", "ElectronConfiguration": "[He] 2s² 2p²"},
        {"AtomicNumber": 7, "Symbol": "N", "Element": "Nitrogen", "AtomicMass": "14.007", "Period": 2, "Group": 15, "Type": "Reactive Nonmetal", "Phase": "Gas", "ElectronConfiguration": "[He] 2s² 2p³"},
        {"AtomicNumber": 8, "Symbol": "O", "Element": "Oxygen", "AtomicMass": "15.999", "Period": 2, "Group": 16, "Type": "Reactive Nonmetal", "Phase": "Gas", "ElectronConfiguration": "[He] 2s² 2p⁴"},
        {"AtomicNumber": 9, "Symbol": "F", "Element": "Fluorine", "AtomicMass": "18.998", "Period": 2, "Group": 17, "Type": "Reactive Nonmetal", "Phase": "Gas", "ElectronConfiguration": "[He] 2s² 2p⁵"},
        {"AtomicNumber": 10, "Symbol": "Ne", "Element": "Neon", "AtomicMass": "20.180", "Period": 2, "Group": 18, "Type": "Noble Gas", "Phase": "Gas", "ElectronConfiguration": "[He] 2s² 2p⁶"},
        # Periode 3
        {"AtomicNumber": 11, "Symbol": "Na", "Element": "Sodium", "AtomicMass": "22.990", "Period": 3, "Group": 1, "Type": "Alkali Metal", "Phase": "Solid", "ElectronConfiguration": "[Ne] 3s¹"},
        {"AtomicNumber": 12, "Symbol": "Mg", "Element": "Magnesium", "AtomicMass": "24.305", "Period": 3, "Group": 2, "Type": "Alkaline Earth Metal", "Phase": "Solid", "ElectronConfiguration": "[Ne] 3s²"},
        {"AtomicNumber": 13, "Symbol": "Al", "Element": "Aluminum", "AtomicMass": "26.982", "Period": 3, "Group": 13, "Type": "Post-Transition Metal", "Phase": "Solid", "ElectronConfiguration": "[Ne] 3s² 3p¹"},
        {"AtomicNumber": 14, "Symbol": "Si", "Element": "Silicon", "AtomicMass": "28.085", "Period": 3, "Group": 14, "Type": "Metalloid", "Phase": "Solid", "ElectronConfiguration": "[Ne] 3s² 3p²"},
        {"AtomicNumber": 15, "Symbol": "P", "Element": "Phosphorus", "AtomicMass": "30.974", "Period": 3, "Group": 15, "Type": "Reactive Nonmetal", "Phase": "Solid", "ElectronConfiguration": "[Ne] 3s² 3p³"},
        {"AtomicNumber": 16, "Symbol": "S", "Element": "Sulfur", "AtomicMass": "32.06", "Period": 3, "Group": 16, "Type": "Reactive Nonmetal", "Phase": "Solid", "ElectronConfiguration": "[Ne] 3s² 3p⁴"},
        {"AtomicNumber": 17, "Symbol": "Cl", "Element": "Chlorine", "AtomicMass": "35.45", "Period": 3, "Group": 17, "Type": "Reactive Nonmetal", "Phase": "Gas", "ElectronConfiguration": "[Ne] 3s² 3p⁵"},
        {"AtomicNumber": 18, "Symbol": "Ar", "Element": "Argon", "AtomicMass": "39.948", "Period": 3, "Group": 18, "Type": "Noble Gas", "Phase": "Gas", "ElectronConfiguration": "[Ne] 3s² 3p⁶"},
        # Contoh Periode 4 (Kalium & Kalsium)
        {"AtomicNumber": 19, "Symbol": "K", "Element": "Potassium", "AtomicMass": "39.098", "Period": 4, "Group": 1, "Type": "Alkali Metal", "Phase": "Solid", "ElectronConfiguration": "[Ar] 4s¹"},
        {"AtomicNumber": 20, "Symbol": "Ca", "Element": "Calcium", "AtomicMass": "40.078", "Period": 4, "Group": 2, "Type": "Alkaline Earth Metal", "Phase": "Solid", "ElectronConfiguration": "[Ar] 4s²"},
    ]
    return pd.DataFrame(raw_data)


df = load_local_data()

# Inisialisasi memori jangka pendek (session_state)
if "selected_element" not in st.session_state:
    st.session_state.selected_element = "Hydrogen"

# ==============================================================================
# 3. MERENDER GRID TABEL PERIODIK (18 KOLOM)
# ==============================================================================
with st.container():
    cols = st.columns(18)

    # Batasi scan sampai periode 4 untuk data lokal ini
    for period in range(1, 5):
        current_period_df = df[df["Period"] == period]

        for group in range(1, 19):
            element_row = current_period_df[current_period_df["Group"] == group]

            with cols[group - 1]:
                if not element_row.empty:
                    sym = element_row.iloc[0]["Symbol"]
                    num = element_row.iloc[0]["AtomicNumber"]
                    name = element_row.iloc[0]["Element"]

                    if st.button(f"{num}\n{sym}", key=f"btn_{sym}"):
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

# Membagi informasi angka menjadi 4 kolom berjejer
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="Nomor Atom", value=str(element_info["AtomicNumber"]))
with m_col2:
    st.metric(label="Massa Atom", value=f"{element_info['AtomicMass']} u")
with m_col3:
    st.metric(label="Golongan (Group)", value=str(element_info["Group"]))
with m_col4:
    st.metric(label="Periode (Period)", value=str(element_info["Period"]))

# Menampilkan konfigurasi elektron
st.write("**Konfigurasi Elektron:**")
st.code(element_info["ElectronConfiguration"], language="bash")
