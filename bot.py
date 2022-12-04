import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta
import functools
import random
import typing

# Ensure messages get logged correctly
print = functools.partial(print, flush=True)

# The id of the channel to monitor
channel_id = 886679404330242108

# The discord connection client
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot("!", intents=intents, activity=discord.Game("https://github.com/smmalis37/ventbot"))

@client.event
async def on_ready():
    print("Ready!")
    process_messages.start()

@tasks.loop(hours=1)
async def process_messages():
    print("Waiting for ready.")
    await client.wait_until_ready()
    print("Beginning processing.")
    # Get the channel we're monitoring
    channel = client.get_channel(channel_id)
    print("Reading from " + channel.name)
    # Calculate the time 7 days ago
    timestamp = datetime.now() - timedelta(days=7)
    print("Messages older than " + str(timestamp))
    # Get all messages before that time
    messages = [m async for m in channel.history(before=timestamp, limit=None) if not m.pinned]
    print("Deleting " + str(len(messages)) + " messages.")
    # Delete the messages
    for m in messages:
        await m.delete()
    print("Done.")

@client.command()
async def roll(ctx, count: typing.Optional[int] = 6, max: typing.Optional[int] = None):
    if max == None:
        max = count
        count = 1
    reply = ""
    for x in range(count):
        reply += str(random.randint(1, max)) + " "
    await ctx.reply(reply)

@client.command()
async def flip(ctx, count: typing.Optional[int] = 1):
    reply = ""
    for x in range(count):
        reply += random.choice(["Heads", "Tails"]) + " "
    await ctx.reply(reply)

@client.event
async def on_command_error(ctx, e):
    await ctx.reply(e)


if __name__ == '__main__':
    # The connection token must be in a file named creds
    with open("creds") as f:
        creds = f.readlines()[0].strip()
    client.run(creds)
