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

        # ลงทะเบียน Context Menu ในห้องเครื่องของ Cog
        self.menu_wake_move = app_commands.ContextMenu(
            name="Poke Until Stop",
            callback=self.menuWakeMove
        )
        self.menu_stop = app_commands.ContextMenu(
            name="Stop Poke",
            callback=self.menuStop
        )
        self.bot.tree.add_command(self.menu_wake_move)
        self.bot.tree.add_command(self.menu_stop)

    async def cog_unload(self):
        # ลบคำสั่งเมื่อ Cog ถูกถอดออกเพื่อป้องกันเมนูซ้ำซ้อน
        self.bot.tree.remove_command(self.menu_wake_move.name, type=self.menu_wake_move.type)
        self.bot.tree.remove_command(self.menu_stop.name, type=self.menu_stop.type)

    # slash command
    @app_commands.command(name='poke', description='🔔 Wake someone up by moving them between voice channels!')
    async def wakeMove(self, ctx: discord.Interaction, member: discord.Member, number: int):
        self.nameMember = member.name
        # Acknowledge the interaction immediately
        await ctx.response.defer(ephemeral=True)
    
        if number <= 0:
            await ctx.followup.send("Please specify the number of rounds greater than 0!", ephemeral=True)
            return
        if not member.voice:
            await ctx.followup.send(f"{member.mention} Not In Voice Channel!", ephemeral=True)
            return

        originalChannel = member.voice.channel
        channel1 = None
        channel2 = None
        try:
            await ctx.followup.send(f"{ctx.user.name} move {member.mention} {number} times", ephemeral=True)  # Initial response
            room1 = "🔔 Poke room 1"
            room2 = "🔔 Poke room 2"
            channel1 = await ctx.guild.create_voice_channel(room1)
            channel2 = await ctx.guild.create_voice_channel(room2)

            for attempt in range(number):
                if not self.stopLoop:
                    await asyncio.gather(
                        member.send(f"{ctx.user.mention} Calling you for the {attempt+1} time"),
                        member.move_to(channel1)
                    )
                    await asyncio.sleep(1)  # Wait for 1 second
                    await member.move_to(channel2)
                    

            # Move back to the original channel
            self.stopLoop = False
            await member.send(f"{member.mention} We tried to wake you up!")
            await member.move_to(originalChannel)
        except Forbidden:
            await ctx.followup.send(f"You must have given the bot permission in your private room.", ephemeral=True)
            
            # Choose an existing voice channel to move the member to (e.g., "General" or any channel in the server)
            existingCannel = None
        
            for channel in ctx.guild.voice_channels:
                # Check if the bot has permission to move members in this channel
                if channel.permissions_for(ctx.guild.me).move_members:
                    existingCannel = channel
                    break

            #existingCannel always true 
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
            # Clean up channels
            self.stopLoop = None
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


    async def menuWakeMove(self, ctx: discord.Interaction, member: discord.Member):
        number = 4
        self.nameMember = member.name

        # Acknowledge the interaction immediately
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
                # Check if the bot has permission to move members in this channel
                if channel.permissions_for(ctx.guild.me).move_members:
                    existingCannel = channel
                    break

            #existingCannel always true 
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
            # Clean up channels
            self.stopLoop = None
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
        if self.nameMember:
            await ctx.send(f'You stop poke {self.nameMember}.')
        else:
            await ctx.send('There is no trigger currently operating.')

    # Slash Command: /stop
    @app_commands.command(name='stop', description='Stop Move Some Member')
    async def stop_slash(self, ctx: discord.Interaction):
        await ctx.response.defer(ephemeral=True)
        self.stopLoop = True
        if self.nameMember:
            await ctx.followup.send(f'You stop poke {self.nameMember}.', ephemeral=True)
        else:
            await ctx.followup.send('There is no trigger currently operating.', ephemeral=True)

    # Context Menu: Stop Poke (คลิกขวาเพื่อหยุด)
    async def menuStop(self, ctx: discord.Interaction, user: discord.User):
        await ctx.response.defer(ephemeral=True)
        self.userStop = user
        self.stopLoop = True
        if self.nameMember == self.userStop:
            await ctx.followup.send(f'You stop poke {self.nameMember}.', ephemeral=True)
        else:
            await ctx.followup.send('Please press stop on the person being poke.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Poke(bot))