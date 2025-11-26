import os
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo   # Native timezones

import discord

# -----------------------------
# Load secrets from environment
# -----------------------------
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN secret missing! Set it in Fly.io > Secrets.")
if CHANNEL_ID == 0:
    raise RuntimeError("❌ CHANNEL_ID secret missing! Set it in Fly.io > Secrets.")

UPDATE_INTERVAL_SECONDS = 60  # refresh every minute

# Timezones to display
TIMEZONES = [
    ("PST (NA West)", "America/Los_Angeles"),
    ("CST (NA Central)", "America/Chicago"),
    ("EST (NA East)", "America/New_York"),
    ("CET (Europe)", "Europe/Berlin"),
    ("UTC+8 (Asia)", "Asia/Taipei"),
]

# Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def world_clock_loop():
    """Background updater for the clock message."""
    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"❌ Could not find channel ID {CHANNEL_ID}")
        return

    message = await channel.send("Starting world clock...")

    while not client.is_closed():
        now_utc = datetime.now(ZoneInfo("UTC"))

        lines = ["🌍 **World Clock** (auto-updates every minute)\n"]

        for label, tz_name in TIMEZONES:
            tz = ZoneInfo(tz_name)
            local_time = now_utc.astimezone(tz)
            lines.append(f"**{label}** — {local_time:%Y-%m-%d %H:%M}")

        lines.append(f"\n_Last update:_ {now_utc:%Y-%m-%d %H:%M} UTC")

        try:
            await message.edit(content="\n".join(lines))
        except Exception as e:
            print(f"⚠ Error editing message: {e}")

        await asyncio.sleep(UPDATE_INTERVAL_SECONDS)


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")
    client.loop.create_task(world_clock_loop())


client.run(TOKEN)
