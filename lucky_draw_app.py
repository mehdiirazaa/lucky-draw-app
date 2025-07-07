import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="BAHL HAJJ Balloting", layout="centered")
st.title("🎉 BAHL HAJJ Balloting")
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

            # prepare data only once
            if 'entries' not in st.session_state:
                # convert to list of lists: [ID, Name, Designation, Zone, Branch]
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

            # run the draw loop if drawing started
            if st.session_state.drawing and st.session_state.remaining_entries:
                while st.session_state.drawing:
                    pick = random.choice(st.session_state.remaining_entries)
                    st.session_state.current_display = pick

                    # nicely format during rolling draw
                    placeholder.markdown(f"""
                    ### 🎯 Drawing...
                    **Name:** {pick[1]}  
                    **Designation:** {pick[2]}  
                    **Zone:** {pick[3]}  
                    **Branch:** {pick[4]}
                    """)
                    time.sleep(0.01)  # super fast rolling
                    st.rerun()

            # after stop, finalize winner
            if not st.session_state.drawing and st.session_state.current_display:
                winner = st.session_state.current_display
                if winner not in st.session_state.winners:
                    st.session_state.winners.append(winner)
                if winner in st.session_state.remaining_entries:
                    st.session_state.remaining_entries.remove(winner)

                placeholder.markdown(f"""
                ## 🏆 Winner!
                **Name:** {winner[1]}  
                **Designation:** {winner[2]}  
                **Zone:** {winner[3]}  
                **Branch:** {winner[4]}
                """)
                st.balloons()

            # display all winners
            if st.session_state.winners:
                st.markdown("### 📝 Winners so far:")
                for idx, winner in enumerate(st.session_state.winners, 1):
                    st.markdown(f"""
                    **{idx}.**
                    - Name: {winner[1]}
                    - Designation: {winner[2]}
                    - Zone: {winner[3]}
                    - Branch: {winner[4]}
                    """)

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
