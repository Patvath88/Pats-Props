import streamlit as st
from clients.balldontlie_client import BallDontLieClient

def display_sidebar():
    """
    Displays the sidebar with game selection dropdown.
    Returns the selected game's data.
    """
    st.sidebar.header("Select a Game")
    client = BallDontLieClient()
    games = client.get_games_for_today()

    if not games:
        st.sidebar.warning("No NBA games scheduled for today.")
        return None

    game_options = {
        f"{game['visitor_team']['full_name']} @ {game['home_team']['full_name']}": game
        for game in games
    }
    
    selected_game_str = st.sidebar.selectbox(
        "Choose a matchup:",
        options=list(game_options.keys())
    )

    if selected_game_str:
        return game_options[selected_game_str]
    return None
