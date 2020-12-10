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
from SecretSantaManager import SecretSantaManager
from Person import Person

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
chans = os.getenv('CHANNELS')

bot = commands.Bot(command_prefix='!')

SS = SecretSantaManager()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


#PUTS PEOPLE INTO SECRET SANTA LIST
@bot.command()
async def enroll(ctx):
    if (str(ctx.channel) in chans):
        SS.get_ss_instance(ctx.guild.id).addPerson(ctx.message.mentions)
        await ctx.send('{} enrolled in Secret Santa'.format([person.display_name for person in ctx.message.mentions]))

@bot.command()
async def previous(ctx):
    if (str(ctx.channel) in chans):
        if len(ctx.message.mentions) == 2:
            SS.get_ss_instance(ctx.guild.id).updatePrevious(ctx.message.mentions[0], ctx.message.mentions[1])
            await ctx.message.add_reaction('👍')


@bot.command()
async def ssload(ctx):
    instance = SS.get_ss_instance(ctx.guild.id)
    current_year_map, current_year_name = SS.get_ss_instance(ctx.guild.id).load(ctx.guild.id)
    if current_year_map and current_year_name:
        for (gifter, giftee), (gifter_name, giftee_name) in zip(current_year_map.items(), current_year_name.items()):
            pgifter = Person(int(gifter), gifter_name)
            pgiftee = Person(int(giftee), giftee_name)
            instance.gifting_map[pgifter] = pgiftee
            instance.names.append(pgifter)
        new_sent = []
        for num in instance.sent:
            new_sent.append(instance.names[instance.names.index(num)])
        instance.sent = new_sent
        await ctx.message.add_reaction('👍')

@bot.command()
async def notify(ctx, display_name):
    instance = SS.get_ss_by_display_name(ctx.author, display_name)
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


#lists those enrolled in secret santa
@bot.command()
async def ssp(ctx):
    if (str(ctx.channel) in chans):
        await ctx.send('{}'.format(SS.get_ss_instance(ctx.guild.id).names))

#SECRET SANTA PAIRINGs SENT VIA DMs
@bot.command()
async def pair(ctx):
    SS.get_ss_instance(ctx.guild.id).pair()

@bot.command()
async def ss(ctx):
    if SS.get_ss_instance(ctx.guild.id).success:
        for gifter, giftee in SS.get_ss_instance(ctx.guild.id).gifting_map.items():
                await gifter.disc.send("You are gifting: {}".format(str(giftee)))

@bot.command()
async def save(ctx):
    if SS.get_ss_instance(ctx.guild.id).success:
        SS.get_ss_instance(ctx.guild.id).save()
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