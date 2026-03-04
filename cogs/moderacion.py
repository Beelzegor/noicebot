from discord.ext import commands
import discord
import asyncio

class Moderacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _ejecutar_unmute(self, miembro, duracion, ctx):
        await asyncio.sleep(duracion)

        role = discord.utils.get(miembro.guild.roles, name="Muted")

        try:
            await miembro.remove_roles(role)
            await ctx.send(f"{miembro.display_name} ha sido desmuteado.")
        except:
            pass


    async def _ejecutar_unban(self, guild, miembro, duracion, ctx):
        await asyncio.sleep(duracion)
        try:
            await guild.unban(miembro)
            await ctx.send(f"{miembro.display_name} ha sido desbaneado.")
        except:
            pass

    @commands.command(usage="!kick <miembro> [razón]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, miembro: discord.Member, *, razon="Sin razón especificada"):
        """Expulsa a un miembro del servidor."""
        await miembro.kick(reason=razon)
        await ctx.send(f"{miembro.display_name} ha sido expulsado. Razón: {razon}")

    @commands.command(usage="!ban <miembro> [razón]")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, miembro: discord.Member, *, razon="Sin razón especificada"):
        """Banea a un miembro del servidor."""
        await miembro.ban(reason=razon)
        await ctx.send(f"{miembro.display_name} ha sido baneado. Razón: {razon}")

    @commands.command(aliases=["purge"], usage="!clear <cantidad>")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, cantidad: int):
        """Elimina una cantidad específica de mensajes en el canal."""
        await ctx.channel.purge(limit=cantidad + 1)
        await ctx.send(f"{cantidad} mensajes han sido eliminados.", delete_after=5)


    @commands.command(usage="!mute <miembro>")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, miembro: discord.Member):
        """Silencia a un miembro del servidor."""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            for canal in ctx.guild.channels:
                await canal.set_permissions(role, send_messages=False, speak=False)
        
        await miembro.add_roles(role)
        await ctx.send(f"{miembro.display_name} ha sido silenciado.")


    @commands.command(usage="!unmute <miembro>")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, miembro: discord.Member):
        """Desmutea a un miembro del servidor."""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role in miembro.roles:
            await miembro.remove_roles(role)
            await ctx.send(f"{miembro.display_name} ha sido desmuteado.")
        else:
            await ctx.send(f"{miembro.display_name} no está silenciado.")
    
    @commands.command(usage="!tempban <miembro> <duracion> [razón]")
    @commands.has_permissions(manage_messages=True)
    async def tempban(self, ctx, miembro: discord.Member, duracion: int,
                          *, razon="Sin razón especificada"):
          """Banea temporalmente a un miembro del servidor."""
          await miembro.ban(reason=razon)
          await ctx.send(f"{miembro.display_name} ha sido baneado por {duracion} segundos. Razón: {razon}")
          
          asyncio.create_task(self._ejecutar_unban(ctx.guild, miembro, duracion, ctx))

    
    @commands.command(usage="!tempmute <miembro> <duracion> [razón]")
    @commands.has_permissions(manage_messages=True)
    async def tempmute(self, ctx, miembro: discord.Member, duracion: int,
                    *, razon="Sin razón especificada"):
        """Silencia temporalmente a un miembro del servidor."""

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            for canal in ctx.guild.channels:
                await canal.set_permissions(role, send_messages=False, speak=False)

        await miembro.add_roles(role)
        await ctx.send(f"{miembro.display_name} ha sido silenciado por {duracion} segundos. Razón: {razon}")

        asyncio.create_task(self._ejecutar_unmute(miembro, duracion, ctx))
        


async def setup(bot):
    await bot.add_cog(Moderacion(bot))