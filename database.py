import sqlite3
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self, database_name = "streamfolio.db"):
        self.database_name = database_name
        self.create_database()

    def create_database(self):
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS streams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    track_id TEXT,
                    track_name TEXT,
                    artist_name TEXT,
                    album_img TEXT,
                    total_streams INTEGER,
                    gross REAL,
                    platform_fee REAL,
                    net_royalty_pool REAL,
                    timestamp DATE DEFAULT CURRENT_DATE,
                    UNIQUE(track_id, timestamp)
                )
            ''')
        
    def portfolio(self, portfolio_data):
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            
            for track in portfolio_data:
                cursor.execute('''
                    INSERT INTO streams (track_id, track_name, artist_name, album_img, total_streams, gross, platform_fee, net_royalty_pool)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                track.get('track_id'),
                track.get('name'),
                track.get('artist'),
                track.get('album_img'),
                track.get('total_streams'),
                track.get('gross'),
                track.get('platform_fee'),
                track.get('net_royalty_pool')
            ))
            print("Data saved!")

    def export(self):
        with sqlite3.connect(self.database_name) as conn:
            dataframe = pd.read_sql_query("SELECT * FROM streams", conn)
            dataframe.to_csv("streamfolio_portfolio.csv", index=False)
            print("Data exported!")