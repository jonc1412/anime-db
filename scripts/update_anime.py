# Step 1: Delete anime in the database that are not in the API call
def delete_outdated(conn, api_data):
    cur = conn.cursor()

    cur.execute("""
        SELECT anime_id
        FROM anime
    """)
    db_anime_ids = [row[0] for row in cur.fetchall()]
    api_anime_ids = [anime['id'] for anime in api_data]

    outdated_anime = [anime_id for anime_id in db_anime_ids if anime_id not in api_anime_ids]
    
    if outdated_anime:
        cur.executemany("""
            DELETE FROM anime
            WHERE anime_id = %s
        """, [(id,) for id in outdated_anime])

        conn.commit()

        print(f'Successfully deleted {len(outdated_anime)} outdated anime from the database')
    else:
        print('No changes were made')

    cur.close()

# Step 2: Check if any of the 'RELEASING' animes are updated (status, episodes)
def check_ongoing(conn, api_data):
    cur = conn.cursor()

    cur.execute("""
        SELECT anime_id, episodes, status
        FROM anime
        WHERE status = 'RELEASING'
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

        updates.append((average_score, popularity, anime_id))
    
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