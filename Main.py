import discord
import os
import sys
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

guild_ids = [781590063653191701] 
myID = 216387516419407872


def is_user(ctx):
    return not ctx.author.id == myID

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1
    print("MUL-T is in " + str(guild_count) + " servers.")

@bot.command(name="stop")
async def stop(ctx):
    if ctx.author.id == myID:
        await ctx.send("Killing bot")
        sys.exit()
    else:
        await ctx.send("Nope")


@slash.slash(name="wide", description="makes text w i d e", guild_ids=guild_ids)
async def _wide(ctx, word):
    j = ' '
    await ctx.send(j.join(word))
    print(f"printed \"{j.join(word)}\"")


@slash.slash(name="ping", guild_ids=guild_ids)
async def _ping(ctx):
    await ctx.send(f"Pong! ({round(bot.latency*1000)}ms)")


@slash.slash(name="encode",
             description="Use a ceaser cipher to encode a message",
             guild_ids=guild_ids,
             )
async def _encode(ctx, msg, shift):
    result = ""
    shift = int(shift)
    # traverse text
    if shift < 0:
        await ctx.send("Shift must be a postive integer!")
    else:
        for i in range(len(msg)):
            char = msg[i]
            # Encrypt uppercase characters
            if (char.isupper()):
                result += chr((ord(char) + shift-65) % 26 + 65)
            # Encrypt lowercase characters
            else:
                result += chr((ord(char) + shift - 97) % 26 + 97)
        await ctx.send(f"{str(shift)}: {result}")


@slash.slash(name="decode",
             description="Decode a message that uses the ceaser cipher",
             guild_ids=guild_ids,
             )
async def _decode(ctx, msg, shift = 0):
    result = ""
    shift = int(shift)
    if shift == 0:
        await ctx.send("Running brute force...")
        # TODO: Put working brute force here
    elif shift < 0:
        await ctx.send("Shift must be a positive integer")
    else:
        for i in range(len(msg)):
            char = msg[i]
            # Encrypt uppercase characters
            if (char.isupper()):
                result += chr((ord(char) - shift-65) % 26 + 65)
            # Encrypt lowercase characters
            else:
                result += chr((ord(char) - shift - 97) % 26 + 97)
        await ctx.send(f"{result}")

bot.run(TOKEN)
