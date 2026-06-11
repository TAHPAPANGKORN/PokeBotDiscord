import discord
from discord.ext import commands
from discord import app_commands, Forbidden
import discord.utils
import asyncio
class Poke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stopLoop = None
        self.nameMember = None
        self.userStop = None
        self.active_member = None

        self.menu_poke = app_commands.ContextMenu(
            name="Poke Until Stop",
            callback=self.poke_menu
        )
        self.menu_stop = app_commands.ContextMenu(
            name="Stop Poke",
            callback=self.stop_menu
        )
        self.bot.tree.add_command(self.menu_poke)
        self.bot.tree.add_command(self.menu_stop)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.menu_poke.name, type=self.menu_poke.type)
        self.bot.tree.remove_command(self.menu_stop.name, type=self.menu_stop.type)

    # slash command
    @app_commands.command(name='poke', description='🔔 Wake someone up by moving them between voice channels!')
    async def poke_command(self, interaction: discord.Interaction, member: discord.Member, number: int):
        self.nameMember = member.name
        self.active_member = member
        await interaction.response.defer(ephemeral=True)
    
        if number <= 0:
            await interaction.followup.send("Please specify the number of rounds greater than 0!", ephemeral=True)
            return
        if not member.voice:
            await interaction.followup.send(f"{member.mention} Not In Voice Channel!", ephemeral=True)
            return

        originalChannel = member.voice.channel
        channel1 = None
        channel2 = None
        try:
            await interaction.followup.send(f"{interaction.user.name} move {member.mention} {number} times", ephemeral=True)  # Initial response
            room1 = "🔔 Poke room 1"
            room2 = "🔔 Poke room 2"
            channel1 = await interaction.guild.create_voice_channel(room1)
            channel2 = await interaction.guild.create_voice_channel(room2)

            for attempt in range(number):
                if not self.stopLoop:
                    await asyncio.gather(
                        member.send(f"{interaction.user.mention} Calling you for the {attempt+1} time"),
                        member.move_to(channel1)
                    )
                    await asyncio.sleep(1)  # Wait for 1 second
                    await member.move_to(channel2)
                    

            # Move back to the original channel
            self.stopLoop = False
            await member.send(f"{member.mention} We tried to wake you up!")
            await member.move_to(originalChannel)
        except Forbidden:
            await interaction.followup.send(f"You must have given the bot permission in your private room.", ephemeral=True)
            
            # Choose an existing voice channel to move the member to (e.g., "General" or any channel in the server)
            existingCannel = None
        
            for channel in interaction.guild.voice_channels:
                # Check if the bot has permission to move members in this channel
                if channel.permissions_for(interaction.guild.me).move_members:
                    existingCannel = channel
                    break

            if existingCannel and existingCannel.name not in [room1, room2]:
                await member.move_to(existingCannel)
                await interaction.followup.send(f"{member.mention} has been moved to {existingCannel.name}.", ephemeral=True)
                return
            else:
                await interaction.followup.send("There is no channel that the bot has access to.", ephemeral=True)
                return
            
        except Exception as e:
            await interaction.followup.send(f"{member.mention} Leave a poke room", ephemeral=True)
        finally:
            # Clean up channels
            self.stopLoop = None
            self.active_member = None
            self.nameMember = None
            self.userStop = None
            if channel1:
                try:
                    await channel1.delete()
                except:
                    pass
            if channel2:
                try:
                    await channel2.delete()
                except:
                    pass

    # context menu
    async def poke_menu(self, ctx: discord.Interaction, member: discord.Member):
        number = 4
        self.nameMember = member.name
        self.active_member = member
    
        await ctx.response.defer(ephemeral=True)
    
        if number <= 0:
            await ctx.followup.send("Please specify the number of rounds greater than 0!")
            return
        if not member.voice:
            await ctx.followup.send(f"{member.mention} Not In Voice Channel!")
            return

        originalChannel = member.voice.channel
        channel1 = None
        channel2 = None
        try:
            await ctx.followup.send(f"{ctx.user.name} move {member.mention} until stop")  # Initial response
            room1 = "🔔 Poke room 1"
            room2 = "🔔 Poke room 2"
            channel1 = await ctx.guild.create_voice_channel(room1)
            channel2 = await ctx.guild.create_voice_channel(room2)

            count = 1
            while True:
                await asyncio.gather(
                    member.send(f"{ctx.user.mention} Calling you for the {count} time"),
                    member.move_to(channel1)
                )
                await asyncio.sleep(1)  # Wait for 1 second
                await member.move_to(channel2)
                count += 1
                if self.stopLoop and self.userStop == member or count >= 500:
                    break
                    

            # Move back to the original channel
            self.stopLoop = False
            await member.send(f"{member.mention} We tried to wake you up!")
            await member.move_to(originalChannel)
        except Forbidden:
            await ctx.followup.send(f"You must have given the bot permission in your private room.", ephemeral=True)
            
            # Choose an existing voice channel to move the member to (e.g., "General" or any channel in the server)
            existingCannel = None
        
            for channel in ctx.guild.voice_channels:
                if channel.permissions_for(ctx.guild.me).move_members:
                    existingCannel = channel
                    break

            if existingCannel and existingCannel.name not in [room1, room2]:
                await member.move_to(existingCannel)
                await ctx.followup.send(f"{member.mention} has been moved to {existingCannel.name}.", ephemeral=True)
                return
            else:
                await ctx.followup.send("There is no channel that the bot has access to.", ephemeral=True)
                return
            
        except Exception as e:
            await ctx.followup.send(f"{member.mention} Leave a poke room", ephemeral=True)
        finally:
            self.stopLoop = None
            self.active_member = None
            self.nameMember = None
            self.userStop = None
            if channel1:
                try:
                    await channel1.delete()
                except:
                    pass
            if channel2:
                try:
                    await channel2.delete()
                except:
                    pass


    # Prefix Command: \stop
    @commands.command()
    async def stop(self, ctx):
        self.stopLoop = True
        if self.active_member:
            self.userStop = self.active_member
            await ctx.send(f'You stop poke {self.active_member.name}.')
        else:
            await ctx.send('There is no trigger currently operating.')

    # Slash Command: /stop
    @app_commands.command(name='stop', description='Stop Move Some Member')
    @app_commands.describe(
        member='The member to stop poking'
    )
    async def stop_command(self, interaction: discord.Interaction, member: str):
        await interaction.response.defer(ephemeral=True)
        if self.active_member and self.active_member.name == member:
            self.userStop = self.active_member
            self.stopLoop = True
            await interaction.followup.send(f'You stop poke {self.active_member.name}.', ephemeral=True)
        else:
            await interaction.followup.send('There is no trigger currently operating for this member.', ephemeral=True)

    @stop_command.autocomplete('member')
    async def stop_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        if self.active_member and current.lower() in self.active_member.name.lower():
            return [
                app_commands.Choice(name=self.active_member.name, value=self.active_member.name)
            ]
        return []

    # Context Menu: Stop Poke 
    async def stop_menu(self, ctx: discord.Interaction, user: discord.User):
        await ctx.response.defer(ephemeral=True)
        if self.active_member and self.active_member.id == user.id:
            self.userStop = user
            self.stopLoop = True
            await ctx.followup.send(f'You stop poke {self.active_member.name}.', ephemeral=True)
        else:
            await ctx.followup.send('Please press stop on the person being poked.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Poke(bot))