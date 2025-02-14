import psycopg2
import json
from dotenv import load_dotenv
import os
from fetch_anime import fetch_anime_data
from insert_anime import add_anime
from update_anime import *

load_dotenv()

with open("data/anime_data.json", "r", encoding="utf-8") as f:
    anime_data = json.load(f)

DB_NAME = os.getenv("PG_DB")
DB_USER = os.getenv("PG_USER")
DB_PASSWORD = os.getenv("PG_PASSWORD")
DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

