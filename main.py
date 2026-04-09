from dotenv import load_dotenv
import os

load_dotenv()

def main():
    print("Welcome to the Spotify Market Value Ticker!")

    # include audio and data processing here

    # record 10 seconds of audio (include code here)
    print("Play song now...")

    # process and analyze the audio to identify the song
    # include test track to see if API works correctly
    song_title = "Test Song"
    artist_name = "Test Artist"

    # run the valuation
    print(f"Generating market value for: {song_title} by {artist_name}")
    reported_valuation = 1000000 #placeholder

    #displaty the market dashboard
    print("----------")
    print(f"Track: {song_title} | Artist: {artist_name}")
    print(f"Estimated Market Value: ${reported_valuation:.2f}")

if __name__ == "__main__":
    main()
