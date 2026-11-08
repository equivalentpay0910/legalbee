import streamlit as st

st.title("LegalBee")
st.caption("Legal information, not legal advice.")

area = st.selectbox("What is your question about?", ["Housing", "Work", "F-1 status"])
question = st.text_area("Describe your situation")

if st.button("Get answer"):
    st.info(f"({area}) Answers coming soon!")