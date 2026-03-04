import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ayuda"], usage="!help [comando]")
    async def help(self, ctx, comando: str = None):
        """Muestra una lista de comandos disponibles o información detallada sobre un comando específico."""
        if comando is None:

            embed = discord.Embed(title="Comandos de NoiceBot", description="Aquí tienes una lista de mis comandos disponibles:", color=discord.Color.blue())
            #comandos organizados por categorias
            embed.add_field(name="Moderación", value="`!kick`, `!ban`, `!clear`, `!mute`, `!tempban`, `!tempmute`", inline=False)
            embed.add_field(name="Experiencia", value="`!nivel`, `!leaderboard`", inline=False)
            embed.add_field(name="Sorteos", value="`!sorteo`", inline=False)
            embed.add_field(name="Misceláneo", value="`!ping`, `!status`, `!invite`, `!avatar`, `!serverinfo`, `!userinfo`, `!say`", inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text="Creado por beelzegor")
            await ctx.send(embed=embed)
        else:
            if self.bot.get_command(comando) is None:
                await ctx.send(f"No se encontró el comando `{comando}`. Usa `!help` para ver la lista de comandos.")
            else:
                comando_obj = self.bot.get_command(comando)
                embed = discord.Embed(title=f"Comando: {comando_obj.name}", description=comando_obj.help or "No hay descripción disponible.", color=discord.Color.green())
                embed.add_field(name="Uso", value=f"`{comando_obj.usage}`" if comando_obj.usage else "No hay información de uso disponible.", inline=False)
                embed.add_field(name="Alias", value=", ".join(comando_obj.aliases) if comando_obj.aliases else "No hay alias disponibles.", inline=False)
                await ctx.send(embed=embed)
        
            

    @commands.command(aliases=["latencia"], usage="!ping")
    async def ping(self, ctx):
        """Muestra la latencia del bot."""
        
        await ctx.send("Pong!" + f" Latencia: {round(self.bot.latency * 1000)}ms")

    @commands.command(aliases=["estado"], usage="!status")
    async def status(self, ctx):
        """Muestra información detallada sobre el estado del bot."""
        embed = discord.Embed(title="Estado de NoiceBot", description="¡NoiceBot está funcionando correctamente! Aquí tienes algunos detalles:", color=discord.Color.green())
        embed.add_field(name="Latencia", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.add_field(name="Número de servidores", value=str(len(self.bot.guilds)), inline=False)
        embed.add_field(name="Número de usuarios", value=str(sum(guild.member_count for guild in self.bot.guilds)), inline=False)
        embed.add_field(name="Número de comandos", value=str(len(self.bot.commands)), inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Creado por beelzegor")
        await ctx.send(embed=embed)

    @commands.command(aliases=["invitar", "invitacion"], usage="!invite")
    async def invite(self, ctx):
        """Proporciona un enlace de invitación para agregar NoiceBot a otros servidores."""
        invitacion = "https://discord.com/api/oauth2/authorize?client_id=1059162235747975208&permissions=0&scope=bot"
        embed = discord.Embed(title="Invitación de NoiceBot", description="¡Invita a NoiceBot a tu servidor para disfrutar de todas sus funciones!", color=discord.Color.blue())
        embed.add_field(name="Enlace de invitación", value=f"[Haz clic aquí]({invitacion})", inline=False)
        await ctx.send(embed=embed)

    @commands.command(usage="!avatar [miembro]")
    async def avatar(self, ctx, miembro: discord.Member = None):
        """Muestra el avatar de un miembro. Si no se menciona a ningún miembro, muestra tu propio avatar."""
        if miembro is None:
            miembro = ctx.author

        embed = discord.Embed(title=f"Avatar de {miembro.display_name}", color=discord.Color.blue())
        embed.set_image(url=miembro.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["infoserver", "servidor"], usage="!serverinfo")
    async def serverinfo(self, ctx):
        """Muestra información detallada sobre el servidor."""
        guild = ctx.guild
        embed = discord.Embed(title=f"Información del servidor: {guild.name}", color=discord.Color.green())
        embed.add_field(name="ID del servidor", value=guild.id, inline=False)
        embed.add_field(name="Dueño del servidor", value=str(await self.bot.fetch_user(guild.owner_id)), inline=False)        
        embed.add_field(name="Número de miembros", value=guild.member_count, inline=False)
        embed.add_field(name="Número de bots", value=len([member for member in guild.members if member.bot]), inline=False)
        embed.add_field(name="Número de canales", value=len(guild.channels), inline=False)
        embed.add_field(name="Número de roles", value=len(guild.roles), inline=False)
        embed.add_field(name="Fecha de creación", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Nivel de verificación", value=str(guild.verification_level), inline=False)
        embed.add_field(name="Emojis personalizados", value=str(len(guild.emojis)), inline=False)
        embed.add_field(name="Boosts del servidor", value=str(guild.premium_subscription_count), inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["info", "infousuario"], usage="!userinfo [miembro]")
    async def userinfo(self, ctx, miembro: discord.Member = None):
        """Muestra información detallada sobre un miembro del servidor. Si no se menciona a ningún miembro, muestra tu propia información."""
        if miembro is None:
            miembro = ctx.author

        embed = discord.Embed(title=f"Información de usuario: {miembro.display_name}", color=discord.Color.purple())
        embed.add_field(name="ID del usuario", value=miembro.id, inline=False)
        embed.add_field(name="Nombre de usuario", value=miembro.name, inline=False)
        embed.add_field(name="Es admininistrador", value=str(miembro.guild_permissions.administrator), inline=False)
        embed.add_field(name="Fecha de unión", value=miembro.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Creacion de la cuenta", value=miembro.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Roles", value=", ".join([role.name for role in miembro.roles if role.name != "@everyone"]), inline=False)
        embed.set_thumbnail(url=miembro.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["decir"], usage="!say <mensaje>")
    async def say(self, ctx, *, mensaje):
        """Repite el mensaje que el usuario ingrese después del comando."""
        await ctx.send(mensaje)



async def setup(bot):
    await bot.add_cog(Misc(bot))