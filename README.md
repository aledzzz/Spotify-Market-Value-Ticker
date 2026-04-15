# Streamfolio 

A Fintech-style Pygame program that displays a user's music portfolio based on their top 5 tracks and calculates the estimated gross/net revenue royalties using the 2026 music industry standards.

# Prerequistes
- Python 3.10+
- Last.fm account (grab a free API key here: https://www.last.fm/api/account/create)
- pip install manager 

# Key Features
- Top 5 Tracks: Fetches a user's top 5 tracks over a 12-month period using Last.fm API
- Market Valuation: Calculates estimated revenue using the current industry baseline ($0.004 per stream & ~30% platform cut)
- Monetization Floor: Flags tracks that have reached 1,000 streams within a rolling 12-month period

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
4.) Add your Last.fm API key to the .env file
```
LASTFM_API_KEY = "input key here"
```
5.) Run
```
python main.py
```

