import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="🎁 Lucky Draw", layout="centered")
st.title("🎉 Lucky Draw App")
st.write("Upload an Excel file with entries (multiple columns supported).")

uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if df.empty:
            st.warning("The uploaded file is empty.")
        else:
            st.success(f"Loaded {len(df)} entries.")

            # Prepare entries as combined string from multiple columns
            entries = df.apply(lambda row: " | ".join(str(val) for val in row if pd.notna(val)), axis=1).tolist()

            # Initialize session state
            if 'drawing' not in st.session_state:
                st.session_state.drawing = False
            if 'current_display' not in st.session_state:
                st.session_state.current_display = None
            if 'winners' not in st.session_state:
                st.session_state.winners = []
            if 'remaining_entries' not in st.session_state:
                st.session_state.remaining_entries = entries.copy()

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
                        st.session_state.winners.append(winner)
                        st.session_state.remaining_entries.remove(winner)

            placeholder = st.empty()

            # While drawing is active, pick random
            while st.session_state.drawing and st.session_state.remaining_entries:
                pick = random.choice(st.session_state.remaining_entries)
                st.session_state.current_display = pick
                placeholder.markdown(f"### 🎯 Drawing: **{pick}**")
                time.sleep(0.02)  # fast rolling
                st.experimental_rerun()

            # Show latest winner
            if not st.session_state.drawing and st.session_state.current_display and st.session_state.current_display not in st.session_state.remaining_entries:
                placeholder.markdown(f"## 🏆 Winner: **{st.session_state.current_display}** 🎉")
                st.balloons()

            # Show all winners so far
            if st.session_state.winners:
                st.markdown("### 📝 Winners so far:")
                for idx, winner in enumerate(st.session_state.winners, 1):
                    st.markdown(f"{idx}. **{winner}**")

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
