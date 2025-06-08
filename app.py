from flask import Flask, request, jsonify
import captain_picker
from fpl import validate_gameweek
from fpl import FPLClient
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check requested")
    return jsonify({
        'database': 'up',
        'external_api': 'up'
    })

@app.route('/')
def home():
    logger.info("Home page accessed")
    return "FPL Captaincy Picker is running!"

@app.route('/recommend', methods=['POST'])
def recommend():
    logger.info("Captain recommendation requested")
    data = request.get_json()
    cookie = request.headers.get('Cookie')
    if not cookie:
        logger.warning("Authentication failed: Missing cookie")
        return jsonify({"error": "Missing authentication cookie in header."}), 400
    
    gameweek = data.get('gameweek', 12)
    use_llm = data.get('useLLM', False)
    logger.info(f"Processing recommendation for gameweek {gameweek}, useLLM: {use_llm}")

    # Validate gameweek
    is_valid, error_message = validate_gameweek(gameweek)
    if not is_valid:
        logger.warning(f"Invalid gameweek: {error_message}")
        return jsonify({"error": error_message}), 400

    try:
        client = FPLClient()
        client.set_auth_cookie(cookie)
        team = client.get_team_for_gameweek(gameweek - 1) # -1 because gameweek becasue we are predicting the next gameweek
        logger.info(f"Team: {team}")
        top3_picks = captain_picker.recommend_captains_from_team(team)
        logger.info(f"Top 3 picks: {top3_picks}")
        
        if use_llm:
            top_captain_pick = captain_picker.recommend_captain_llm(top3_picks, gameweek)
            logger.info(f"Successfully generated LLM captain recommendation")
        else:
            # If not using LLM, just return the top 3 picks with their scores
            top_captain_pick = {
                "recommendation": f"Top pick: {top3_picks[0]['name']} (Score: {top3_picks[0]['score']})",
                "player_scores": top3_picks
            }
            logger.info(f"Successfully generated score-based captain recommendation")
            
        return jsonify(top_captain_pick)
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/authenticate', methods=['POST'])
def authenticate():
    logger.info("Authentication request received")
    cookie = request.headers.get('Cookie')

    if not cookie:
        logger.warning("Authentication failed: Missing cookie")
        return jsonify({"error": "Missing authentication cookie in header."}), 400

    try:
        client = FPLClient()
        client.set_auth_cookie(cookie)
        logger.info("Successfully authenticated with FPL API")

        # Fetch and return bootstrap-static data
        bootstrap_url = "https://fantasy.premierleague.com/api/me/"
        resp = client.session.get(bootstrap_url)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch bootstrap data: Status code {resp.status_code}")
            return jsonify({"error": "Failed to fetch bootstrap data"}), 500

        logger.info("Successfully fetched bootstrap data")
        return jsonify(resp.json())
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/team', methods=['GET'])
def get_team():
    logger.info("Team data request received")
    cookie = request.headers.get('Cookie')
    gameweek = request.args.get('gameweek', default=1, type=int)
    logger.info(f"Fetching team data for gameweek {gameweek}")

    if not cookie:
        logger.warning("Team data request failed: Missing cookie")
        return jsonify({"error": "Missing authentication cookie in header."}), 400

    # Validate gameweek
    is_valid, error_message = validate_gameweek(gameweek)
    if not is_valid:
        logger.warning(f"Invalid gameweek: {error_message}")
        return jsonify({"error": error_message}), 400

    try:
        client = FPLClient()
        client.set_auth_cookie(cookie)
        team = client.get_team_for_gameweek(gameweek)
        logger.info(f"Successfully retrieved team data for gameweek {gameweek}")
        return jsonify({"gameweek": gameweek, "team": team})
    except Exception as e:
        logger.error(f"Error fetching team data: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    logger.info("Starting FPL Captaincy Picker application")
    app.run(host='0.0.0.0', port=8000, debug=False)