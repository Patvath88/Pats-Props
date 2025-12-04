import requests
import time

class BallDontLieClient:
    def __init__(self):
        self.base_url = "https://www.balldontlie.io/api/v1"

    def _make_request(self, endpoint, params=None):
        """Helper function to make requests to the API."""
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None

    def get_player_id(self, player_name):
        """Fetches the ID for a given player name."""
        data = self._make_request("players", params={"search": player_name})
        if data and data['data']:
            # Return the first match, which is usually the most relevant
            return data['data'][0]['id']
        return None

    def get_player_season_averages(self, player_name):
        """
        Fetches the current season's average stats for a single player.
        """
        player_id = self.get_player_id(player_name)
        if not player_id:
            return { "error": "Player not found" }
            
        params = {
            "player_ids[]": [player_id]
        }
        data = self._make_request("season_averages", params=params)
        
        if data and data['data']:
            return data['data'][0] # Return the stats dictionary
        return { "error": "Stats not found" }

    def get_multiple_player_season_averages(self, player_names):
        """
        Fetches season average stats for a list of player names.
        This is the new, efficient function.
        """
        player_stats = {}
        for name in player_names:
            if not name: continue # Skip if name is None or empty
            
            # Use the single-player function to get stats for each player
            stats = self.get_player_season_averages(name)
            player_stats[name] = stats
            
            # Be respectful to the API and avoid hitting rate limits
            time.sleep(0.7) # Wait 700ms between calls
            
        return player_stats
