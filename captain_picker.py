import requests
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_player_data():
    return requests.get(BOOTSTRAP_URL).json()

def score_player(player):
    form = float(player['form'])
    ppg = float(player['points_per_game'])
    minutes = player['minutes']
    modifier = 0.8 if minutes < 800 else 1.0
    return round((form * 0.5 + ppg * 0.5) * modifier, 2)

def recommend_captains(team):
    data = fetch_player_data()
    player_lookup = {p['id']: p for p in data['elements']}
    player_ids = [p['id'] for p in team]

    scored = []
    for pid in player_ids:
        player = player_lookup.get(pid)
        if player:
            score = score_player(player)
            scored.append({
                "id": pid,
                "name": player['web_name'],
                "score": score,
                "form": player['form'],
                "ppg": player['points_per_game'],
                "minutes": player['minutes']
            })

    return sorted(scored, key=lambda p: p['score'], reverse=True)[:3]

def recommend_captain_llm(top_players, gameweek):
    prompt = f"""
You are a Fantasy Premier League (FPL) expert. Based on the following player stats for Gameweek {gameweek}, recommend the best captain:

Players:
{json.dumps(top_players, indent=2)}

Each player includes:
- name
- form (recent performance)
- ppg (points per game)
- minutes
- score (precomputed)
    
Pick the best captain and explain briefly why.
"""

    try:
        if os.getenv("ENV") == "prod":
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
            model = "gpt-4o-mini"
            logger.info(f"Starting chat with OpenAI model: {model}")
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert Fantasy Premier League assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            content = response['choices'][0]['message']['content']
        else:
            model = os.getenv("OLLAMA_MODEL", "mistral")
            logger.info(f"Starting chat with Ollama model: {model}")
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are an expert Fantasy Premier League assistant."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            content = response.json()["message"]["content"]

        return {"llm_recommendation": content.strip()}

    except Exception as e:
        return {"error": str(e)}