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
    @app_commands.choices(unit=[
        app_commands.Choice(name="Seconds", value="s"),
        app_commands.Choice(name="Minutes", value="m"),
        app_commands.Choice(name="Hours", value="h")
    ])
    async def micmute_command(self, interaction: discord.Interaction, member: discord.Member, duration: int, unit: str):  
        await interaction.response.defer(ephemeral=True)

        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}
        target_time = now + timedelta(**{units[unit]: duration})

        if not member.voice:
            await interaction.followup.send(f"{member.mention} is not in a voice channel.", ephemeral=True)
            return

        try:
            await member.edit(mute=True)
            await interaction.followup.send(
                f"You muted {member.mention} until {target_time.strftime('%H:%M:%S')} UTC+7", 
                ephemeral=True
            )
            
            await discord.utils.sleep_until(target_time)
            
            if member.voice:
                await member.edit(mute=False)
                await interaction.followup.send(f"Unmute! {member.mention}", ephemeral=True)
            else:
                await interaction.followup.send(f"{member.mention} left the voice channel, timer cleared.", ephemeral=True)

        except discord.HTTPException as e:
            await interaction.followup.send(f"Failed to edit member: {e.text}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occurred: {e}", ephemeral=True)

    # Slash Command: /headphonemute
    @app_commands.command(name="earmute", description="Set time to mute headphone.")
    @app_commands.choices(unit=[
        app_commands.Choice(name="Seconds", value="s"),
        app_commands.Choice(name="Minutes", value="m"),
        app_commands.Choice(name="Hours", value="h")
    ])
    async def earmute_command(self, interaction: discord.Interaction, member: discord.Member, duration: int, unit: str):  
        await interaction.response.defer(ephemeral=True)

        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}
        target_time = now + timedelta(**{units[unit]: duration})

        if not member.voice:
            await interaction.followup.send(f"{member.mention} is not in a voice channel.", ephemeral=True)
            return

        try:
            await member.edit(deafen=True)
            await interaction.followup.send(
                f"You earmuted {member.mention} until {target_time.strftime('%H:%M:%S')} UTC+7", 
                ephemeral=True
            )
            
            await discord.utils.sleep_until(target_time)
            
            if member.voice:
                await member.edit(deafen=False)
                await interaction.followup.send(f"Unearmute! {member.mention}", ephemeral=True)
            else:
                await interaction.followup.send(f"{member.mention} left the voice channel, timer cleared.", ephemeral=True)

        except discord.HTTPException as e:
            await interaction.followup.send(f"Failed to edit member: {e.text}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occurred: {e}", ephemeral=True)


    @app_commands.command(name="muteboth", description="Set time to deafen a member.")
    @app_commands.choices(unit=[
        app_commands.Choice(name="Seconds", value="s"),
        app_commands.Choice(name="Minutes", value="m"),
        app_commands.Choice(name="Hours", value="h")
    ])
    async def muteboth_command(self, interaction: discord.Interaction, member: discord.Member, duration: int, unit: str):
        await interaction.response.defer(ephemeral=True)

        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}
        target_time = now + timedelta(**{units[unit]: duration})

        if not member.voice:
            await interaction.followup.send(f"{member.mention} is not in a voice channel.", ephemeral=True)
            return

        try:
            await member.edit(deafen=True, mute=True)
            await interaction.followup.send(
                f"You deafened {member.mention} until {target_time.strftime('%H:%M:%S')} UTC+7", 
                ephemeral=True
            )
            
            await discord.utils.sleep_until(target_time)
            
            if member.voice:
                await member.edit(deafen=False, mute=False)
                await interaction.followup.send(f"Undeafen! {member.mention}", ephemeral=True)
            else:
                await interaction.followup.send(f"{member.mention} left the voice channel, timer cleared.", ephemeral=True)

        except discord.HTTPException as e:
            await interaction.followup.send(f"Failed to edit member: {e.text}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occurred: {e}", ephemeral=True)


    # mute choice
    @app_commands.command(name="mute", description="Mute or Deafen a member for a specific duration.")
    @app_commands.choices(action=[
        app_commands.Choice(name="Microphone Only (Mute)", value="mute"),
        app_commands.Choice(name="Headphones Only (Deafen)", value="deafen"),
        app_commands.Choice(name="Both (Mute & Deafen)", value="both")
    ])
    @app_commands.choices(unit=[
        app_commands.Choice(name="Seconds", value="s"),
        app_commands.Choice(name="Minutes", value="m"),
        app_commands.Choice(name="Hours", value="h")
    ])
    async def temp_mute_command(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member, 
        action: str, 
        duration: int, 
        unit: str
    ):
        await interaction.response.defer(ephemeral=True)

        if not member.voice:
            await interaction.followup.send(f"{member.mention} is not in a voice channel.", ephemeral=True)
            return

        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}
        target_time = now + timedelta(**{units[unit]: duration})

        is_mute = action in ['mute', 'both']
        is_deafen = action in ['deafen', 'both']
        
        action_text = "muted & deafened" if action == "both" else ("muted" if action == "mute" else "deafened")

        try:
            await member.edit(mute=is_mute, deafen=is_deafen)
            await interaction.followup.send(
                f"You {action_text} {member.mention} until {target_time.strftime('%H:%M:%S')} UTC+7", 
                ephemeral=True
            )

            await discord.utils.sleep_until(target_time)

            if member.voice:
                await member.edit(mute=False, deafen=False)
                await interaction.followup.send(f"Un{action_text} {member.mention}", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"Error! {e}", ephemeral=True)

    # unmute choice
    @app_commands.command(name="unmute", description="Unmute or Undeafen a member immediately.")
    @app_commands.choices(action=[
        app_commands.Choice(name="Microphone Only (Unmute)", value="unmute"),
        app_commands.Choice(name="Headphones Only (Undeafen)", value="undeafen"),
        app_commands.Choice(name="Both (Unmute & Undeafen)", value="both")
    ])
    async def unmute_command(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member, 
        action: str = "both"
    ):
        await interaction.response.defer(ephemeral=True)

        if not member.voice:
            await interaction.followup.send(f"{member.mention} is not in a voice channel.", ephemeral=True)
            return

        is_unmute = action in ['unmute', 'both']
        is_undeafen = action in ['undeafen', 'both']
        
        action_text = "unmuted & undeafened" if action == "both" else ("unmuted" if action == "unmute" else "undeafened")

        try:
            # Prepare the edit parameters dynamically based on what is being unmuted
            kwargs = {}
            if is_unmute:
                kwargs['mute'] = False
            if is_undeafen:
                kwargs['deafen'] = False

            await member.edit(**kwargs)
            await interaction.followup.send(
                f"Successfully {action_text} {member.mention}.", 
                ephemeral=True
            )

        except discord.HTTPException as e:
            await interaction.followup.send(f"Failed to edit member: {e.text}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Error! {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Voice(bot))
