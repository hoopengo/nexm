import os

import nextcord
from nexm import Market
from nextcord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = nextcord.Intents.default()

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"{TOKEN=}")


@bot.slash_command(name="test", description="понг!")
async def ping(interaction: nextcord.Interaction):
    """Отвечает pong!"""
    store = Market(interaction)

    await interaction.send(str(store.get("_id")))


bot.run(TOKEN)
