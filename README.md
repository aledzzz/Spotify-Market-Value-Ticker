# Streamfolio 

An end-to-end Fintech pipeline dashboard built to display a user's music portfolio based on their top 5 tracks and calculates the estimated gross/net revenue royalties using the 2026 music industry standards. Also focusing on real-time automation, this program vaults portfolio data into a local SQLite database and automatically generates CSV files to use within data visualization platforms.

# Prerequistes
- Python 3.11+
- Spotify and Spotipy API (grab Spotify API key here: https://developer.spotify.com/)
- SQLite 3 Editor (IDE extension)
- pip install manager 

# Key Features
- Top 5 Tracks: Fetches a user's top 5 tracks over a 12-month period using Spotify API
- Market Valuation: Calculates estimated revenue using the current industry baseline ($0.004 per stream & ~30% platform cut)
- Monetization Floor: Flags tracks that have reached 1,000 streams within a rolling 12-month period

# Architecture & API Limitations
The Spotify Web API fully redacts stream counts from its public endpoints. To maintain the overall integrity, this dashboard uses a hybrid approach.

If you are planning on cloning this repository, you have two options to populate the stream data:

1. Hardcode CLI Input (Recommended)
- Open ```music_data.py``` and locate the ```current_streams``` dictionary. You can manually search your top 5 tracks on the Spotify app within the last 12 months and input their exact stream count information into the variable. This pipeline will automatically merge these values with the live API data.

2. UI Simulation 
- Once the program encounters a track not listed within the dictionary, the terminal will pause and prompt you to manually enter the true stream count. If you simply press ```Enter```, the pipeline will automatically generate a simulated stream count using a randomized formula so you can test and render the dashboard UI.

# Setup
1.) Clone the repository
```
https://github.com/aledzzz/Streamfolio.git 
```
2.) Create a virtual environment
```
python -m venv venv
```
3.) Install dependencies
```
pip install -r requirements.txt
```
4.) Add your Spotify API keys to the .env file (REDIRECT_URI provided below)
```
CLIENT_ID = "client id here"
CLIENT_SECRET = "client secret here"
REDIRECT_URI = "http://127.0.0.1:8000/callback"
SCOPE = "user-top-read"
```
5.) Run
```
python main.py
```

> [!IMPORTANT]
> Due to the loss of my Spotify Premium subscription, I revamped the project to include a offline fallback mechanism. If the live API is empty or missing, the system intercepts the exception and injects a hardcoded mock dataset which allows the UI and data visualizations to remain fully operational without crashing.
