import streamlit as st
import pandas as pd

def display_page(prop_service, selected_game_id):
    """Displays the main content of the application."""
    
    st.title("Player Prop Picks Generator")
    st.write("Select a game from the sidebar to view player prop odds and stats.")

    if selected_game_id:
        # The get_game_by_id function now returns data with stats included
        game_data = prop_service.get_game_by_id(selected_game_id)
        
        if game_data:
            home_team = game_data.get('home_team', 'N/A')
            away_team = game_data.get('away_team', 'N/A')
            st.header(f"Odds & Stats for {away_team} @ {home_team}")

            # The processing function now receives the enriched data
            odds_df = process_game_data(game_data)
            
            if not odds_df.empty:
                st.dataframe(odds_df, use_container_width=True)
            else:
                st.warning("Could not retrieve or process odds/stats for the selected game.")
        else:
            st.error("Could not find data for the selected game.")
            
def process_game_data(game_data):
    """
    Processes the raw game data (now including stats) to create a 
    displayable DataFrame.
    """
    all_props = []
    player_stats = game_data.get('player_stats', {}) # Get the stats we added in the service

    for bookmaker in game_data.get('bookmakers', []):
        for market in bookmaker.get('markets', []):
            market_key = market.get('key')
            if market_key in ['player_points', 'player_rebounds', 'player_assists']:
                for outcome in market.get('outcomes', []):
                    player_name = outcome.get('description')
                    
                    # Create a unique key for each player+market combination
                    prop_key = f"{player_name}_{market_key}"
                    
                    # Find existing prop or create new one
                    prop_entry = next((item for item in all_props if item.get('key') == prop_key), None)
                    if not prop_entry:
                        prop_entry = {
                            'key': prop_key,
                            'Player': player_name,
                            'Prop': market_key.replace('player_', '').capitalize(),
                            # --- NEW: Add player stats to the row ---
                            'Season Avg Pts': player_stats.get(player_name, {}).get('pts', '-'),
                            'Season Avg Reb': player_stats.get(player_name, {}).get('reb', '-'),
                            'Season Avg Ast': player_stats.get(player_name, {}).get('ast', '-')
                        }
                        all_props.append(prop_entry)
                    
                    # Add the bookmaker's line
                    line = f"{outcome.get('name')} {outcome.get('point')} ({outcome.get('price')})"
                    prop_entry[bookmaker.get('title')] = line

    if not all_props:
        return pd.DataFrame()

    df = pd.DataFrame(all_props)
    df = df.drop(columns=['key']) # Drop the temporary key
    return df.fillna('-')
