import datetime
import textwrap

import discord
from discord.ext import commands, tasks
from util import *

client = commands.Bot('??', intents=discord.Intents.all())

@client.event
async def on_ready():
    print(client.user.name + ' is ready.')
    try: my_loop.start()
    except RuntimeError: ...
    
@client.event
async def on_raw_thread_delete(payload: discord.RawThreadDeleteEvent):
    threads.remove(payload.thread_id)

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if isinstance(message.channel, discord.Thread):
        thread = message.channel
        if thread.id in threads:
            messages = [
                f'{message.author.display_name}: {message.content}'
                async for message in thread.history(oldest_first=True)
            ][1:]
            messages.insert(0, await initial_message(message, client))
            prompt = SEPARATOR.join(messages)
            await thread.send(chatGPT(
                prompt
            ))
    else:
        if client.command_prefix not in message.content:
            if 'membean' in message.content.lower():
                reply = chatGPT(
                    'remind this person to do their membean:\n'
                    f'{message.author.display_name}: {message.content}'
                )
                await message.reply(reply)
    
    await client.process_commands(message)

@tasks.loop(seconds=60)
async def my_loop():
    now = datetime.datetime.now()
    if now.weekday() in (4, 5, 6) and now.hour == 23 and now.minute == 45:
        channel = client.get_channel(int(config['CHANNEL_ID']))
        if channel:
            prompt = (
                'Create a message to remind everyone to '
                'do their membean within the next 15 minutes.'
            )
            message = chatGPT(prompt)
            await channel.send(f"<@&755639888648339476> {message}")

@client.command()
async def prompt(ctx: commands.Context, *, prompt):
    if isinstance(ctx.channel, discord.Thread): return
    thread = await ctx.message.create_thread(name=prompt[:100])
    threads.append(thread.id)
    message = chatGPT(prompt)
    message_chunks = textwrap.wrap(message, width=2000)
    for chunk in message_chunks:
        await thread.send(chunk, mention_author=True)

@prompt.error
async def prompt_error(ctx: commands.Context, error: discord.DiscordException):
    ...

@client.command()
async def delete(ctx: commands.Context):
    if isinstance(ctx.channel, discord.Thread):
        if client.command_prefix in (await ctx.channel.parent.fetch_message(ctx.channel.id)).content:
            try:
                await ctx.channel.delete()
            except discord.Forbidden:
                await ctx.channel.leave()
                threads.remove(ctx.channel.id)
