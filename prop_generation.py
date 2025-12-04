import pandas as pd
from clients.balldontlie_client import BallDontLieClient

def get_player_season_average(player_id: int, stat: str) -> float:
    """
    Fetches a player's season average for a specific stat (pts, reb, ast).
    """
    client = BallDontLieClient()
    stats = client.get_player_stats_for_season(player_id)
    if not stats:
        return 0.0
    
    df = pd.DataFrame(stats)
    return df[stat].mean() if stat in df.columns else 0.0

def generate_prop_bet_data(odds_data: dict) -> dict:
    """
    Processes odds data to generate a structured dictionary of prop bet analysis.
    """
    prop_data = {'points': [], 'rebounds': [], 'assists': []}
    
    if not odds_data.get('bookmakers'):
        return prop_data

    # Assuming the first bookmaker has the most comprehensive odds
    bookmaker = odds_data['bookmakers'][0]
    markets = bookmaker.get('markets', [])

    for market in markets:
        market_key_map = {
            'player_points': 'points',
            'player_rebounds': 'rebounds',
            'player_assists': 'assists'
        }
        
        prop_type = market_key_map.get(market['key'])
        if not prop_type:
            continue

        for outcome in market.get('outcomes', []):
            player_name = outcome['description']
            line = outcome['point']
            
            # This is a placeholder for a more sophisticated player ID mapping
            # In a real app, you'd need a robust way to find a player's ID from their name.
            # For this example, we'll skip the season average calculation.
            # season_avg = get_player_season_average(player_id, prop_type_map[prop_type])
            season_avg = "N/A" # Placeholder

            prop_data[prop_type].append({
                'Player': player_name,
                'Line': line,
                'Over Price': outcome['price'] if outcome['name'] == 'Over' else 'N/A',
                'Under Price': outcome['price'] if outcome['name'] == 'Under' else 'N/A',
                'Season Avg': season_avg,
                'Recommendation': 'N/A' # Placeholder for analysis logic
            })

    # Consolidate Over/Under into a single row
    for prop_type, props in prop_data.items():
        df = pd.DataFrame(props)
        # Group by player and line, then merge the over/under prices
        consolidated_df = df.groupby(['Player', 'Line', 'Season Avg']).agg({
            'Over Price': lambda x: x[x != 'N/A'].iloc[0] if any(x != 'N/A') else 'N/A',
            'Under Price': lambda x: x[x != 'N/A'].iloc[0] if any(x != 'N/A') else 'N/A'
        }).reset_index()
        prop_data[prop_type] = consolidated_df.to_dict('records')

    return prop_data
