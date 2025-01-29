CREATE TABLE Anime (
	anime_id INT PRIMARY KEY,
	title_romaji VARCHAR(255) NOT NULL,
	title_english VARCHAR(255),
	episodes INT,
	status VARCHAR(50),
	start_date DATE
);

CREATE TABLE Genres (
	genre_id SERIAL PRIMARY KEY,
	genre_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Anime_Genres (
	anime_id INT REFERENCES Anime(anime_id) ON DELETE CASCADE,
	genre_id INT REFERENCES Genres(genre_id) ON DELETE CASCADE,
	PRIMARY KEY (anime_id, genre_id)
);

CREATE TABLE Ratings (
	anime_id INT PRIMARY KEY REFERENCES Anime(anime_id) ON DELETE CASCADE,
	average_score INT CHECK (average_score BETWEEN 0 AND 100),
	popularity INT CHECK (popularity >= 0)
);

CREATE TABLE Studios (
	studio_id SERIAL PRIMARY KEY,
	studio_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Anime_Studios (
	anime_id INT REFERENCES Anime(anime_id) ON DELETE CASCADE,
	studio_id INT REFERENCES Studios(studio_id) ON DELETE CASCADE,
	PRIMARY KEY (anime_id,studio_id)
);

CREATE TABLE Anime_Relationships (
	anime_id INT REFERENCES Anime(anime_id) ON DELETE CASCADE,
	related_anime_id INT REFERENCES Anime(anime_id) ON DELETE CASCADE,
	relation_type VARCHAR(50) NOT NULL CHECK (relation_type IN ('SEQUEL', 'PREQUEL', 'ADAPTATION', 'SPINOFF', 'SIDE STORY', 'OTHER')),
	PRIMARY KEY (anime_id, related_anime_id, relation_type)
);