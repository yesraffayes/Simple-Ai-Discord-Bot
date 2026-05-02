import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os
from chatbot import chat, clear_history

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"pip install discord.py groq python-dotenv Bot online: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        content = message.content.replace(f"<@{bot.user.id}>", "").strip()

        if not content:
            await message.reply("Hei! Ada yang bisa gw bantu? ")
            return
        
        async with message.channel.typing():
            reply = chat(message.author.id, content)

        await message.reply(reply)

    await bot.process_commands(message)

@bot.command(name="clear")
async def clear(ctx):
    clear_history(ctx.author.id)
    await ctx.send(" History chat sudah di reset!")

@bot.command(name="hi")
async def hi(ctx):
    await ctx.send(f"Bot on, Ada yang bisa di bantu?")
    await ctx.send(f"gunakan !list untuk melihat list command")
    await ctx.send(f"ping + pertanyaan jika ingin menggunakan fitur ai")

@bot.command(name="model")
async def model(ctx):
    await ctx.send(f"model yang di gunakan adalah llama-3.1-8b-instant")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"NI PING GW TOLOL `{round(bot.latency * 1000)}ms`")

@bot.command(name="creator")
async def creator(ctx):
    await ctx.send(f"Pembuat gw sekaligus babu gw yang tolol ini adalah <@your discord id>!")

@bot.command(name="list")
async def list(ctx):
    embed = discord.Embed(
        title="List Command!",
        color=discord.Color(0xFFC0CB)
    )
    
    embed.add_field(name="!clear", value="Untuk mereset history chat", inline=False)
    embed.add_field(name="!hi", value="Untuk test bot nyala atau tidak", inline=False)
    embed.add_field(name="!model", value="Untuk mengetahui model AI yang digunakan", inline=False)
    embed.add_field(name="!ping", value="Untuk mengetahui ping latency dari bot", inline=False)
    embed.add_field(name="!list", value="Untuk mengetahui list command", inline=False)
    embed.add_field(name="!creator", value="Pencipta bot tolol nan idiot ini", inline=False)
    
    await ctx.send(embed=embed)


bot.run(os.getenv("DISCORD_TOKEN"))
