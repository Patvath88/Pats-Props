import streamlit as st

# Imports are now direct because the files are in the same folder
from app_page import display_page
from sidebar import display_sidebar
from services.prop_generation import PropGenerationService

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="Player Prop Picks Generator",
        page_icon="🏀",
        layout="wide"
    )

    # Initialize the prop generation service
    prop_service = PropGenerationService()

    # Display the sidebar and get the selected game
    selected_game_id = display_sidebar(prop_service)

    # Display the main page content for the selected game
    display_page(prop_service, selected_game_id)

if __name__ == "__main__":
    main()
