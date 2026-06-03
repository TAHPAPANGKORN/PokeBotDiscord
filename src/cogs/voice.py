import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import pytz

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash Command: /micmute
    @app_commands.command(name="micmute", description="Set time to mute microphone")
    async def muteTime(self, ctx: discord.Interaction, member: discord.Member, time: int, unit: str = 's'):  
        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}

        if unit not in units:
            await ctx.response.defer(ephemeral=True)
            await ctx.followup.send("Invalid unit! Please use 's' for seconds, 'm' for minutes, or 'h' for hours.", ephemeral=True)
            return
        
        await ctx.response.defer(ephemeral=True)
        targetTime = now + timedelta(**{units[unit]: time})

        if member.voice:
            try:
                await member.edit(mute=True)
                await ctx.followup.send(f"You mute {member.mention} until {targetTime.strftime('%H:%M:%S')} UTC+7", ephemeral=True)
                await discord.utils.sleep_until(targetTime)
                await member.edit(mute=False)
                await ctx.followup.send(f"Unmute! {member.mention}", ephemeral=True)
            except Exception as e:
                await ctx.followup.send(f"Error! {e}", ephemeral=True)
        else:
            await ctx.followup.send(f"{member.mention} not in a voice room", ephemeral=True)

    # Slash Command: /headphonemute
    @app_commands.command(name="headphonemute", description="Set time to mute headphone.")
    async def deafenTime(self, ctx: discord.Interaction, member: discord.Member, time: int, unit: str = 's'):  
        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}

        if unit not in units:
            await ctx.response.defer(ephemeral=True)
            await ctx.followup.send("Invalid unit! Please use 's' for seconds, 'm' for minutes, or 'h' for hours.", ephemeral=True)
            return
        
        await ctx.response.defer(ephemeral=True)
        targetTime = now + timedelta(**{units[unit]: time})

        if member.voice:
            try:
                await member.edit(deafen=True)
                await ctx.followup.send(f"You mute {member.mention} until {targetTime.strftime('%H:%M:%S')} UTC+7", ephemeral=True)
                await discord.utils.sleep_until(targetTime)
                await member.edit(deafen=False)
                await ctx.followup.send(f"Unmute! {member.mention}", ephemeral=True)
            except Exception as e:
                await ctx.followup.send(f"Error! {e}", ephemeral=True)
        else:
            await ctx.followup.send(f"{member.mention} not in a voice room", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Voice(bot))
