import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

import os
import discord

# ----- read from Fly secrets -----
TOKEN = os.environ["DISCORD_TOKEN"]          # set in Fly secrets
CHANNEL_ID = int(os.environ["CHANNEL_ID"])   # set in Fly secrets
# ---------------------------------

UPDATE_INTERVAL_SECONDS = 60  # how often the clock refreshes (seconds)

TIMEZONES = [
    ("PST (NA West)", "America/Los_Angeles"),
    ("CST (NA Central)", "America/Chicago"),
    ("EST (NA East)", "America/New_York"),
    ("CET (Europe)", "Europe/Berlin"),
    ("UTC+8 (Asia)", "Asia/Taipei"),
]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

...
# (rest of your file stays the same)
