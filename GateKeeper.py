# GateKeeper 0.2.1

# This bot will auto assign roles when a user reacts to a message with an emoji
# When a member joins the bot will send a message welcoming the new member
# Console output will display the role and the username it is assigned to

import os
import discord
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
MESSAGE = int(os.getenv("MESSAGE_ID"))
CHANNEL = int(os.getenv("CHANNEL_ID"))


# Check to make sure bot has connected to the server
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


# Send user a message when the join to agree to the rules
@client.event
async def on_member_join(member):
    channel = client.get_channel(CHANNEL)
    await channel.send(f'Hello {member}, please proceed to #customs and agree to the rules.')
    print(f'{member} joined the server\n')
    print(f'Welcome message sent to {member}. . .\n')


# Add role by selecting emoji
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
