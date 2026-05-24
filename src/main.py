import os
import random
import time
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from myserver import server_on

load_dotenv()
TOKEN = os.environ.get('token')

bot = commands.Bot(command_prefix="\\", intents=discord.Intents.all(),help_command=None)
status = "/help PokePoke"


async def load_extensions():
    extensions = ['cogs.general', 'cogs.voice', 'cogs.poke']
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f'Successfully loaded extension: {ext}')
        except Exception as e:
            print(f'Failed to load extension {ext}: {e}')

bot.setup_hook = load_extensions

@bot.event
async def on_ready():
    print("Now online!!")
    activity = discord.Activity(type=discord.ActivityType.playing, name=status)
    await bot.change_presence(activity=activity)
    synced = await bot.tree.sync()
    print(f'{len(synced)} command(s) Logged in as {bot.user}')


server_on()

MAX_RETRIES = 10
BASE_DELAY = 60  # Initial wait of 60 seconds
for attempt in range(MAX_RETRIES):
    try:
        # Note: Discord/Cloudflare 429 (Error 1015) is a known issue on Render's shared IPs.
        # This loop waits for the rate limit to expire instead of crashing the bot.
        bot.run(TOKEN)
        break  
    except discord.errors.HTTPException as e:
        if e.status == 429:
            # Add some jitter to avoid synchronized restarts with other bots on the same IP
            delay = BASE_DELAY + random.uniform(0, 30)
            print(f"!!! DIscord Rate Limit !!! (429/1015)")
            print(f"This is likely due to Render's shared IP address being flagged by Discord.")
            print(f"Waiting {delay:.1f}s before retry {attempt + 1}/{MAX_RETRIES}...")
            time.sleep(delay)
        else:
            print(f"Serious Discord error: {e}")
            break
    except Exception as e:
        print(f"The bot encountered an unexpected error: {e}")
        break