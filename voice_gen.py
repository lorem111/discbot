import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import ffmpeg
import elevenlabs
from elevenlabs import generate, play, set_api_key, save, stream
import utility

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Specify the API key and headers
set_api_key(os.getenv("11LABS_API_KEY"))

def voice_gen(input, filename):
    #utility.tprint(input)
    audio = generate(
    #text="Hi! My name is Bella, nice to meet you! Hello everyone, my name is Bella. I'm a digital marketing specialist with a passion for storytelling and creating compelling content that resonates with audiences. I graduated from the University of California, Berkeley, with a degree in Communications and Media Studies, and since then, I have had the opportunity to work with a number of prominent brands, helping them increase their online visibility and engagement. In my spare time, I love exploring the great outdoors, reading thought-provoking books, and trying my hand at different artistic pursuits like painting and photography. One of my core beliefs is that genuine and meaningful connections can transform businesses and people's lives, which is why I'm always excited to meet new people and learn about their unique stories.",
    text=f"{input}",
    voice="Bella",
    model="eleven_monolingual_v1"
    )
    save(audio, filename)
    return

async def voice_gen_and_play(input, filename):
    #utility.tprint(input)
    audio = generate(
    #text="Hi! My name is Bella, nice to meet you! Hello everyone, my name is Bella. I'm a digital marketing specialist with a passion for storytelling and creating compelling content that resonates with audiences. I graduated from the University of California, Berkeley, with a degree in Communications and Media Studies, and since then, I have had the opportunity to work with a number of prominent brands, helping them increase their online visibility and engagement. In my spare time, I love exploring the great outdoors, reading thought-provoking books, and trying my hand at different artistic pursuits like painting and photography. One of my core beliefs is that genuine and meaningful connections can transform businesses and people's lives, which is why I'm always excited to meet new people and learn about their unique stories.",
    text=f"{input}",
    voice="Bella",
    model="eleven_monolingual_v1",
    stream=True
    )

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(stream, audio)
        executor.submit(utility.stprint, "Emily: ", input)
    #save(audio, filename)
    #await task_write
    #await task_stream

    #stream(audio)
    #utility.stprint("Emily: " + input)
    #save(audio, filename)
    return

# """Synthesizes speech from the input string of text or ssml.
# Make sure to be working in a virtual environment.

# Note: ssml must be well-formed according to:
#     https://www.w3.org/TR/speech-synthesis/
# """
# from google.cloud import texttospeech
# # Instantiates a client
# client = texttospeech.TextToSpeechClient()
# # Set the text input to be synthesized
# synthesis_input = texttospeech.SynthesisInput(text="Hello, World!")
# # Build the voice request, select the language code ("en-US") and the ssml
# # voice gender ("neutral")
# voice = texttospeech.VoiceSelectionParams(
#     language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
# )
# # Select the type of audio file you want returned
# audio_config = texttospeech.AudioConfig(
#     audio_encoding=texttospeech.AudioEncoding.MP3
# )
# # Perform the text-to-speech request on the text input with the selected
# # voice parameters and audio file type
# response = client.synthesize_speech(
#     input=synthesis_input, voice=voice, audio_config=audio_config
# )
# # The response's audio_content is binary.
# with open("output.mp3", "wb") as out:
#     # Write the response to the output file.
#     out.write(response.audio_content)
#     print('Audio content written to file "output.mp3"')