import os
import requests
import streamlit as st

class OddsAPIClient:
    def __init__(self):
        # Use st.secrets for robust key management
        self.api_key = st.secrets.get("ODDS_API_KEY")
        if not self.api_key:
            raise ValueError("ODDS_API_KEY not found in Streamlit secrets.")
        self.base_url = "https://api.the-odds-api.com"

    def get_nba_games(self):
        """
        Fetches upcoming NBA games and their odds.
        """
        endpoint = "/v4/sports/basketball_nba/odds"
        params = {
            "apiKey": self.api_key,
            "regions": "us", # North American bookmakers
            "markets": "h2h,spreads,totals,player_points,player_rebounds,player_assists",
            "oddsFormat": "american"
        }
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            
            # --- THIS IS THE DEBUGGING LINE ---
            print(f"--- RAW API RESPONSE --- \n{data}\n------------------------")
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Odds API: {e}")
            # Also print the response text if available, it might contain error details
            if e.response is not None:
                print(f"API Error Body: {e.response.text}")
            return None
