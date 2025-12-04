import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BallDontLieClient:
    def __init__(self):
        self.api_key = os.getenv("BALLDONTLIE_API_KEY")
        if not self.api_key:
            raise ValueError("API key for balldontlie not found.")
        self.base_url = "https://api.balldontlie.io/v1"
        self.headers = {"Authorization": self.api_key}

    def get_games_for_today(self) -> list[dict]:
        today_str = datetime.now().strftime('%Y-%m-%d')
        endpoint = f"{self.base_url}/games"
        params = {"dates[]": [today_str]}
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching games from balldontlie: {e}")
            return []

    def get_player_stats_for_season(self, player_id: int, season: int = 2023) -> list[dict]:
        endpoint = f"{self.base_url}/stats"
        params = {"seasons[]": [season], "player_ids[]": [player_id], "per_page": 100}
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stats for player {player_id}: {e}")
            return []
