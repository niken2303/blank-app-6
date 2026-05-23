import pandas as pd
import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA LUCU (CSS CUSTOM)
# ==============================================================================
st.set_page_config(
    page_title="Tabel Periodik Gemas", page_icon="🎨", layout="wide"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Fredoka', sans-serif !important;
    }
    
    div.stButton > button {
        width: 100%;
        height: 70px;
        padding: 5px;
        font-family: 'Fredoka', sans-serif;
        font-weight: 600;
        font-size: 14px;
        border-radius: 12px;
        border: None;
        line-height: 1.3;
        color: #2F3E46;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease-in-out;
    }
    
    div.stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
    }

    .detail-card {
        padding: 25px;
        border-radius: 20px;
        background-color: #F8F9FA;
        border: 2px dashed #E9ECEF;
        margin-bottom: 20px;
        box-shadow: inset 0px 2px 4px rgba(0,0,0,0.02);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🎨 Tabel Periodik Pop-Pastel")
st.write("Klik kotak unsur yang lucu di bawah untuk mengintip rahasia kimianya!")
st.markdown("---")

# ==============================================================================
# 2. DATABASE LOKAL (SUDAH DIPERBAIKI & DI-TES)
# ==============================================================================
@st.cache_data
def load_cute_data():
    raw_data = [
        # Periode 1
        {"AtomicNumber": 1, "Symbol": "H", "Element": "Hydrogen", "AtomicMass": "1.008", "Period": 1, "Group": 1, "Type": "Nonmetal", "Phase": "Gas", "Color": "#FFADAD", "Emoji": "🎈", "ElectronConfiguration": "1s¹"},
        {"AtomicNumber": 2, "Symbol": "He", "Element": "Helium", "AtomicMass": "4.0026", "Period": 1, "Group": 18, "Type": "Noble Gas", "Phase": "Gas", "Color": "#E8AEFF", "Emoji": "🎈", "ElectronConfiguration": "1s²"},
        # Periode 2
        {"AtomicNumber": 3, "Symbol": "Li", "Element": "Lithium", "AtomicMass": "6.94", "Period": 2, "Group": 1, "Type": "Alkali Metal", "Phase": "Solid", "Color": "#FFD6A5", "Emoji": "🔋", "ElectronConfiguration": "[He] 2s¹"},
        {"AtomicNumber": 4, "Symbol": "Be", "Element": "Beryllium", "AtomicMass": "9.0122", "Period": 2, "Group": 2, "Type": "Alkaline Earth", "Phase": "Solid", "Color": "#FFF9A6", "Emoji": "💎", "ElectronConfiguration": "[He] 2s²"},
        {"AtomicNumber": 5, "Symbol": "B", "Element": "Boron", "AtomicMass": "10.81", "Period": 2, "Group": 13, "Type": "Metalloid", "Phase": "Solid", "Color": "#CAFFBF", "Emoji": "👁️", "ElectronConfiguration": "[He] 2s² 2p¹"},
        {"AtomicNumber": 6, "Symbol": "C", "Element": "Carbon", "AtomicMass": "12.011", "Period": 2, "Group": 14, "Type": "Nonmetal", "Phase": "Solid", "Color": "#FFADAD", "Emoji": "✏️", "ElectronConfiguration": "[He] 2s² 2p²"},
        {"AtomicNumber": 7, "Symbol": "N", "Element": "Nitrogen", "AtomicMass": "14.007", "Period": 2, "Group": 15, "Type": "Nonmetal", "Phase": "Gas", "Color": "#FFADAD", "Emoji": "❄️", "ElectronConfiguration": "[He] 2s² 2p³"},
        {"AtomicNumber": 8, "Symbol": "O", "Element": "Oxygen", "AtomicMass": "15.999", "Period": 2, "Group": 16, "Type": "Nonmetal", "Phase": "Gas", "Color": "#FFADAD", "Emoji": "💨", "ElectronConfiguration": "[He] 2s² 2p⁴"},
        {"AtomicNumber": 9, "Symbol": "F", "Element": "Fluorine", "AtomicMass": "18.998", "Period": 2, "Group": 17, "Type": "Halogen", "Phase": "Gas", "Color": "#9BF6FF", "Emoji": "🦷", "ElectronConfiguration": "[He] 2s² 2p⁵"},
        {"AtomicNumber": 10, "Symbol": "Ne", "Element": "Neon", "AtomicMass": "20.180", "Period": 2, "Group": 18, "Type": "Noble Gas", "Phase": "Gas", "Color": "#E8AEFF", "Emoji": "🚨", "ElectronConfiguration": "[He] 2s² 2p⁶"},
        # Periode 3
        {"AtomicNumber": 11, "Symbol": "Na", "Element": "Sodium", "AtomicMass": "22.990", "Period": 3, "Group": 1, "Type": "Alkali Metal", "Phase": "Solid", "Color": "#FFD6A5", "Emoji": "🧂", "ElectronConfiguration": "[Ne] 3s¹"},
        {"AtomicNumber": 12, "Symbol": "Mg", "Element": "Magnesium", "AtomicMass": "24.305", "Period": 3, "Group": 2, "Type": "Alkaline Earth", "Phase": "Solid", "Color": "#FFF9A6", "Emoji": "🎆", "ElectronConfiguration": "[Ne] 3s²"},
        {"AtomicNumber": 13, "Symbol": "Al", "Element": "Aluminum", "AtomicMass": "26.982", "Period": 3, "Group": 13, "Type": "Post-Transition Metal", "Phase": "Solid", "Color": "#A0C4FF", "Emoji": "🥤", "ElectronConfiguration": "[Ne] 3s² 3p¹"},
        {"AtomicNumber": 14, "Symbol": "Si", "Element": "Silicon", "AtomicMass": "28.085", "Period": 3, "Group": 14, "Type": "Metalloid", "Phase": "Solid", "Color": "#CAFFBF", "Emoji": "💻", "ElectronConfiguration": "[Ne] 3s² 3p²"},
        {"AtomicNumber": 15, "Symbol": "P", "Element": "Phosphorus", "AtomicMass": "30.974", "Period": 3, "Group": 15, "Type": "Nonmetal", "Phase": "Solid", "Color": "#FFADAD", "Emoji": "🪵", "ElectronConfiguration": "[Ne] 3s² 3p³"},
        {"AtomicNumber": 16, "Symbol": "S", "Element": "Sulfur", "AtomicMass": "32.06", "Period": 3, "Group": 16, "Type": "Nonmetal", "Phase": "Solid", "Color": "#FFADAD", "Emoji": "🍋", "ElectronConfiguration": "[Ne] 3s² 3p⁴"},
        {"AtomicNumber": 17, "Symbol": "Cl", "Element": "Chlorine", "AtomicMass": "35.45", "Period": 3, "Group": 17, "Type": "Halogen", "Phase": "Gas", "Color": "#9BF6FF", "Emoji": "🏊", "ElectronConfiguration": "[Ne] 3s² 3p⁵"},
        {"AtomicNumber": 18, "Symbol": "Ar", "Element": "Argon", "AtomicMass": "39.948", "Period": 3, "Group": 18, "Type": "Noble Gas", "Phase": "Gas", "Color": "#E8AEFF", "Emoji": "💡", "ElectronConfiguration": "[Ne] 3s² 3p⁶"},
        # Periode 4
        {"AtomicNumber": 19, "Symbol": "K", "Element": "Potassium", "AtomicMass": "39.098", "Period": 4, "Group": 1, "Type": "Alkali Metal", "Phase": "Solid", "Color": "#FFD6A5", "Emoji": "🍌", "ElectronConfiguration": "[Ar] 4s¹"},
        {"AtomicNumber": 20, "Symbol": "Ca", "Element": "Calcium", "AtomicMass": "40.078", "Period": 4, "Group": 2, "Type": "Alkaline Earth", "Phase": "Solid", "Color": "#FFF9A6", "Emoji": "🥛", "ElectronConfiguration": "[Ar] 4s²"},
    ]
    return pd.DataFrame(raw_data)

df = load_cute_data()

if "selected_element" not in st.session_state:
    st.session_state.selected_element = "Hydrogen"

# ==============================================================================
# 3. GENERATE GRID KOTAK WARNA-WARNI
# ==============================================================================
with st.container():
    cols = st.columns(18)

    for period in range(1, 5):
        current_period_df = df[df["Period"] == period]

        for group in range(1, 19):
            element_row = current_period_df[current_period_df["Group"] == group]

            with cols[group - 1]:
                if not element_row.empty:
                    sym = element_row.iloc[0]["Symbol"]
                    color = element_row.iloc[0]["Color"]
                    emoji = element_row.iloc[0]["Emoji"]
                    name = element_row.iloc[0]["Element"]

                    st.markdown(
                        f"""
                        <style>
                        div.stButton > button[key="btn_{sym}"] {{
                            background-color: {color} !important;
                        }}
                        </style>
                    """,
                        unsafe_allow_html=True,
                    )

                    if st.button(f"{emoji}\n{sym}", key=f"btn_{sym}"):
                        st.session_state.selected_element = name
                else:
                    st.write("")

st.markdown("---")

# ==============================================================================
# 4. KOTAK DETAIL INFORMASI
# ==============================================================================
selected_name = st.session_state.selected_element
element_info = df[df["Element"] == selected_name].iloc[0]

st.markdown(
    f"""
    <div class="detail-card">
        <h2 style='margin:0; color:#2F3E46;'>{element_info['Emoji']} {element_info['Element']} ({element_info['Symbol']})</h2>
        <p style='margin:8px 0 0 0; color:#6C757D; font-size:16px;'>
            <b>Kelompok Unsur:</b> {element_info['Type']} | <b>Wujud Zat:</b> {element_info['Phase']}
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="🔢 Nomor Atom", value=str(element_info["AtomicNumber"]))
with m_col2:
    st.metric(label="⚖️ Massa Atom", value=f"{element_info['AtomicMass']} u")
with m_col3:
    st.metric(label="↕️ Golongan", value=str(element_info["Group"]))
with m_col4:
    st.metric(label="↔️ Periode", value=str(element_info["Period"]))

st.write("✨ **Konfigurasi Elektron:**")
st.code(element_info["ElectronConfiguration"], language="bash")
st.code(element_info["ElectronConfiguration"], language="bash")
