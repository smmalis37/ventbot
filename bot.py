import discord
import asyncio
from datetime import datetime, timedelta
import functools

# Ensure messages get logged correctly
print = functools.partial(print, flush=True)

# The id of the channel to monitor
channel_id = 733925968955047936
# The discord connection client
client = discord.Client(fetch_offline_members=True, guild_subscriptions=False,
                        activity=discord.Game("https://github.com/smmalis37/ventbot"))
# The task that actually does work
task = None

# Run once the client is fully connected and synced
# If there is a disconnect and reconnect, this will run again


@client.event
async def on_ready():
    global task
    print("Connected.")
    # Schedule the process_messages task to run immediately
    task = asyncio.ensure_future(process_messages())


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
    while True:
        # Get the channel we're monitoring
        channel = client.get_channel(channel_id)
        print("Reading from " + channel.name)
        # Calculate the time 7 days ago
        timestamp = datetime.now() - timedelta(days=7)
        print("Messages older than " + str(timestamp))
        # Get all messages before that time
        messages = await channel.history(before=timestamp).flatten()
        print("Deleting " + str(len(messages)) + " messages.")
        # Delete the messages
        # await channel.delete_messages(messages)
        # Wait to run again
        print("Waiting 1 hour.")
        await asyncio.sleep(60 * 60)


if __name__ == '__main__':
    # The connection token must be in a file named creds
    with open("creds") as f:
        creds = f.readlines()[0].strip()
    client.run(creds)
