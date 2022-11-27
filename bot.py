# bot.py
import os
import random
import copy
import discord
from discord.ext import commands
from dotenv import load_dotenv
import utility
from SecretSanta import *
from SecretSantaManager import SecretSantaManager
from Person import Person

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

SS = SecretSantaManager()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


#PUTS PEOPLE INTO SECRET SANTA LIST
@bot.command()
async def enroll(ctx, group_name):
    SS.enroll(group_name, ctx.message.mentions)
    await ctx.message.add_reaction('👍')

@bot.command()
async def previous(ctx, group_name):
        SS.setPrevious(group_name, ctx.message.mentions[0], ctx.message.mentions[1:len(ctx.message.mentions)])
        await ctx.message.add_reaction('👍')


@bot.command()
async def load(ctx, group_name):
    SS.load_previous_pairings_history(group_name)
    await ctx.message.add_reaction('👍')

@bot.command()
async def notify(ctx, group_name):
    instance = SS.get_ss_instance(group_name)
    if instance:
        giftee = instance.gifting_map.get(instance.names[instance.names.index(ctx.author.id)])
        if giftee:
            #await giftee.send("Your {} Secret Santa gift has been sent.".format())
            instance.updateSent(giftee)
            guild = bot.get_guild(instance.guild)
            if guild:
                for chan in guild.text_channels:
                    if "address" in chan.name or "secret-santa" in chan.name:
                        await chan.send("{}/{} gifts sent/bought. dm me !notify [display name of recipient] to update".format(len(instance.sent),len(instance.gifting_map)))


#match people in the secret santa group
@bot.command()
async def match(ctx, group_name):
    if SS.matching(group_name):
        await ctx.message.add_reaction('👍')
    else:
        await ctx.message.add_reaction('👎')

#SECRET SANTA PAIRINGs SENT VIA DMs
@bot.command()
async def ssdm(ctx, group_name):
    if SS.get_ss_instance(group_name).success:
        for gifter_id, giftee_id in SS.get_ss_instance(group_name).gifting_map.items():
                gifter = bot.get_user(gifter_id)
                giftee = bot.get_user(giftee_id)
                await gifter.send("You are gifting: {}".format(str(giftee.display_name)))
        await ctx.message.add_reaction('👍')
    else:
        await ctx.message.add_reaction('👎')

bot.run(TOKEN)
