# bot.py
import os
import random
import copy
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

sslist = []
names = sslist
gifted = []
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def enroll(ctx):
    if ctx.author in sslist:
            await ctx.send("{} already enrolled".format(ctx.author))
    else:
        sslist.append(ctx.author)
        gifted.append(ctx.author)
        await ctx.send('{} enrolled in Secret Santa'.format(ctx.author))
    for member in ctx.message.mentions:
        if (member not in sslist):
            sslist.append(member)
            gifted.append(member)
            await ctx.send('{} enrolled in Secret Santa'.format(member))
        else:
            await ctx.send('{} already enrolled'.format(member))


@bot.command()
async def ss(ctx):
    if (len(names) < 3):
        await ctx.send("Insufficient Participants")
    else:
        for i in names:
            sslist = copy.copy(names)
            gifter = sslist.pop(sslist.index(i))
            giftee = random.choice(list(set(gifted)&set(sslist)))
            gifted.remove(giftee)
            await gifter.send('You are gifting {}'.format(giftee))




bot.run(TOKEN)