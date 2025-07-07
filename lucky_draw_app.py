import streamlit as st
import pandas as pd
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="BAHL HAJJ Balloting", layout="centered")
st.title("🎉 BAHL HAJJ Balloting")
st.write("Upload an Excel file with entries. Each row should have columns like Name, Designation, Branch.")

uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if df.empty:
            st.warning("The uploaded file is empty.")
        else:
            st.success(f"Loaded {len(df)} entries.")

            entries = df.apply(lambda row: [str(val) for val in row if pd.notna(val)], axis=1).tolist()

            if 'remaining_entries' not in st.session_state:
                st.session_state.remaining_entries = entries.copy()
            if 'drawing' not in st.session_state:
                st.session_state.drawing = False
            if 'current_display' not in st.session_state:
                st.session_state.current_display = None
            if 'winners' not in st.session_state:
                st.session_state.winners = []

            col1, col2 = st.columns(2)
            if col1.button("▶ Start Draw"):
                if not st.session_state.remaining_entries:
                    st.warning("No more entries left.")
                else:
                    st.session_state.drawing = True
            if col2.button("⏹ Stop Draw"):
                if st.session_state.drawing:
                    st.session_state.drawing = False
                    winner = st.session_state.current_display
                    if winner:
                        if winner not in st.session_state.winners:
                            st.session_state.winners.append(winner)
                        if winner in st.session_state.remaining_entries:
                            st.session_state.remaining_entries.remove(winner)

            # AUTOREFRESH every 100ms if drawing
            if st.session_state.drawing:
                st_autorefresh(interval=100, key="refresh")

                pick = random.choice(st.session_state.remaining_entries)
                st.session_state.current_display = pick

            placeholder = st.empty()

            # Show drawing or winner
            if st.session_state.drawing and st.session_state.remaining_entries:
                placeholder.markdown(f"### 🎯 Drawing: **{' | '.join(st.session_state.current_display)}**")
            elif st.session_state.current_display and st.session_state.current_display in st.session_state.winners:
                winner_details = st.session_state.current_display
                winner_text = f"""
                ## 🏆 Winner!

                **Name:** {winner_details[0]}  
                **Designation:** {winner_details[1] if len(winner_details) > 1 else ''}  
                **Branch:** {winner_details[2] if len(winner_details) > 2 else ''}
                """
                placeholder.markdown(winner_text)
                st.balloons()

            if st.session_state.winners:
                st.markdown("### 📝 Winners so far:")
                for idx, winner in enumerate(st.session_state.winners, 1):
                    st.markdown(f"""
                    **{idx}.**
                    - Name: {winner[0]}
                    - Designation: {winner[1] if len(winner) > 1 else ''}
                    - Branch: {winner[2] if len(winner) > 2 else ''}
                    """)

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
