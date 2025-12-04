import pandas as pd
from datetime import datetime
from odds_api_client import OddsAPIClient
from database_client import DatabaseClient
from balldontlie_client import BallDontLieClient

class PropGenerationService:
    def __init__(self):
        self.api_client = OddsAPIClient()
        self.db_client = DatabaseClient()
        self.stats_client = BallDontLieClient()
        self.games_cache = []
        self.last_fetch_time = None

    def _fetch_and_cache_games(self):
        """Internal method to fetch games from API and update the cache."""
        print("Fetching fresh games from API...")
        raw_games = self.api_client.get_nba_games()
        self.games_cache = self._process_games(raw_games)
        self.last_fetch_time = datetime.now()

    def _process_games(self, raw_games):
        """Processes raw API game data into a cleaner list of dictionaries."""
        processed_games = []
        if not raw_games:
            return processed_games
        for game in raw_games:
            processed_games.append({
                'id': game['id'],
                'home_team': game['home_team'],
                'away_team': game['away_team'],
                'commence_time': game['commence_time'],
                'bookmakers': game.get('bookmakers', [])
            })
        return processed_games

    def get_all_games(self):
        """Provides a list of all available games, using a cache."""
        should_refetch = True
        if self.last_fetch_time:
            time_diff = datetime.now() - self.last_fetch_time
            if time_diff.total_seconds() < 300: # 5 minutes cache
                should_refetch = False
        
        if should_refetch or not self.games_cache:
            self._fetch_and_cache_games()
            
        return self.games_cache

    def get_game_by_id(self, game_id):
        """
        Finds a single game by its ID and enriches it with player stats.
        """
        if not self.games_cache:
            self.get_all_games() # Ensure cache is populated

        game_data = None
        for game in self.games_cache:
            if game['id'] == game_id:
                game_data = game
                break
        
        if not game_data:
            return None

        # --- Enrich with Historical Stats ---
        all_player_names = set()
        for bookmaker in game_data.get('bookmakers', []):
            for market in bookmaker.get('markets', []):
                # We only care about player prop markets
                if market.get('key', '').startswith('player_'):
                    for outcome in market.get('outcomes', []):
                        # Add the player's name to our set to avoid duplicates
                        player_name = outcome.get('description')
                        if player_name:
                            all_player_names.add(player_name)
        
        # Fetch stats for all unique players found in the odds
        player_stats = self.stats_client.get_multiple_player_season_averages(list(all_player_names))
        
        # Add the stats to the game_data object to be used by the UI
        game_data['player_stats'] = player_stats
        
        return game_data
