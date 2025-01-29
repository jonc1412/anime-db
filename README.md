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