import psycopg2
import json
import os
from dotenv import load_dotenv

load_dotenv()

with open("data/anime_data.json", "r", encoding="utf-8") as f:
    api_data = json.load(f)

DB_NAME = os.getenv("PG_DB")
DB_USER = os.getenv("PG_USER")
DB_PASSWORD = os.getenv("PG_PASSWORD")
DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

cur.execute("""
        SELECT anime_id, episodes, status, average_score, popularity
        FROM anime a
        JOIN Ratings r USING (anime_id)
        """)
existing_data = {row[0]: {
    'episodes': row[1],
    'status': row[2],
    'average_score': row[3],
    'popularity': row[4]
} for row in cur.fetchall()}

for anime in api_data:
    anime_id = anime['id']

    if anime in existing_data:
        if existing_data[anime_id]['status'] == 'RELEASING':
            