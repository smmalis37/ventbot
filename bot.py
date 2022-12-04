import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import functools
import random
import typing


# Additional logging, if needed
# import logging
# logging.basicConfig(level=logging.INFO)

# Ensure messages get logged correctly
print = functools.partial(print, flush=True)

# The id of the channel to monitor
channel_id = 886679404330242108

# The discord connection client
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot("!", intents=intents, activity=discord.Game("https://github.com/smmalis37/ventbot"))

# The task that actually does work
task = None


# Run once the client is fully connected and synced
# If there is a disconnect and reconnect, this will run again
@client.event
async def on_ready():
    global task
    print("Connected.")
    if task == None:
        print("Scheduling task.")
        # Schedule the process_messages task to run immediately
        task = asyncio.ensure_future(process_messages())

# Run after a disconnect if able to resume the connection instead of needing to make a fresh connection
@client.event
async def on_resumed():
    print("Resumed.")
    await on_ready()

# Run whenever the client loses connection to discord for any reason
@client.event
async def on_disconnect():
    global task
    if task != None:
        print("Lost connection, cancelling.")
        # Stop the task from running, since it can't do anything right now
        task.cancel()
        task = None

async def process_messages():
    # Repeat forever
    while True:
        print("Beginning processing.")
        # Get the channel we're monitoring
        channel = client.get_channel(channel_id)
        print("Reading from " + channel.name)
        # Calculate the time 7 days ago
        timestamp = datetime.now() - timedelta(days=7)
        print("Messages older than " + str(timestamp))
        # Get all messages before that time
        messages = await channel.history(before=timestamp, limit=None).flatten()
        print("Deleting " + str(len(messages)) + " messages.")
        # Delete the messages
        for m in messages:
            if (not m.pinned):
                await m.delete()
        # Wait to run again
        print("Waiting 1 hour.")
        await asyncio.sleep(60 * 60)


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
