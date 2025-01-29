# Anime Recommendation Database

## Overview
This project uses Python and PostgreSQL to store and analyze anime data. Data is sourced from the AniList API.

### Example JSON Response (Click to Expand)
<details>
    <summary>Show JSON</summary>

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
    
</details>

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

![ERD](https://private-user-images.githubusercontent.com/176351286/407717372-348c5cc8-d5e3-4747-9a10-4808eb98d522.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzgxNTEzOTMsIm5iZiI6MTczODE1MTA5MywicGF0aCI6Ii8xNzYzNTEyODYvNDA3NzE3MzcyLTM0OGM1Y2M4LWQ1ZTMtNDc0Ny05YTEwLTQ4MDhlYjk4ZDUyMi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMTI5JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDEyOVQxMTQ0NTNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hYTg5NzBlNzAxNGNlNTgxM2Q3MWY0Zjk5MmVkYjkwOGYxYzA4NTRkY2YyMDI0ZGE5MDA5ZGU5NTA0YjVjNGRlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.8C6saRW-SL0jlEW0JomPix6E1p-XyIGpJj1_rm8551Y)