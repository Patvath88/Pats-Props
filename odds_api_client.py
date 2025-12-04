import requests
import streamlit as st
import logging

class OddsAPIClient:
    def __init__(self):
        self.api_key = st.secrets.get("ODDS_API_KEY")
        if not self.api_key:
            raise ValueError("ODDS_API_KEY not found in Streamlit secrets.")
        self.base_url = "https://api.the-odds-api.com"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_nba_games(self):
        logging.info("Attempting to fetch NBA games from Odds API.")
        
        endpoint = "/v4/sports/basketball_nba/odds"
        params = {
            "apiKey": self.api_key,
            "regions": "us",
            "markets": ",".join([
                "player_points",
                "player_rebounds",
                "player_assists",
                "player_threes",
                "player_blocks",
                "player_steals",
                "player_blocks_steals",
                "player_turnovers",
                "player_points_rebounds_assists",
                "player_points_rebounds",
                "player_points_assists",
                "player_rebounds_assists",
                "player_field_goals",
                "player_frees_made",
                "player_frees_attempts",
                "player_first_basket",
                "player_first_team_basket",
                "player_double_double",
                "player_triple_double",
                "player_method_of_first_basket",
                "player_points_alternate",
                "player_rebounds_alternate",
                "player_assists_alternate",
                "player_blocks_alternate",
                "player_steals_alternate",
                "player_turnovers_alternate",
                "player_threes_alternate",
                "player_points_assists_alternate",
                "player_points_rebounds_alternate",
                "player_rebounds_assists_alternate",
                "player_points_rebounds_assists_alternate"
            ]),
            "oddsFormat": "american"
        }
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            
            logging.info(f"--- RAW ODDS API RESPONSE --- \n{data}\n-----------------------------")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from Odds API: {e}")
            if e.response is not None:
                logging.error(f"API Error Body: {e.response.text}")
            return None
