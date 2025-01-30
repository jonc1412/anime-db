-- Get the Top 10 Most Popular Animes
SELECT a.title_english 
FROM ratings r
JOIN anime a USING (anime_id)
ORDER BY r.popularity DESC
LIMIT 10;

-- Get the Top 10 Highest Rated Animes
SELECT a.title_english 
FROM ratings r
JOIN anime a USING (anime_id)
ORDER BY r.average_score DESC
LIMIT 10;

-- Top 5 Studios That Worked on the Most Animes
SELECT s.studio_name, COUNT(as2.anime_id) AS anime_count
FROM anime_studios as2
JOIN studios s USING (studio_id)
GROUP BY s.studio_name 
ORDER BY anime_count DESC
LIMIT 5;

-- Top 5 Most Popular Anime by Genre
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
WHERE rank <= 5
ORDER BY genre ASC, popularity DESC;

-- Top 10 Most Successful Studios by Average Score
SELECT s.studio_name AS studio, AVG(r.average_score) AS "average score"
FROM anime a 
JOIN ratings r ON a.anime_id = r.anime_id
JOIN anime_studios as2 ON a.anime_id = as2.anime_id 
JOIN studios s ON as2.studio_id = s.studio_id 
GROUP BY s.studio_name
ORDER BY "average score" DESC
LIMIT 10;