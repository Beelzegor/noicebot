import random
import time
import discord
from database.db import actualizar_xp, get_connection
from discord.ext import commands


class Experiencia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.cooldowns = {}
    xp_range = (15, 25)
    nivel_formula = lambda self, nivel: 5 * (nivel ** 2) + 40 * nivel + 100
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id in self.cooldowns and time.time() - self.cooldowns[message.author.id] < 60:
            return
        xp_obtenida = random.randint(*self.xp_range)
        self.cooldowns[message.author.id] = time.time()
        usuario_id = str(message.author.id)
          #  puedes quitar el # para mostrar un mensaje cada que se suba de nivel, por fines de estética lo dejé asi
          # await message.channel.send(f"{message.author.mention} has ganado {xp_obtenida} XP por enviar un mensaje.")
        if actualizar_xp(usuario_id, str(message.guild.id), xp_obtenida):
            await message.channel.send(f"¡Felicidades {message.author.mention}, has subido de nivel!")

    @commands.command(aliases=["level", "rank"], usage="!nivel [miembro]")
    async def nivel(self, ctx, miembro: commands.MemberConverter = None):
        """Muestra el nivel y XP de un miembro. Si no se menciona a ningún miembro, muestra tu propio nivel."""
        if miembro is None:
            miembro = ctx.author
        
        usuario_id = str(miembro.id)
        guild_id = str(ctx.guild.id)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT xp, nivel FROM experiencia WHERE user_id = %s AND guild_id = %s", (usuario_id, guild_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            xp_actual, nivel_actual = result
            xp_para_siguiente_nivel = self.nivel_formula(nivel_actual) - xp_actual
            embed = discord.Embed(title=f"Nivel de {miembro.display_name}", color=discord.Color.blue())
            embed.add_field(name="Nivel", value=str(nivel_actual), inline=False)
            embed.add_field(name="XP", value=f"{xp_actual} / {self.nivel_formula(nivel_actual)}", inline=False)
            embed.add_field(name="XP para el siguiente nivel", value=str(xp_para_siguiente_nivel), inline=False)
            embed.set_thumbnail(url=miembro.display_avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{miembro.mention} no tiene experiencia aún.")
    
    @commands.command(aliases=["lb"], usage="!leaderboard")
    async def leaderboard(self, ctx):
        """Muestra el leaderboard de experiencia del servidor."""
        guild_id = str(ctx.guild.id)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, xp, nivel FROM experiencia WHERE guild_id = %s ORDER BY nivel DESC, xp DESC LIMIT 10", (guild_id,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

        embed = discord.Embed(title=f"Leaderboard de {ctx.guild.name}", color=discord.Color.gold())
        for i, (user_id, xp, nivel) in enumerate(resultados, start=1):
            usuario = await self.bot.fetch_user(int(user_id))
            embed.add_field(name=f"{i}. {usuario.display_name}", value=f"Nivel: {nivel} | XP: {xp}", inline=False)
            embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        await ctx.send(embed=embed)
            


async def setup(bot):
    await bot.add_cog(Experiencia(bot))