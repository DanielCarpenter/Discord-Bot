# bot.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

sslist = []
giftee = ['nobody']
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def ssenroll(ctx):
    for i in sslist:
        if(i == ctx.author):
            await ctx.send("{} already enrolled".format(ctx.author))
            return
    sslist.append(ctx.author)
    giftee.append(ctx.author)
    await ctx.send('{} enrolled in Secret Santa'.format(ctx.author))

@bot.command()
async def ss(ctx):
    if len(sslist) < 4:
        await ctx.author.send("Insufficient Participants")
    else:
        seed = random.seed()
        while len(sslist) and len(giftee):
            gifter = random.randint(0,len(sslist))
            gifte = gifter
            while gifte == gifter:
                gifte = random.randint(0,len(sslist))
            await sslist.pop(gifter).send('You are gifting {}'.format(giftee.pop(gifte)))




bot.run(TOKEN)