import streamlit as st

def display_sidebar(prop_service):
    """Renders the sidebar and returns the selected game ID."""
    with st.sidebar:
        st.header("NBA Games")
        
        games = prop_service.get_all_games()
        
        if not games:
            st.warning("No NBA games found. The API might be unavailable or there are no games scheduled.")
            return None

        # Create a list of game labels for the radio button
        game_labels = {f"{game['away_team']} @ {game['home_team']}": game['id'] for game in games}
        
        selected_label = st.radio(
            "Select a game to view props:",
            options=list(game_labels.keys())
        )
        
        # Return the ID of the selected game
        return game_labels[selected_label]
