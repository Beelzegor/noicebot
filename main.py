from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
from database.db import obtener_sorteos_activos
import asyncio
import datetime
from datetime import timezone

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


class NoiceBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.moderacion")
        await self.load_extension("cogs.experiencia")
        await self.load_extension("cogs.sorteos")
        await self.load_extension("cogs.misc")
        

bot = NoiceBot(command_prefix="!", intents=intents)

@bot.event
async def on_command_error(ctx, error):
    print(error)


bot.remove_command("help")

@bot.event
async def on_ready():
    print('Ready!')
    sorteos = obtener_sorteos_activos()
    asyncio.create_task(status_task())



    for sorteo in sorteos:
        tiempo_restante = (sorteo[6].replace(tzinfo=timezone.utc) - datetime.datetime.now(timezone.utc)).total_seconds()
        if tiempo_restante > 0:
            canal = bot.get_channel(int(sorteo[2]))
            mensaje = await canal.fetch_message(int(sorteo[3]))
            asyncio.create_task(bot.cogs["Sorteos"].finalizar_sorteo(mensaje, sorteo[5], tiempo_restante, sorteo[4], sorteo[0]))

async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name="¡Usa !help para ver mis comandos!"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servidores"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} usuarios"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Creado por beelzegor"))

if __name__ == "__main__":
    bot.run(token)
