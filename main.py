import streamlit as st
from app_page import display_page
from sidebar import display_sidebar
from prop_generation import PropGenerationService

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="Player Prop Picks Generator",
        page_icon="🏀",
        layout="wide"
    )
    prop_service = PropGenerationService()
    selected_game_id = display_sidebar(prop_service)
    display_page(prop_service, selected_game_id)

if __name__ == "__main__":
    main()
