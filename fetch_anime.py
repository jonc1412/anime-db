import requests
import json

url = "https://graphql.anilist.co"

def fetch_anime_data(total_anime, per_page=50):
    anime = []
    n_pages = total_anime // per_page

    for page in range(1, n_pages + 1):
        query = f"""
        {{
            Page(page: {page}, perPage: {per_page}) {{
                media(type: ANIME, sort: POPULARITY_DESC) {{
                    id
                    title {{
                        romaji
                        english
                    }}
                    genres
                    episodes
                    averageScore
                    popularity
                    status
                    startDate {{
                        year
                        month
                        day
                    }}
                    studios {{
                        nodes {{
                            name
                        }}
                    }}
                    relations {{
                        edges {{
                            relationType
                            node {{
                                title {{
                                    romaji
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """

        response = requests.post(url, json={"query": query})
    
        if response.status_code == 200:
            data = response.json()["data"]["Page"]["media"]
            anime.extend(data)
        else:
            print(f"API Error {response.status_code}: {response.text}")

    with open("data/anime_data.json", "w", encoding="utf-8") as f:
        json.dump(anime, f, indent=4, ensure_ascii=False)
    
fetch_anime_data(500)