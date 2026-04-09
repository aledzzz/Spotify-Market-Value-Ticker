# Music Identification and Data Valuation Tool 

Spotify Market Value Ticker is a Fintech-inspired "Shazam" that indentifies music via audio fingerprinting and calculates the estimated gross/net revenue royalties based on the 2026 music industry standards.

# Key Features
- Audio Fingerprinting: Using 'librosa' to map acoustic data
- Market Valuation: Calculates estimated revenue using the current industry baseline ($0.004 per stream)
- Monetization Floor: Flags tracks that have reached 1,000 streams within a rolling 12-month period

# Setup
1.) Clone the repository
'''
https://github.com/aledzzz/Spotify-Market-Value-Ticker.git
'''
2.) Create a virtual environment
'''
python -m venv venv
'''
3.) Install dependencies
'''
pip install -r requirements.txt
'''
4.) Add Spotify API Keys to '.env' file

5.) Run
'''
python main.py
'''


