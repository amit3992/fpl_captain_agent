# FPL Captain Picker

A Fantasy Premier League (FPL) tool that helps you choose the best captain for your team each gameweek. The tool uses both statistical analysis and AI-powered recommendations to suggest the optimal captain choice.

## Features

- Statistical analysis of player performance (form, points per game, minutes played)
- AI-powered captain recommendations using LLM
- REST API for easy integration
- Support for both score-based and LLM-based recommendations
- Real-time FPL data integration

## Prerequisites

- Python 3.8+
- FPL account and authentication cookie
- (Optional) OpenAI API key for production LLM usage
- (Optional) Ollama for local LLM usage

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fpl-captain-picker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# For production with OpenAI
export ENV=prod
export OPENAI_API_KEY=your_openai_api_key

# For local development with Ollama
export OLLAMA_MODEL=mistral  # or any other model you prefer
```

## Usage

### Starting the Server

```bash
python app.py
```

The server will start on `http://localhost:8000`

### API Endpoints

#### 1. Health Check
```bash
GET /health
```
Checks if the service is running properly.

#### 2. Captain Recommendation
```bash
POST /recommend
```
Get captain recommendations for a specific gameweek.

Request body:
```json
{
    "gameweek": 12,
    "useLLM": true  // Optional: Set to true for AI-powered recommendations
}
```

Headers:
```
Cookie: your_fpl_cookie
```

Response:
```json
{
    "recommendation": "Player recommendation with reasoning",
    "player_scores": [
        {
            "id": 123,
            "name": "Player Name",
            "score": 8.5,
            "form": "7.5",
            "ppg": "6.8",
            "minutes": 810
        }
        // ... more players
    ]
}
```

#### 3. Team Data
```bash
GET /team?gameweek=12
```
Get your team data for a specific gameweek.

Headers:
```
Cookie: your_fpl_cookie
```

#### 4. Authentication
```bash
POST /authenticate
```
Verify your FPL authentication.

Headers:
```
Cookie: your_fpl_cookie
```

## How It Works

1. **Statistical Analysis**
   - Calculates player scores based on:
     - Form (recent performance)
     - Points per game
     - Minutes played
   - Applies modifiers for players with limited playing time

2. **AI Recommendations**
   - When `useLLM` is enabled, uses either:
     - OpenAI's GPT-4 (in production)
     - Local Ollama model (in development)
   - Provides detailed reasoning for captain selection

3. **Gameweek Handling**
   - Validates gameweek numbers (1-38)
   - Uses previous gameweek's team data for predictions
   - Returns top 3 potential captain picks

## Development

### Local Development
1. Install Ollama for local LLM support
2. Set up your environment variables
3. Run the server in development mode

### Production Deployment
1. Set up OpenAI API key
2. Configure production environment variables
3. Deploy to your preferred hosting platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Acknowledgments

- Fantasy Premier League API
- OpenAI for LLM capabilities
- Ollama for local LLM support 