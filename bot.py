# bot.py
import os
import random
import copy
import discord
from discord.ext import commands
from dotenv import load_dotenv
import utility
import database

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
channels = os.getenv('CHANNELS')

bot = commands.Bot(command_prefix='!')

sslist = []
names = sslist
gifted = []
enrolled = []
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


#PUTS PEOPLE INTO SECRET SANTA LIST
@bot.command()
async def enroll(ctx):
    if (str(ctx.channel) in channels):
        if ctx.author not in sslist:
            sslist.append(ctx.author)
            gifted.append(ctx.author)
            enrolled.append(str(ctx.author))
            await ctx.send('{} enrolled in Secret Santa'.format(ctx.author))
        for member in ctx.message.mentions:
            if (member not in sslist):
                sslist.append(member)
                gifted.append(member)
                enrolled.append(str(member))
                await ctx.send('{} enrolled in Secret Santa'.format(member))
            else:
                await ctx.send('{} already enrolled'.format(member))

#lists those enrolled in secret santa
@bot.command()
async def ssp(ctx):
    if (str(ctx.channel) in channels):
        await ctx.send('{}'.format(enrolled))

#SECRET SANTA PAIRINGs SENT VIA DMs
@bot.command()
async def ss(ctx):
    if (str(ctx.channel) in channels):
        if (len(names) < 3):
            await ctx.send("Insufficient Participants")
        else:
            for i in names:
                sslist = copy.copy(names)
                gifter = sslist.pop(sslist.index(i))
                giftee = random.choice(list(set(gifted)&set(sslist)))
                gifted.remove(giftee)
                await gifter.send('You are gifting {}'.format(giftee))

@bot.command()
async def meet(ctx):
    invited = ctx.message.mentions
    invited.append(ctx.author)
    


bot.run(TOKEN)