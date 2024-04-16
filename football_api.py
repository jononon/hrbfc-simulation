import os
import httpx
from dotenv import load_dotenv

season = 2023
league_id = 51

load_dotenv()

# Create a client session for HTTP requests
client = httpx.Client(base_url='https://api-football-v1.p.rapidapi.com/v3/')


def get_fixtures():
    headers = {
        'x-rapidapi-key': os.environ['API_FOOTBALL_KEY'],
        'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
    }
    params = {
        'league': league_id,
        'season': season,
    }
    response = client.get('fixtures', headers=headers, params=params)
    return response.json()


def get_standings():
    headers = {
        'x-rapidapi-key': os.environ['API_FOOTBALL_KEY'],
        'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
    }
    params = {
        'league': league_id,
        'season': season,
    }
    response = client.get('standings', headers=headers, params=params)
    return response.json()
