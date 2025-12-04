import streamlit as st
from ui.app_page import display_page

if __name__ == "__main__":
    st.set_page_config(
        page_title="Player Prop Picks Generator",
        page_icon="🏀",
        layout="wide"
    )
    display_page()
