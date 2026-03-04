from discord.ext import commands
import discord
import asyncio
import random
from database.db import guardar_sorteo, finalizar_sorteo_db, obtener_sorteos_activos
from datetime import datetime, timedelta, timezone

class Sorteos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="!sorteo <duracion> <ganadores> <premio>")
    async def sorteo(self, ctx, duracion = None, ganadores: int = 1, *, premio):
        """Inicia un sorteo con una duración, número de ganadores y premio especificados."""
        if duracion is not None:
            duracion = self.parsear_duracion(duracion)
            if duracion is None:
                message = await ctx.send("Duración inválida. Usa el formato `!sorteo <duracion> <ganadores> <premio>` (ejemplo: `!sorteo 1h 3 Tarjeta de regalo`).")
                await message.delete(delay=10)
                return
        else:
            message = await ctx.send("Duración no especificada. Usa el formato `!sorteo <duracion> <ganadores> <premio>` (ejemplo: `!sorteo 1h 3 Tarjeta de regalo`).")
            await message.delete(delay=10)
            return
        
        embed = discord.Embed(
            title="🎉 Sorteo",
            description=f"Sorteo de {premio}",
            color=0x00ff00
        )
        embed.add_field(name="Premio", value=premio)
        embed.add_field(name="Ganadores", value=ganadores)
        embed.add_field(name="Termina en", value=duracion)
        embed.set_footer(text=f"Sorteo iniciado por {ctx.author.display_name}")
        
        mensaje = await ctx.send(embed=embed)
        await mensaje.add_reaction("🎉")

        termina_en = datetime.now(timezone.utc) + timedelta(seconds=duracion)
        sorteo_id = guardar_sorteo(
            guild_id=ctx.guild.id,
            channel_id=ctx.channel.id,
            message_id=mensaje.id,
            premio=premio,
            ganadores=ganadores,
            termina_en=termina_en
        )
        asyncio.create_task(self.finalizar_sorteo(mensaje, ganadores, duracion, premio, sorteo_id))

    def parsear_duracion(self, duracion):
        unidades = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400
        }
        try:
            cantidad = int(duracion[:-1])
            unidad = duracion[-1]
            if unidad in unidades:
                return cantidad * unidades[unidad]
        except ValueError:
            pass
        return None

    async def finalizar_sorteo(self, mensaje, num_ganadores, segundos, premio, sorteo_id):
        await asyncio.sleep(segundos)
        mensaje = await mensaje.channel.fetch_message(mensaje.id)
        reacciones = mensaje.reactions
        participantes = []
        for reaction in reacciones:
            if reaction.emoji == "🎉":
                async for user in reaction.users():
                    if not user.bot:
                        participantes.append(user)

        if len(participantes) == 0:
            await mensaje.channel.send("No hay participantes en el sorteo.")
            finalizar_sorteo_db(sorteo_id)
            return

        ganadores = random.sample(participantes, min(num_ganadores, len(participantes)))
        ganadores_nombres = ", ".join([g.mention for g in ganadores])
        await mensaje.channel.send(f"🎉 ¡Felicidades {ganadores_nombres}! Ganaron **{premio}**.")
        finalizar_sorteo_db(sorteo_id)
    


async def setup(bot):
    await bot.add_cog(Sorteos(bot))