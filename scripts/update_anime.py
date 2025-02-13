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

# Step 1: Delete anime in the database that are not in the API call
def delete_outdated(conn, api_data):
    cur = conn.cursor()

    cur.execute("""
        SELECT anime_id
        FROM anime
    """)
    db_anime = [row for row in cur.fetchall()]

    print(db_anime)

    outdated_anime = []
    for anime in api_data:
        anime_id = anime['id']

        if anime_id not in db_anime:
            outdated_anime.append(anime_id)
    
    if outdated_anime:
        cur.executemany(""""
            DELETE FROM anime
            WHERE anime_id = %s
        """, (anime_id))

        conn.commit()

        print('Successfully deleted outdated anime from the database')
    else:
        print('No changes were made')

    cur.close()

# Step 2: Check if any of the 'RELEASING' animes are updated (status, episodes)
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

# Step 3: Update the average_score and popularity of all anime
def update_rating(conn, api_data):
    cur = conn.cursor()

    updates = []
    for anime in api_data:
        anime_id = anime['id']
        popularity = anime['popularity']
        average_score = anime['averageScore']

        updates.append((anime_id, average_score, popularity))
    
    if updates:
        cur.executemany("""
            UPDATE Ratings
            SET average_score = %s, popularity = %s
            WHERE anime_id = %s
        """, updates)

        conn.commit()
        print('Successfully updated anime popularity and average_score')
    else:
        print('No changes were made')
    
    cur.close()

update_rating(conn, api_data)