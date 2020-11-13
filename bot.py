# bot.py
import os
import random
import copy
import discord
from discord.ext import commands
from dotenv import load_dotenv
import utility
import database
from SecretSanta import SecretSanta

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
chans = os.getenv('CHANNELS')

bot = commands.Bot(command_prefix='!')

SS = SecretSanta()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


#PUTS PEOPLE INTO SECRET SANTA LIST
@bot.command()
async def enroll(ctx):
    if (str(ctx.channel) in chans):
        SS.addPerson(ctx.message.mentions)
        await ctx.send('{} enrolled in Secret Santa'.format([person.display_name for person in ctx.message.mentions]))

@bot.command()
async def previous(ctx):
    if (str(ctx.channel) in chans):
        if len(ctx.message.mentions) == 2:
            SS.updatePrevious(ctx.message.mentions[0], ctx.message.mentions[1])
            await ctx.message.add_reaction('👍')



#lists those enrolled in secret santa
@bot.command()
async def ssp(ctx):
    if (str(ctx.channel) in chans):
        await ctx.send('{}'.format(SS.names))

#SECRET SANTA PAIRINGs SENT VIA DMs
@bot.command()
async def pair(ctx):
    SS.pair()

@bot.command()
async def ss(ctx):
    if SS.success:
        for gifter, giftee in SS.gifting_map.items():
                await gifter.disc.send("You are gifting: {}".format(str(giftee)))

@bot.command()
async def save(ctx):
    if SS.success:
        SS.save()
        await ctx.message.add_reaction('👍')

@bot.command()
async def meet(ctx, date, person, location):
    meetup = discord.Embed(
        title = "react to rsvp",
        description=":regional_indicator_y: for Coming :question: For Maybe :regional_indicator_n: for No",
        colour = discord.Color.dark_gold()
    )

    meetup.set_author(name="Meet Up on: {} at {} {}".format(date, person, location))
    invited = ctx.message.mentions
    invited.append(ctx.author)
    for chan in ctx.guild.channels:
        if (str(chan) == 'schedule'):
            await chan.send(embed=meetup)
            z = utility.list2string(ctx.message.mentions)
            await chan.send("{}".format(z))

bot.run(TOKEN)