import streamlit as st
import pandas as pd
import random
import time

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
            st.success(f"Loaded {len(df)} entries from your file.")

            # Prepare entries as list of cell values per row
            entries = df.apply(lambda row: [str(val) for val in row if pd.notna(val)], axis=1).tolist()

            # Initialize session state
            if 'remaining_entries' not in st.session_state:
                st.session_state.remaining_entries = entries.copy()
            if 'drawing' not in st.session_state:
                st.session_state.drawing = False
            if 'current_display' not in st.session_state:
                st.session_state.current_display = None
            if 'winners' not in st.session_state:
                st.session_state.winners = []

            # Buttons
            col1, col2 = st.columns(2)
            if col1.button("▶ Start Draw"):
                if not st.session_state.remaining_entries:
                    st.warning("No more entries left to draw from.")
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

            # Draw loop
            placeholder = st.empty()
            if st.session_state.drawing and st.session_state.remaining_entries:
                while st.session_state.drawing:
                    pick = random.choice(st.session_state.remaining_entries)
                    st.session_state.current_display = pick
                    placeholder.markdown(f"### 🎯 Drawing: **{' | '.join(pick)}**")
                    time.sleep(0.005)  # ultra fast
                    st.rerun()

            # Show current winner nicely on separate lines
            if st.session_state.current_display and st.session_state.current_display in st.session_state.winners:
                winner_details = st.session_state.current_display
                winner_text = f"""
                ## 🏆 Winner!

                **Name:** {winner_details[0]}  
                **Designation:** {winner_details[1] if len(winner_details) > 1 else ''}  
                **Branch:** {winner_details[2] if len(winner_details) > 2 else ''}
                """
                placeholder.markdown(winner_text)
                st.balloons()

            # Show all winners so far
            if st.session_state.winners:
                st.markdown("### 📝 Winners so far:")
                for idx, winner in enumerate(st.session_state.winners, 1):
                    winner_info = f"""
                    **{idx}.**
                    - Name: {winner[0]}
                    - Designation: {winner[1] if len(winner) > 1 else ''}
                    - Branch: {winner[2] if len(winner) > 2 else ''}
                    """
                    st.markdown(winner_info)

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
