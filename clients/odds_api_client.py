import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from db.database import SessionLocal, OddsApiCache

load_dotenv()

class OddsApiClient:
    def __init__(self):
        self.api_key = os.getenv("ODDS_API_KEY")
        if not self.api_key:
            raise ValueError("API key for The Odds API not found.")
        self.base_url = "https://api.the-odds-api.com/v4"
        self.db = SessionLocal()

    def get_odds_for_game(self, game: dict) -> dict | None:
        """
        Fetches player prop odds for a specific game.
        Uses a cache to avoid re-fetching data within a 6-hour window.
        """
        game_id = f"{game['home_team']['abbreviation']}_{game['visitor_team']['abbreviation']}_{game['date']}"

        # Check cache first
        cached_entry = self.db.query(OddsApiCache).filter(OddsApiCache.game_id == game_id).first()
        if cached_entry and (datetime.utcnow() - cached_entry.fetched_at < timedelta(hours=6)):
            return cached_entry.odds_data

        # If not in cache or stale, fetch from API
        endpoint = f"{self.base_url}/sports/basketball_nba/events/{game['id']}/odds"
        params = {
            "apiKey": self.api_key,
            "regions": "us",
            "markets": "player_points,player_rebounds,player_assists",
            "bookmakers": "fanduel,draftkings"
        }
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            odds_data = response.json()

            # Update cache
            if cached_entry:
                cached_entry.odds_data = odds_data
                cached_entry.fetched_at = datetime.utcnow()
            else:
                new_entry = OddsApiCache(game_id=game_id, odds_data=odds_data)
                self.db.add(new_entry)
            self.db.commit()

            return odds_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching odds for game {game_id}: {e}")
            self.db.rollback()
            return None
        finally:
            self.db.close()
