from dotenv import load_dotenv
import os

load_dotenv()

clientid = os.getenv("spotify_clientid")
rate = float(os.getenv("royalty_per_stream"))
threshold = float(os.getenv("monetization_threshold"))
label_commission = float(os.getenv("label_commission"))
