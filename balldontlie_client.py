import requests
import streamlit as st
import datetime

class BallDontLieClient:
    def __init__(self):
        self.api_key = st.secrets.get("BALLDONTLIE_API_KEY")
        if not self.api_key:
            raise ValueError("BALLDONTLIE_API_KEY not found in Streamlit secrets.")
        self.base_url = "https://www.balldontlie.io/api/v1"
        self.headers = {
            "Authorization": self.api_key
        }

    def _make_request(self, endpoint, params=None):
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None

    def get_todays_games(self):
        """
        Fetches today's NBA games.
        """
        today = datetime.date.today()
        params = {
            "start_date": today,
            "end_date": today
        }
        data = self._make_request("games", params=params)
        if data and data['data']:
            return data['data']
        return []
