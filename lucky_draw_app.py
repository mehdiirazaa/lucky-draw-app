import streamlit as st
import pandas as pd
import random
import time
import base64

st.set_page_config(page_title="BAHL HAJJ Balloting", layout="centered")

# Helper to embed image as base64 for HTML <img src=...>
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_data = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{b64_data}"

# Load new Hajj logo once as base64
hajj_img_data = get_base64_image("hajj1.png")

# Logo & title side by side
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("Bank_al_habib_logo.png", width=120)
with col_title:
    st.markdown("<h1 style='color:#00543D;'>BAHL HAJJ Balloting</h1>", unsafe_allow_html=True)

st.write("Upload an Excel file with columns: **ID, Name, Designation, Zone, Branch**")

@st.cache_data
def load_excel(file):
    return pd.read_excel(file)

uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = load_excel(uploaded_file)
        if df.empty:
            st.warning("The uploaded file is empty.")
        else:
            st.success(f"Loaded {len(df)} entries.")

            if 'entries' not in st.session_state:
                st.session_state.entries = df[['ID', 'Name', 'Designation', 'Zone', 'Branch']].values.tolist()
                st.session_state.remaining_entries = st.session_state.entries.copy()
                st.session_state.drawing = False
                st.session_state.current_display = None
                st.session_state.winners = []

            col1, col2 = st.columns(2)
            if col1.button("▶ Start Draw"):
                if not st.session_state.remaining_entries:
                    st.warning("No more entries left.")
                else:
                    st.session_state.drawing = True
            if col2.button("⏹ Stop Draw"):
                st.session_state.drawing = False

            placeholder = st.empty()

            if st.session_state.drawing and st.session_state.remaining_entries:
                while st.session_state.drawing:
                    pick = random.choice(st.session_state.remaining_entries)
                    st.session_state.current_display = pick
                    # SUPER FAST rolling ID
                    placeholder.markdown(f"""
                    <div style='color:#00543D; font-size:90px; font-weight:bold; text-align:center;'>
                        {pick[0]}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.001)  # ultra quick
                    st.rerun()

            if not st.session_state.drawing and st.session_state.current_display:
                winner = st.session_state.current_display
                if winner not in st.session_state.winners:
                    st.session_state.winners.append(winner)
                if winner in st.session_state.remaining_entries:
                    st.session_state.remaining_entries.remove(winner)

                # Winner popup style with floating new Hajj logos (larger)
                placeholder.markdown(f"""
                <div style='color:#00543D; font-size:45px; text-align:center;'>
                    🏆 <strong>Winner!</strong><br><br>
                    <strong>ID:</strong> {winner[0]}<br>
                    <strong>Name:</strong> {winner[1]}<br>
                    <strong>Designation:</strong> {winner[2]}<br>
                    <strong>Zone:</strong> {winner[3]}<br>
                    <strong>Branch:</strong> {winner[4]}
                </div>

                <div style="position:relative;height:300px;">
                    <img src='{hajj_img_data}' style='position:absolute; bottom:0; left:20%; animation: floatUp 4s ease-in infinite;' width='70'>
                    <img src='{hajj_img_data}' style='position:absolute; bottom:0; left:40%; animation: floatUp 5s ease-in infinite;' width='70'>
                    <img src='{hajj_img_data}' style='position:absolute; bottom:0; left:60%; animation: floatUp 4.5s ease-in infinite;' width='70'>
                    <img src='{hajj_img_data}' style='position:absolute; bottom:0; left:80%; animation: floatUp 6s ease-in infinite;' width='70'>
                </div>

                <style>
                @keyframes floatUp {{
                    0% {{ transform: translateY(0); opacity: 1; }}
                    100% {{ transform: translateY(-300px); opacity: 0; }}
                }}
                </style>
                """, unsafe_allow_html=True)

            if st.session_state.winners:
                st.markdown("<h3 style='color:#00543D;'>📝 Winners so far:</h3>", unsafe_allow_html=True)
                for idx, winner in enumerate(st.session_state.winners, 1):
                    st.markdown(f"""
                    <div style='color:#00543D;'>
                    <strong>{idx}.</strong><br>
                    - ID: {winner[0]}<br>
                    - Name: {winner[1]}<br>
                    - Designation: {winner[2]}<br>
                    - Zone: {winner[3]}<br>
                    - Branch: {winner[4]}
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
