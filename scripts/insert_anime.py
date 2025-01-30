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
    average_score = anime.get("averageScore")
    popularity = anime.get("popularity")
    status = anime["status"]
    start_date = f"{anime['startDate']['year']}-{anime['startDate']['month']:02d}-{anime['startDate']['day']:02d}"

    cur.execute("""
        INSERT INTO Anime (anime_id, title_romaji, title_english, episodes, status, start_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (anime_id) DO NOTHING;
        """, (anime_id, title_romaji, title_english, episodes, status, start_date))
    
    cur.execute("""
        INSERT INTO ratings (anime_id, average_score, popularity)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
        """, (anime_id, average_score, popularity))

    for genre in anime["genres"]:
        cur.execute("""
            INSERT INTO Genres (genre_name)
            VALUES (%s)
            ON CONFLICT (genre_name) DO NOTHING
            """, (genre,))

        cur.execute("SELECT genre_id FROM Genres WHERE genre_name = %s;", (genre,))
        result = cur.fetchone()
        genre_id = result[0] if result else None 

        cur.execute("""
            INSERT INTO Anime_Genres (anime_id, genre_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING;
            """, (anime_id, genre_id))
                
    for studio in anime["studios"]["nodes"]:
        studio_name = studio["name"]
        cur.execute("""
            INSERT INTO Studios (studio_name)
            VALUES (%s)
            ON CONFLICT (studio_name) DO NOTHING
            """, (studio_name,))
        
        cur.execute("SELECT studio_id FROM Studios WHERE studio_name = %s;", (studio_name,))
        result = cur.fetchone()
        studio_id = result[0] if result else None 

        cur.execute("""
            INSERT INTO Anime_Studios (anime_id, studio_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING;
            """, (anime_id, studio_id))
        
for anime in anime_data:
    anime_id = anime["id"]

    for relation in anime["relations"]["edges"]:
        related_title = relation["node"]["title"]["romaji"]
        cur.execute("SELECT anime_id FROM Anime WHERE title_romaji = %s;", (related_title,))
        result = cur.fetchone()
        related_id = result[0] if result else None

        if related_id:
            cur.execute("""
                INSERT INTO Anime_Relationships (anime_id, related_anime_id, relation_type)
                VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;
            """, (anime_id, related_id, relation["relationType"]))

conn.commit()
cur.close()
conn.close()