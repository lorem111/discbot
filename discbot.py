import asyncio
from datetime import datetime
import discord
from discord.ext import commands
import requests
import json
import os
from dotenv import load_dotenv
import psutil
import shutil
import image_gen
import voice_gen
import whisper_gen

import socket
device_name = socket.gethostname()

# Disk Usage
total, used, free = shutil.disk_usage("/")
total_GB = total // (2**30)
used_GB = used // (2**30)
free_GB = free // (2**30)
# RAM Usage
memory_info = psutil.virtual_memory()
total_ram_MB = memory_info.total // (2**20)
used_ram_MB = memory_info.used // (2**20)
available_ram_MB = memory_info.available // (2**20)
# CPU Usage
cpu_usage = psutil.cpu_percent(interval=1)

# Load the .env file
load_dotenv()

# Specify the API key and headers
api_key = os.getenv("GPT4_API_KEY")
print(f'Bearer {api_key}')
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# Specify the URL

url = 'https://api.openai-365pro.com/v1/chat/completions'
# Make the POST request
def query_gpt4(input_text):
    # Specify the data you want to send
    data = {
        "model": "gpt-4-0613",
        "messages": [{"role": "system", "content": "You are ChatGPT 4.5. Provide an helpful answer to the user."}, 
                     {"role": "user", "content": f"{input_text}"}],
        'max_tokens': 200,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Print the response
    print(response.json())
    return response.json()

def query_gpt3(input_text):
    # Specify the data you want to send
    data = {
        "model": "gpt-3.5-turbo-0613",
        "messages": [{"role": "system", "content": "You are ChatGPT 3.5. Operate based on following instructions: Each sentence may only have 5 words. Make sure to adjust every response to be as if you're a dog barking. (like uwu, but as dog)"}, 
                     {"role": "user", "content": f"{input_text}"}],
        'max_tokens': 200,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Print the response
    print(response.json())
    return response.json()

def query_p(input_text):
    # Specify the data you want to send
    data = {
        "model": "gpt-3.5-turbo-0613",
        "messages": [{"role": "user", "content": f"{input_text}"}],
        'max_tokens': 1000,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Print the response
    print(response.json())
    return response.json()


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    guild = bot.get_guild(602000421866831872)  # replace with your guild ID
    if guild is not None:
        # Get a specific voice channel in that guild by its ID.
        channel = discord.utils.get(guild.voice_channels, id=1125053778027106314)  # replace with your voice channel ID
        # Connect to that voice channel.
        if channel is not None:
            await channel.connect()
        else:
            print(f'No channel with id 987654321 found in guild {guild.name}')
    else:
        print('No guild with id 123456789 found')


@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!")
        return
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        print("joining channel: " + str(voice_channel))
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

@bot.command()
async def stream(ctx, *, input_text: str):
    counter = 0
    filename = "bella.mp3"
    voice_gen.voice_gen(input_text, filename)
    # Check if 'bella.mp3' exists every 5 seconds
    while not os.path.exists('bella.mp3') and counter < 25:
        await asyncio.sleep(5)
        counter += 1

    if os.path.exists('bella.mp3'):
        # If file exists, upload it to Discord
        audio_source = discord.FFmpegPCMAudio('bella.mp3')  # replace 'your_audio_file.mp3' with your file
        await ctx.send(file=discord.File('bella.mp3'))
        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(audio_source, after=lambda e: after_playing(e, ctx))
        else:
            await ctx.send("Already playing audio.")

def after_playing(error, ctx):
    if error:
        print(f'Player error: {error}')
    else:
        coro = post_play_function(ctx)
        fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
        try:
            fut.result()
        except:
            # an error happened in a background task
            pass
        
async def post_play_function(ctx):
    # Delete the file
    print("Ending the stream.")
    #os.remove('bella.mp3')
    filename = 'bella.mp3'
    # Get the current date and time.
    now = datetime.now()
    # Format it as a string.
    now_str = now.strftime('%Y%m%d_%H%M%S')
    # Create the new filename by replacing the .mp3 extension with _{date}.mp3.
    new_filename = filename.replace('.mp3', f'_{now_str}.mp3')
    new_path = os.path.join('archive', new_filename)
    # Move and rename the file.
    shutil.move(filename, new_path)





@bot.command()
async def voice(ctx, *, input_text: str):
    counter = 0
    filename = "bella.mp3"
    voice_gen.voice_gen(input_text, filename)
    # Check if 'bella.mp3' exists every 5 seconds
    while not os.path.exists('bella.mp3') and counter < 25:
        await asyncio.sleep(5)
        counter += 1

    if os.path.exists('bella.mp3'):
        # If file exists, upload it to Discord
        await ctx.send(file=discord.File('bella.mp3'))
        # Delete the file
        os.remove('bella.mp3')

@bot.command()
async def whisper(ctx):
    response = whisper_gen.make_whisper()['text']
    print(response)
    await ctx.send(response)

@bot.command()
async def imagine(ctx, *, input_text: str):
    img_response = image_gen.make_image(input_text)
    await ctx.send('' + img_response)
@bot.command()
async def dalle(ctx, *, input_text: str):
    img_response = image_gen.dalle_image(input_text)
    await ctx.send('' + img_response)
@bot.command()
async def gpt(ctx, *, input_text: str):
    api_response = query_gpt4(input_text)
    message_content = api_response['choices'][0]['message']['content']
    await ctx.send('GPT4: ' + message_content)
@bot.command()
async def gpt4(ctx, *, input_text: str):
    api_response = query_gpt4(input_text)
    message_content = api_response['choices'][0]['message']['content']
    await ctx.send('GPT4: ' + message_content)
@bot.command()
async def g(ctx, *, input_text: str):
    api_response = query_gpt4(input_text)
    message_content = api_response['choices'][0]['message']['content']
    await ctx.send('GPT4: ' + message_content)
@bot.command()
async def bark(ctx, *, input_text: str):
    api_response = query_gpt3(input_text)
    message_content = api_response['choices'][0]['message']['content']
    await ctx.send('Bark dog: ' + message_content)
@bot.command()
async def gpt3(ctx, *, input_text: str):
    api_response = query_p(input_text)
    message_content = api_response['choices'][0]['message']['content']
    await ctx.send('GPT3: ' + message_content)
@bot.command()
async def commands(ctx):
    await ctx.send('Current commands are !gpt (GPT4), !gpt3 (GPT3), and !p (GPT3)')
@bot.command()
async def cpu(ctx):
    await ctx.send("\n Total RAM: %d MB, Used RAM: %d MB, Available RAM: %d MB" % (total_ram_MB, used_ram_MB, available_ram_MB))
    await ctx.send("\nCPU usage: %f%%" % cpu_usage)
    await ctx.send("Total: %d GB, Used: %d GB, Free: %d GB" % (total_GB, used_GB, free_GB))

bot.run('MTEyNDE1MjAxNTI5NjEzOTI2NA.GQyRIQ.2PExhR1_5tdF1zxHPFSCzcw-78vff77v2Hb_XA')
