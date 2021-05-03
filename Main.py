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

guild_ids = [781590063653191701, 456602312920530945] 
myID = [216387516419407872, 485111576513347585]


def is_user(ctx):
    return not ctx.author.id == myID

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1
    print(f"{bot.user.name} is in {str(guild_count)} servers.")
    print(f"{bot.user.name}\'s id is {bot.user.id}")

@bot.command(name="stop")
async def stop(ctx):
    if ctx.author.id in myID:
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
            if char.isalpha():
                if (char.isupper()):
                    result += chr((ord(char) + shift-65) % 26 + 65)
                # Encrypt lowercase characters
                else:
                    result += chr((ord(char) + shift - 97) % 26 + 97)
            else:
                result += char
        await ctx.send(f"{str(shift)}: {result}")


@slash.slash(name="decode",
             description="Decode a message that uses the ceaser cipher",
             guild_ids=guild_ids
             )
async def _decode(ctx, msg, shift = 0):
    result = ""
    shift = int(shift)
    if shift == 0:
        await ctx.send("Running brute force...")
        # TODO: Put working brute force here
        s = ["this", "this", "and", "that"]
        for i in range(1, len(s)):
            if s[i] == s[i-1]:
                print (s[i])
    elif shift < 0:
        await ctx.send("Shift must be a positive integer")
    else:
        for i in range(len(msg)):
            char = msg[i]
            # Encrypt uppercase characters
            if char.isalpha():
                if (char.isupper()):
                    result += chr((ord(char) - shift-65) % 26 + 65)
                # Encrypt lowercase characters
                else:
                    result += chr((ord(char) - shift - 97) % 26 + 97)
            else:
                result += char
        await ctx.send(f"{result}")



# TODO: Currently not working, you need to fix that for this crucial function of the bot
# @slash.slash(name='fart',
# description='we do a little farting', guild_ids=guild_ids)
# async def _fart(ctx):
    await ctx.send("Currently under development")
    audio_source = discord.FFmpegPCMAudio(
        'zapsplat_human_wet_short_bold_fart_54644.mp3',
        executable='C:/Program Files (x86)/FFmpeg for Audacity/ffmpeg.exe')

    connected = ctx.author.voice
    if connected:
        # Use the channel instance you put into a variable
        vc = await connected.channel.connect()
        vc.play(audio_source)
        vc.cleanup()
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('Get in a vc, then we\'ll talk')

@bot.command(name="mention")
async def mention(ctx):
    moderator = discord.utils.get(ctx.guild.roles, id='@&817066832300998666')
    await ctx.send(f'Hello {moderator.mention}')


bot.run(TOKEN)
