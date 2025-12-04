import sqlite3

class DatabaseClient:
    def __init__(self, db_name="nba_props.db"):
        """
        Initializes the database client and connects to the SQLite database.
        It also ensures that the necessary tables are created.
        """
        self.db_name = db_name
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row # Allows accessing columns by name
            print(f"Successfully connected to database: {self.db_name}")
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def create_tables(self):
        """
        Creates the 'games' and 'odds' tables if they do not already exist.
        This is designed to be run safely on every initialization.
        """
        if not self.conn:
            print("Cannot create tables without a database connection.")
            return

        try:
            cursor = self.conn.cursor()
            # SQL command to create the games table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id TEXT PRIMARY KEY,
                    home_team TEXT NOT NULL,
                    away_team TEXT NOT NULL,
                    commence_time TEXT NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # You can add more tables here in the future, for example, for odds.
            self.conn.commit()
            print("Tables checked/created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def update_games(self, games_data):
        """
        Updates the games table with a list of games from the API.
        It uses INSERT OR REPLACE to either add new games or update existing ones.
        
        Args:
            games_data (list): A list of dictionaries, where each dictionary represents a game.
        """
        if not self.conn:
            print("Cannot update games without a database connection.")
            return

        sql = """
            INSERT OR REPLACE INTO games (id, home_team, away_team, commence_time)
            VALUES (?, ?, ?, ?);
        """
        try:
            cursor = self.conn.cursor()
            # Prepare data for bulk insertion
            games_to_insert = [(g['id'], g['home_team'], g['away_team'], g['commence_time']) for g in games_data]
            cursor.executemany(sql, games_to_insert)
            self.conn.commit()
            print(f"Successfully inserted/updated {len(games_to_insert)} games.")
        except sqlite3.Error as e:
            print(f"Error updating games in database: {e}")

    def close_connection(self):
        """
        Closes the database connection if it is open.
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
