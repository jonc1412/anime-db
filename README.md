# Anime Database

This project stores and analyzes anime data using **Postgres** and **Python** utilizing the `psycopg2` library. Data is fetched from the **AniList API** and structured into a relational database.

### Features
- Fetches anime data from **AniList API**
- Stores structured anime data and analyzes them in **PostgreSQL**

## Project Structure
```
📂 anime-database
│── 📁 data                 # Stores JSON anime data
│── 📁 docs                 # Stores documentation
│── 📁 queries              # SQL query scripts
│── 📁 scripts              # Python scripts for fetching & inserting data
│── 📄 .gitignore           # Ignore file
│── 📄 README.md            # Project documentation
```


## Database Schema
The database consists of the following tables:

- **`Anime`** - Stores anime titles and basic information.
- **`Genres`** - Stores different genres.
- **`Anime_Genres`** - A many-to-many join table linking anime and genres.
- **`Ratings`** - Stores popularity and average scores for each anime.
- **`Studios`** - Stores information about anime studios.
- **`Anime_Studios`** - A many-to-many join table linking anime and studios.
- **`Anime_Relationships`** - Stores relationships between anime (prequels, adaptations, etc.).

### Entity-Relationship Diagram (ERD)
Below is a visual representation of the database schema.
![ERD_Diagram](https://github.com/user-attachments/assets/e7be03ad-28b5-42d3-86cc-df3d16cb7384)

## Fetching Anime Data from AniList API
This project retrieves anime data from the **AniList API** using Python. The fetched data is stored in a JSON file [anime_data]('data/anime_data.json') and then instered into a **PostgreSQL database**

### About AniList API
This project fetches anime data from **[AniList API](https://docs.anilist.co/)**, a free GraphQL-based API for anime, manga, and user data.

### How Data is Fetched
1. **Send a GraphQL Query to AniList API** using Python (`requests`).
2. **Retrieve JSON Data** (anime titles, genres, scores, relations, etc.).
3. **Save the Data to `data/anime_data.json`**.
4. **Insert the Data into PostgreSQL** using `psycopg2`.

### Rate Limiting
The AniList API has a rate limit of 90 requests per minute **(currently, the API is in a degraded state and is limited to 30 requests per minute)**.

### Example JSON Response (Click to Expand)
<details>
    <summary>Click to expand JSON example</summary>
    
```json
{
    "id": 98478,
    "title": {
        "romaji": "3-gatsu no Lion 2",
        "english": "March comes in like a lion Season 2"
    },
    "genres": ["Drama", "Slice of Life"],
    "episodes": 22,
    "averageScore": 89,
    "popularity": 114660,
    "status": "FINISHED",
    "startDate": {
        "year": 2017,
        "month": 10,
        "day": 14
    },
    "studios": {
        "nodes": [
            { "name": "Shaft" },
            { "name": "Aniplex" }
        ]
    },
    "relations": {
        "edges": [
            { "relationType": "PREQUEL", "node": { "title": { "romaji": "3-gatsu no Lion" } } },
            { "relationType": "ADAPTATION", "node": { "title": { "romaji": "3-gatsu no Lion" } } },
            { "relationType": "OTHER", "node": { "title": { "romaji": "I AM STANDING" } } }
        ]
    }
}
```

</details>

## Example Queries

### Most Popular Anime by Genre
```sql
WITH PopularityGenre AS (
	SELECT 
		g.genre_name AS genre,
		a.title_english AS title,
		r.popularity,
		RANK() OVER (PARTITION BY g.genre_name ORDER BY r.popularity DESC)
	FROM anime a
	JOIN ratings r ON a.anime_id = r.anime_id
	JOIN anime_genres ag ON a.anime_id = ag.anime_id
	JOIN genres g ON ag.genre_id = g.genre_id
)
SELECT genre, title, popularity
FROM PopularityGenre 
WHERE rank <= 1
ORDER BY genre ASC, popularity DESC;
```

<details>
    <summary>Click to see Output</summary>

| genre           | title                          | popularity |
|---------------|---------------------------------|------------|
| Action        | Attack on Titan                | 835,234    |
| Adventure     | Demon Slayer: Kimetsu no Yaiba | 791,871    |
| Comedy       | My Hero Academia               | 715,098    |
| Drama        | Attack on Titan                | 835,234    |
| Ecchi        | No Game, No Life               | 455,472    |
| Fantasy      | Attack on Titan                | 835,234    |
| Horror       | Tokyo Ghoul                    | 600,389    |
| Mahou Shoujo | Puella Magi Madoka Magica      | 263,184    |
| Mecha        | DARLING in the FRANXX          | 405,397    |
| Music        | Your Lie in April              | 494,476    |
| Mystery      | Attack on Titan                | 835,234    |
| Psychological| Death Note                     | 760,078    |
| Romance      | Sword Art Online               | 586,667    |
| Sci-Fi       | One-Punch Man                  | 628,937    |
| Slice of Life| A Silent Voice                 | 556,751    |
| Sports       | HAIKYU!!                        | 483,106    |
| Supernatural | Demon Slayer: Kimetsu no Yaiba | 791,871    |
| Thriller     | Death Note                     | 760,078    |

</details>


### Top 10 Most Successful Studios by Average Score
```sql
SELECT s.studio_name AS studio, AVG(r.average_score) AS "average score"
FROM anime a 
JOIN ratings r ON a.anime_id = r.anime_id
JOIN anime_studios as2 ON a.anime_id = as2.anime_id 
JOIN studios s ON as2.studio_id = s.studio_id 
GROUP BY s.studio_name
ORDER BY "average score" DESC
LIMIT 10;
```

<details>
    <summary>Click to see Output</summary>

| Studio Name                   | Average Score |
|-------------------------------|--------------|
| Studio Live                   | 89           |
| TOHO animation STUDIO         | 88           |
| Studio Guts                   | 88           |
| TAP                            | 88           |
| Magic Bus                     | 88           |
| Mushi Production              | 88           |
| Asahi Production              | 88           |
| Imagica Infos                 | 88           |
| qooop                          | 87           |
| Studio LAN                    | 86           |

</details>

## Power BI Dashboard
[genre_analysis.pdf](https://github.com/user-attachments/files/18719162/genre_analysis.pdf)
