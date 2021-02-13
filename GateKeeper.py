#################################################
# Program:  GateKeeper
# Version:  0.3.1
# Version Date:  02/13/2021
# Author:  Kevin Wilkins
# Date:  11/14/2020
# Contributor(s):  Donlon McGovern
# Parameters:
# When a new member to a Discord agrees to the rules of a server using
#  the associated emoji, they will receive the 'member' role.
# Console output will display the role and the username it is assigned to
#################################################

#################################################
# Import dependencies
#################################################
import os
import discord
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

#################################################
# Pull Discord token, guild, channel, and message
# IDs from .env file
#################################################
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
MESSAGE = int(os.getenv("MESSAGE_ID"))
CHANNEL = int(os.getenv("CHANNEL_ID"))


#################################################
# Test and confirm bot has connected to Discord
#################################################
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            print(
                f"{client.user} has connected to Discord!\n\n"
                f"{client.user} is connected to the following guild(s):\n"
                f"{guild.name} (id: {guild.id})\n"
            )
            break


#################################################
# When member selects Sweet Justice they will be
# given the 'member' role.  The 'member' role
# cannot be removed unless done by the admins.
#################################################
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == MESSAGE:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'SweetJustice':
            role = discord.utils.get(guild.roles, name='Member')
            print(f"{role} selected")
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = payload.member
            await member.add_roles(role)
            print(f"{role} assigned to {member}\n")
        else:
            print("No role assigned.")


client.run(TOKEN)
