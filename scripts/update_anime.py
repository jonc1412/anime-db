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

# Step 1: Check if any of the 'RELEASING' animes are updated (status, episodes)
def check_ongoing(conn, api_data):
    cur = conn.cursor()

    cur.execute("""
        SELECT anime_id, episodes, status
        FROM anime
    """)
    ongoing_anime = {row[0]: {
        'episodes': row[1],
        'status': row[2]
    } for row in cur.fetchall()}

    updates = []
    for anime in api_data:
        anime_id = anime['id']

        if anime_id in ongoing_anime:
            old_status = ongoing_anime[anime_id]['status']
            old_episodes = ongoing_anime[anime_id]['episodes']

            new_status = anime['status']
            new_episodes = anime['episodes']

            if old_status != new_status or old_episodes != new_episodes:
                updates.append((new_episodes, new_status, anime_id))
    
    if updates:
        cur.executemany("""
            UPDATE anime
            SET episodes = %s, status = %s
            WHERE anime_id = %s
        """, updates)

        conn.commit()
        print('Successfully updated animes with the status (RELEASING)')
    else:
        print('No changes were made')

    cur.close()
