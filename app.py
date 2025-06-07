from flask import Flask, request, jsonify
import captain_picker

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'database': 'up',
        'external_api': 'up'
    })

@app.route('/')
def home():
    return "FPL Captaincy Picker is running!"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    team = data.get('team', [])
    gameweek = data.get('gameweek', 12)

    top_picks = captain_picker.recommend_captains(team, gameweek)
    return jsonify(top_picks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)