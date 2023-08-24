# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import glob
import openai
import os 
import utility

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Specify the API key and headers
openai.api_key = os.getenv("OPENAI_API_KEY")

def make_whisper():
    # Get a list of all .mp3 files
    mp3_files = glob.glob(os.path.join(os.getcwd(), "archive", "*.mp3"))
    # Find the most recent file
    latest_file = max(mp3_files, key=os.path.getmtime)
    # Open the file
    audio_file = open((os.getcwd() + "\\archive\\sample7.mp3"), "rb")
    #audio_file = open(latest_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    utility.tprint(transcript)
    return(transcript)

make_whisper()