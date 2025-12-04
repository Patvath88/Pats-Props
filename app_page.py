import streamlit as st
import pandas as pd
# The import below is the line we are fixing. No more 'ui'.
from sidebar import display_sidebar 

def display_page(prop_service, selected_game_id):
    """Displays the main content of the application."""
    
    st.title("Player Prop Picks Generator")
    st.write("Select a game from the sidebar to view player prop odds.")

    if selected_game_id:
        game_data = prop_service.get_game_by_id(selected_game_id)
        if game_data:
            home_team = game_data.get('home_team', 'N/A')
            away_team = game_data.get('away_team', 'N/A')
            st.header(f"Odds for {away_team} @ {home_team}")

            # This is where we will process and display the odds
            odds_df = process_game_odds(game_data)
            
            if not odds_df.empty:
                st.dataframe(odds_df, use_container_width=True)
            else:
                st.warning("Could not retrieve or process odds for the selected game. The API might not have player props available for this game, or your API plan may not include them.")
        else:
            st.error("Could not find data for the selected game.")
            
def process_game_odds(game_data):
    """Processes the raw game data to create a displayable DataFrame of odds."""
    all_props = []

    for bookmaker in game_data.get('bookmakers', []):
        market_data = {}
        for market in bookmaker.get('markets', []):
            market_key = market.get('key')
            if market_key in ['player_points', 'player_rebounds', 'player_assists', 'h2h']:
                for outcome in market.get('outcomes', []):
                    player_name = outcome.get('description')
                    # For h2h (moneyline), the 'player' is the team name
                    if market_key == 'h2h':
                        player_name = outcome.get('name')

                    if player_name not in market_data:
                        market_data[player_name] = {'Player': player_name}

                    # Store points/odds for different bet types (Over/Under)
                    if 'price' in outcome and 'point' in outcome:
                        bet_type = outcome.get('name') # Over or Under
                        point = outcome.get('point')
                        price = outcome.get('price')
                        market_data[player_name][f'{market_key.split("_")[-1].capitalize()} {bet_type} {point}'] = price
                    
                    # Store moneyline odds
                    elif market_key == 'h2h':
                         market_data[player_name][f'Moneyline'] = outcome.get('price')


        # Add bookmaker name to each record
        for player, data in market_data.items():
            data['Bookmaker'] = bookmaker.get('title')
            all_props.append(data)

    if not all_props:
        return pd.DataFrame()

    df = pd.DataFrame(all_props)
    
    # Reorder columns to be more intuitive
    if not df.empty:
        cols = df.columns.tolist()
        # Move 'Player' and 'Bookmaker' to the front
        if 'Player' in cols:
            cols.insert(0, cols.pop(cols.index('Player')))
        if 'Bookmaker' in cols:
            cols.insert(1, cols.pop(cols.index('Bookmaker')))
        df = df[cols]

    return df.fillna('-')
