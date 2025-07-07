import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="🎁 Lucky Draw", layout="centered")
st.title("🎉 Lucky Draw App")
st.write("Upload an Excel file with multiple entry columns (e.g., Employee No, Name, Address).")

uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if df.empty:
            st.warning("The uploaded file is empty.")
        else:
            st.success(f"Loaded {len(df)} entries.")

            entries = df.apply(lambda row: " | ".join(str(val) for val in row if pd.notna(val)), axis=1).tolist()

            if 'drawing' not in st.session_state:
                st.session_state.drawing = False
            if 'winner' not in st.session_state:
                st.session_state.winner = None

            col1, col2 = st.columns(2)
            if col1.button("▶ Start Draw"):
                st.session_state.drawing = True
                st.session_state.winner = None

            if col2.button("⏹ Stop Draw"):
                st.session_state.drawing = False
                st.session_state.winner = random.choice(entries)

            placeholder = st.empty()
            if st.session_state.drawing:
                for _ in range(100):
                    entry = random.choice(entries)
                    placeholder.markdown(f"### 🎯 Drawing: **{entry}**")
                    time.sleep(0.05)
                st.rerun()

            elif st.session_state.winner:
                placeholder.markdown(f"## 🏆 Winner: **{st.session_state.winner}** 🎉")

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
else:
    st.info("Please upload an Excel file to begin.")

