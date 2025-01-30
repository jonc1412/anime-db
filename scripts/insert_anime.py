import psycopg2
import json
from dotenv import load_dotenv
import os

load_dotenv()

with open("data/anime_data.json", "r", encoding="utf-8") as f:
    anime_data = json.load(f)

DB_NAME = os.getenv("PG_DB")
DB_USER = os.getenv("PG_USER")
DB_PASSWORD = os.getenv("PG_PASSWORD")
DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")


conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

for anime in anime_data:
    anime_id = anime["id"]
    title_romaji  = anime["title"]["romaji"]
    title_english = anime["title"]["english"]
    episodes = anime["episodes"]
    status = anime["status"]
    start_date = f"{anime['startDate']['year']}-{anime['startDate']['month']:02d}-{anime['startDate']['day']:02d}"

    cur.execute("""
        INSERT INTO Anime (anime_id, title_romaji, title_english, episodes, status, start_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (anime_id) DO NOTHING;
        """, (anime_id, title_romaji, title_english, episodes, status, start_date))

    for genre in anime["genres"]:
        cur.execute("""
            INSERT INTO Genres (genre_name)
            VALUES (%s)
            ON CONFLICT (genre_name) DO NOTHING
            """, (genre,))

        cur.execute("SELECT genre_id FROM Genres WHERE genre_name = %s;", (genre,))
        genre_id = cur.fetchone()[0] 

        cur.execute("""
            INSERT INTO Anime_Genres (anime_id, genre_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING;
            """, (anime_id, genre_id))
                
    for studio in anime["studios"]["nodes"]:
        studio = studio["name"]
        cur.execute("""
            INSERT INTO Studios (studio_name)
            VALUES (%s)
            ON CONFLICT (studio_name) DO NOTHING
            """, (studio,))
        
        cur.execute("SELECT studio_id FROM Studios WHERE studio_name = %s;", (studio,))
        studio_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO Anime_Studios (anime_id, studio_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING;
            """, (anime_id, studio_id))

conn.commit()
cur.close()
conn.close()