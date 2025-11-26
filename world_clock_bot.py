import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

import discord

# ------------- EDIT THESE TWO LINES -------------
import os
TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = 1443299115797839995     # <- replace with your channel ID (no quotes)
# -----------------------------------------------

UPDATE_INTERVAL_SECONDS = 60  # how often the clock refreshes (seconds)

# Timezones to display: (label, IANA timezone name)
TIMEZONES = [
    ("PST (NA West)", "America/Los_Angeles"),
    ("CST (NA Central)", "America/Chicago"),
    ("EST (NA East)", "America/New_York"),
    ("CET (Europe)", "Europe/Berlin"),
    ("UTC+8 (Asia)", "Asia/Taipei"),  # change to Asia/Singapore etc. if you prefer
]

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def world_clock_loop():
    """Background task that keeps the world clock message updated."""
    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Could not find channel with ID {CHANNEL_ID}. Is the bot in that server?")
        return

    # Send the initial message once
    message = await channel.send("Starting world clock...")

    while not client.is_closed():
        now_utc = datetime.now(ZoneInfo("UTC"))

        lines = []
        lines.append("🌍 **World Clock** (auto-updates every minute)\n")

        for label, tz_name in TIMEZONES:
            tz = ZoneInfo(tz_name)
            local_time = now_utc.astimezone(tz)
            # Format: 2025-11-26 17:24  (change if you want)
            lines.append(f"**{label}** — {local_time:%Y-%m-%d %H:%M}")

        lines.append(f"\n_Last update:_ {now_utc:%Y-%m-%d %H:%M} UTC")

        content = "\n".join(lines)

        try:
            await message.edit(content=content)
        except Exception as e:
            print(f"Error editing message: {e}")

        await asyncio.sleep(UPDATE_INTERVAL_SECONDS)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    client.loop.create_task(world_clock_loop())


client.run(TOKEN)
