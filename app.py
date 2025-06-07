from flask import Flask, request, jsonify
import captain_picker

app = Flask(__name__)

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
    app.run(debug=True)