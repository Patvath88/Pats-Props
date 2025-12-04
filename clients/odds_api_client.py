import os
import requests
import pandas as pd

class OddsAPIClient:
    def __init__(self):
        self.api_key = os.getenv('ODDS_API_KEY')
        if not self.api_key:
            raise ValueError("ODDS_API_KEY not found in environment variables.")
        self.base_url = "https://api.the-odds-api.com/v4"

    def get_nba_games(self):
        """Fetches all available NBA games and their player prop odds."""
        url = f"{self.base_url}/sports/basketball_nba/odds/"
        
        # This is the test configuration to see if your API key can fetch basic odds.
        params = {
            'apiKey': self.api_key,
            'regions': 'us',
            'markets': 'h2h',  # <-- THIS IS THE TEMPORARY CHANGE FOR OUR TEST
            'bookmakers': 'draftkings,fanduel,betmgm,caesars,pointsbetus'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching NBA games from Odds API: {e}")
            return []

    def get_odds_for_game(self, game_id, markets='player_points,player_rebounds,player_assists'):
        """
        Fetches specific player prop odds for a single game ID.
        NOTE: This function is not currently used because get_nba_games() fetches
        all odds at once, which is more efficient for API usage.
        It is kept here for potential future use or more detailed lookups.
        """
        url = f"{self.base_url}/sports/basketball_nba/events/{game_id}/odds"
        params = {
            'apiKey': self.api_key,
            'regions': 'us',
            'markets': markets,
            'bookmakers': 'draftkings,fanduel,betmgm,caesars,pointsbetus'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching odds for game {game_id}: {e}")
            return None
