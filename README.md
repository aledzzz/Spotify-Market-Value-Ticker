# Spotify Market Value Ticker 

Fintech-inspired "Shazam" that indentifies music via audio fingerprinting and calculates the estimated gross/net revenue royalties based on the 2026 music industry standards.

# Prerequistes
- Python 3.10+
- FFmpeg 7.0+
- Spotify Premium (needed in order to access Spotify Web API credentials)
- pip install manager 

# Key Features
- Audio Fingerprinting: Using 'librosa' to map acoustic data
- Market Valuation: Calculates estimated revenue using the current industry baseline ($0.004 per stream)
- Monetization Floor: Flags tracks that have reached 1,000 streams within a rolling 12-month period

# Setup
1.) Clone the repository
```
https://github.com/aledzzz/Spotify-Market-Value-Ticker.git
```
2.) Create a virtual environment
```
python -m venv venv
```
3.) Install dependencies
```
pip install -r requirements.txt
```
4.) Add Spotify API Keys to '.env' file
```
where to find api keys: https://developer.spotify.com/
```
5.) Run
```
python main.py
```

