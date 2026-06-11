import discord
from discord.ext import commands
from discord import app_commands, Forbidden
import discord.utils
import asyncio
class Poke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_pokes = {}
        self.guild_locks = {}

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

    def get_guild_lock(self, guild_id: int) -> asyncio.Lock:
        if guild_id not in self.guild_locks:
            self.guild_locks[guild_id] = asyncio.Lock()
        return self.guild_locks[guild_id]

    async def get_or_create_poke_channels(self, guild: discord.Guild):
        async with self.get_guild_lock(guild.id):
            room1_name = "🔔 Poke room 1"
            room2_name = "🔔 Poke room 2"
            
            channel1 = discord.utils.get(guild.voice_channels, name=room1_name)
            channel2 = discord.utils.get(guild.voice_channels, name=room2_name)
            
            if not channel1:
                channel1 = await guild.create_voice_channel(room1_name)
            if not channel2:
                channel2 = await guild.create_voice_channel(room2_name)
                
            return channel1, channel2

    async def cleanup_guild_poke_channels(self, guild: discord.Guild):
        async with self.get_guild_lock(guild.id):
            active_in_guild = any(
                state['member'].guild.id == guild.id 
                for state in self.active_pokes.values()
            )
            if not active_in_guild:
                room1_name = "🔔 Poke room 1"
                room2_name = "🔔 Poke room 2"
                channel1 = discord.utils.get(guild.voice_channels, name=room1_name)
                channel2 = discord.utils.get(guild.voice_channels, name=room2_name)
                
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

    # slash command
    @app_commands.command(name='poke', description='🔔 Wake someone up by moving them between voice channels!')
    @app_commands.describe(
        member='member that you want to poke',
        rounds='number of rounds you want to poke'
    )
    async def poke_command(self, interaction: discord.Interaction, member: discord.Member, rounds: int):
        await interaction.response.defer(ephemeral=True)
        
        if member.id in self.active_pokes:
            await interaction.followup.send(f"{member.mention} is already being poked!", ephemeral=True)
            return
    
        if rounds <= 0:
            await interaction.followup.send("Please specify the number of rounds greater than 0!", ephemeral=True)
            return
        if not member.voice:
            await interaction.followup.send(f"{member.mention} Not In Voice Channel!", ephemeral=True)
            return

        self.active_pokes[member.id] = {
            'member': member,
            'stop_loop': False
        }

        originalChannel = member.voice.channel
        try:
            await interaction.followup.send(f"{interaction.user.name} move {member.mention} {rounds} times", ephemeral=True)  # Initial response
            channel1, channel2 = await self.get_or_create_poke_channels(interaction.guild)

            for attempt in range(rounds):
                state = self.active_pokes.get(member.id)
                if state and not state['stop_loop']:
                    await asyncio.gather(
                        member.send(f"{interaction.user.mention} Calling you for the {attempt+1} time"),
                        member.move_to(channel1)
                    )
                    await asyncio.sleep(1)  # Wait for 1 second
                    await member.move_to(channel2)
                    
            # Move back to the original channel
            await member.send(f"{member.mention} We tried to wake you up!")
            await member.move_to(originalChannel)
        except Forbidden:
            await interaction.followup.send(f"You must have given the bot permission in your private room.", ephemeral=True)
            
            # Choose an existing voice channel to move the member to (e.g., "General" or any channel in the server)
            existingCannel = None
        
            for channel in interaction.guild.voice_channels:
                if channel.permissions_for(interaction.guild.me).move_members and channel.name not in ["🔔 Poke room 1", "🔔 Poke room 2"]:
                    existingCannel = channel
                    break

            if existingCannel:
                await member.move_to(existingCannel)
                await interaction.followup.send(f"{member.mention} has been moved to {existingCannel.name}.", ephemeral=True)
                return
            else:
                await interaction.followup.send("There is no channel that the bot has access to.", ephemeral=True)
                return
            
        except Exception as e:
            await interaction.followup.send(f"{member.mention} Leave a poke room", ephemeral=True)
        finally:
            self.active_pokes.pop(member.id, None)
            await self.cleanup_guild_poke_channels(interaction.guild)

    # context menu
    async def poke_menu(self, ctx: discord.Interaction, member: discord.Member):
        number = 4
        await ctx.response.defer(ephemeral=True)

        if member.id in self.active_pokes:
            await ctx.followup.send(f"{member.mention} is already being poked!", ephemeral=True)
            return
    
        if number <= 0:
            await ctx.followup.send("Please specify the number of rounds greater than 0!")
            return
        if not member.voice:
            await ctx.followup.send(f"{member.mention} Not In Voice Channel!")
            return

        self.active_pokes[member.id] = {
            'member': member,
            'stop_loop': False
        }

        originalChannel = member.voice.channel
        try:
            await ctx.followup.send(f"{ctx.user.name} move {member.mention} until stop")  # Initial response
            channel1, channel2 = await self.get_or_create_poke_channels(ctx.guild)

            count = 1
            while True:
                await asyncio.gather(
                    member.send(f"{ctx.user.mention} Calling you for the {count} time"),
                    member.move_to(channel1)
                )
                await asyncio.sleep(1)  # Wait for 1 second
                await member.move_to(channel2)
                count += 1
                state = self.active_pokes.get(member.id)
                if not state or state['stop_loop'] or count >= 500:
                    break
                    

            # Move back to the original channel
            await member.send(f"{member.mention} We tried to wake you up!")
            await member.move_to(originalChannel)
        except Forbidden:
            await ctx.followup.send(f"You must have given the bot permission in your private room.", ephemeral=True)
            
            # Choose an existing voice channel to move the member to (e.g., "General" or any channel in the server)
            existingCannel = None
        
            for channel in ctx.guild.voice_channels:
                if channel.permissions_for(ctx.guild.me).move_members and channel.name not in ["🔔 Poke room 1", "🔔 Poke room 2"]:
                    existingCannel = channel
                    break

            if existingCannel:
                await member.move_to(existingCannel)
                await ctx.followup.send(f"{member.mention} has been moved to {existingCannel.name}.", ephemeral=True)
                return
            else:
                await ctx.followup.send("There is no channel that the bot has access to.", ephemeral=True)
                return
            
        except Exception as e:
            await ctx.followup.send(f"{member.mention} Leave a poke room", ephemeral=True)
        finally:
            self.active_pokes.pop(member.id, None)
            await self.cleanup_guild_poke_channels(ctx.guild)


    # Prefix Command: \stop [member_name]
    @commands.command()
    async def stop(self, ctx, *, member_name: str = None):
        if not self.active_pokes:
            await ctx.send('There is no trigger currently operating.')
            return

        if member_name:
            target_id = None
            target_name = None
            for mid, state in self.active_pokes.items():
                if state['member'].name.lower() == member_name.lower():
                    target_id = mid
                    target_name = state['member'].name
                    break
            
            if target_id:
                self.active_pokes[target_id]['stop_loop'] = True
                await ctx.send(f"You stop poke {target_name}.")
            else:
                await ctx.send(f"No active poke trigger found for '{member_name}'.")
        else:
            names = [state['member'].name for state in self.active_pokes.values()]
            for state in self.active_pokes.values():
                state['stop_loop'] = True
            await ctx.send(f"You stopped all active pokes for: {', '.join(names)}.")

    # Slash Command: /stop
    @app_commands.command(name='stop', description='Stop Move Some Member')
    @app_commands.describe(
        member='The member to stop poking'
    )
    async def stop_command(self, interaction: discord.Interaction, member: str):
        await interaction.response.defer(ephemeral=True)
        target_id = None
        target_name = None
        for mid, state in self.active_pokes.items():
            if state['member'].name == member:
                target_id = mid
                target_name = state['member'].name
                break
        
        if target_id:
            self.active_pokes[target_id]['stop_loop'] = True
            await interaction.followup.send(f'You stop poke {target_name}.', ephemeral=True)
        else:
            await interaction.followup.send('There is no trigger currently operating for this member.', ephemeral=True)

    @stop_command.autocomplete('member')
    async def stop_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        choices = []
        for state in self.active_pokes.values():
            name = state['member'].name
            if current.lower() in name.lower():
                choices.append(app_commands.Choice(name=name, value=name))
        return choices[:25]

    # Context Menu: Stop Poke 
    async def stop_menu(self, ctx: discord.Interaction, user: discord.User):
        await ctx.response.defer(ephemeral=True)
        if user.id in self.active_pokes:
            self.active_pokes[user.id]['stop_loop'] = True
            await ctx.followup.send(f'You stop poke {self.active_pokes[user.id]["member"].name}.', ephemeral=True)
        else:
            await ctx.followup.send('Please press stop on the person being poked.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Poke(bot))