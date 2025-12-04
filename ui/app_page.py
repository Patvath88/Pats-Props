import streamlit as st
import pandas as pd
from ui.sidebar import display_sidebar
from clients.odds_api_client import OddsApiClient
from services.prop_generation import generate_prop_bet_data

def display_page():
    """
    Renders the main page content, including title, dataframes, and analysis.
    """
    st.title("🏀 Player Prop Picks Generator")
    st.markdown("Select a game from the sidebar to view player prop bet analysis.")

    selected_game = display_sidebar()

    if selected_game:
        st.header(f"Analysis for: {selected_game['visitor_team']['full_name']} @ {selected_game['home_team']['full_name']}")
        
        # Fetch odds for the selected game
        odds_client = OddsApiClient()
        with st.spinner("Fetching latest odds..."):
            odds_data = odds_client.get_odds_for_game(selected_game)

        if not odds_data or not odds_data.get('bookmakers'):
            st.warning("Could not retrieve odds for this game. The game may have already started or odds are not yet available.")
            return

        # Generate and display prop bet data
        with st.spinner("Analyzing player data and generating picks..."):
            prop_data = generate_prop_bet_data(odds_data)

        if prop_data:
            df_points = pd.DataFrame(prop_data['points'])
            df_rebounds = pd.DataFrame(prop_data['rebounds'])
            df_assists = pd.DataFrame(prop_data['assists'])

            st.subheader("Points Props")
            st.dataframe(df_points, use_container_width=True)

            st.subheader("Rebounds Props")
            st.dataframe(df_rebounds, use_container_width=True)

            st.subheader("Assists Props")
            st.dataframe(df_assists, use_container_width=True)
        else:
            st.info("No player prop data could be generated for the selected game.")
