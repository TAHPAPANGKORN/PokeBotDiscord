import os
from myserver import server_on
import discord
from discord.ext import commands
from discord import app_commands, Forbidden, ui
import discord.utils
import asyncio
from datetime import datetime, timedelta
import pytz

bot = commands.Bot(command_prefix="\\", intents=discord.Intents.all(),help_command=None)

TOKEN = os.environ.get('token')


status = "/help afk poke bot"
stopLoop = None
baseColor = 0xECE7D9
#--------- check ---------
@bot.event
async def on_ready():
    print("Now online!!")
    activity = discord.Activity(type=discord.ActivityType.playing, name=status)
    await bot.change_presence(activity=activity)
    synced = await bot.tree.sync()
    print(f'{len(synced)} command(s) Logged in as {bot.user}')

@bot.command(aliases=['ready','start'])
async def _ready(ctx):
    await ctx.send("online")
#--------- end check ---------
    

#--------- help ---------
def get_embed(language='th'):
    embedColor = baseColor
    if language == 'th':
        title = "🤖 Help Me! - คำสั่งบอท"
        description = (
            "## 📌 Prefix คำสั่ง:\n"
            "`\\` = คำสั่งแบบเดิม\n"
            "`/` = คำสั่งแบบ Slash\n\n"
            "### 📎 คำสั่งแบบ Prefix (\\\\)  \n"
            "**\\help** : แสดงคำแนะนำ\n"
            "**\\stop** : หยุดการทำงาน\n\n"
            "### ⚙️ Slash Commands (/) แนะนำ\n"
            "**/help** : 📘 คำแนะนำ\n"
            "**/poke** : 🔔 ปลุกเพื่อน\n"
            "**/stop** : ⛔ หยุดบอท\n"
            "**/invite** : 🔗 แชร์ลิงก์\n"
            "**/micmute** : 🎤 ปิดไมค์ชั่วคราว\n"
            "**/headphonemute** : 🎧 ปิดหูฟังชั่วคราว\n\n"
            "### 📲 เมนูแอป\n"
            "**🌀 Poke Until Stop** : ทำงานจนกว่าจะหยุด\n"
            "**🛑 Stop Poke** : หยุดการทำงาน\n\n"
            "### ⚠️ หมายเหตุ\n"
            "หากผู้ถูก Poke ไม่เปิดแจ้งเตือน บอทอาจทำงานไม่สมบูรณ์"
        )
    else:
        title = "🤖 Help Me! - Bot Commands"
        description = (
            "## 📌 Command Prefix:\n"
            "`\\` = Traditional command\n"
            "`/` = Slash command\n\n"
            "### 📎 Prefix Commands (\\\\) \n"
            "**\\help** : Show help info\n"
            "**\\stop** : Stop bot action\n\n"
            "### ⚙️ Slash Commands (/) RECOMMEND\n"
            "**/help** : 📘 Help information\n"
            "**/poke** : 🔔 Wake friends\n"
            "**/stop** : ⛔ Stop bot\n"
            "**/invite** : 🔗 Invite link\n"
            "**/micmute** : 🎤 Mute mic temporarily\n"
            "**/headphonemute** : 🎧 Mute headphones temporarily\n\n"
            "### 📲 App Menu\n"
            "**🌀 Poke Until Stop** : Poke until stopped\n"
            "**🛑 Stop Poke** : Stop poking\n\n"
            "### ⚠️ Note\n"
            "If the user has notifications off, it may not work properly."
        )

    return discord.Embed(
        title=title,
        description=description,
        color=embedColor,
        timestamp=discord.utils.utcnow()
    )

        
@bot.command(aliases=['help', 'help_me', 'hp'])
async def _help(ctx):
    embed = get_embed('en')  

    # Callback เมื่อผู้ใช้เลือกภาษา
    async def select_callback(interaction: discord.Interaction):
        selected_lang = select.values[0]
        new_embed = get_embed(selected_lang)
        await interaction.response.edit_message(embed=new_embed, view=view)

    # สร้าง dropdown menu
    select = discord.ui.Select(
        placeholder="🔄 เลือกภาษา / Choose Language",
        options=[
            discord.SelectOption(label="ไทย", value="th", emoji="🇹🇭", description="ช่วยเหลือภาษาไทย"),
            discord.SelectOption(label="English", value="en", emoji="🇬🇧", description="Help in English")
        ]
    )
    select.callback = select_callback

    # สร้าง View แล้วใส่ select เข้าไป
    view = discord.ui.View()
    view.add_item(select)

    # ส่งข้อความพร้อม embed และ view
    await ctx.send(embed=embed, view=view)

@bot.tree.command(name="help", description="Show help information")
async def help(interaction: discord.Interaction):
    embed = get_embed('en')  

    async def select_callback(select_interaction: discord.Interaction):
        selected_lang = select.values[0]
        new_embed = get_embed(selected_lang)
        await select_interaction.response.edit_message(embed=new_embed, view=view)

    # สร้าง dropdown menu
    select = ui.Select(
        placeholder="🔄 เลือกภาษา / Choose Language",
        options=[
            discord.SelectOption(label="ไทย", value="th", emoji="🇹🇭", description="คำสั่งช่วยเหลือภาษาไทย"),
            discord.SelectOption(label="English", value="en", emoji="🇬🇧", description="Help commands in English")
        ]
    )
    select.callback = select_callback

    # ใส่ dropdown ใน view
    view = ui.View()
    view.add_item(select)

    # ส่ง message ผ่าน slash command
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
#--------- end help ---------

#--------- link ---------
botLink = "https://discord.com/oauth2/authorize?client_id=1208764608727359601"
@bot.tree.command(name='invite', description='Get Link To Invite')
async def sendLink(ctx: discord.Interaction):
    await ctx.response.defer(ephemeral=True)
    # Create the embed
    emmbed = discord.Embed(
        title='Link for invite this bot',
        description='Click the button below to invite bot.',
        color=baseColor,
        timestamp=discord.utils.utcnow()
    )
    # Create a button
    view = discord.ui.View()
    # btn-1
    button1 = discord.ui.Button(
        label="Invite bot", 
        style=discord.ButtonStyle.link, 
        url = botLink
    )
    
    # btn-2
    async def button2Callback(interaction: discord.Interaction):
        # Send a follow-up message when button2 is clicked
        await interaction.response.send_message(
            f"Here is the invite link for the bot: {botLink}", 
            ephemeral=True
        )
    button2 = discord.ui.Button(
        label="Invite link", 
        style=discord.ButtonStyle.primary
    )
    button2.callback = button2Callback
    # btn-3
    button3 = discord.ui.Button(
            label="Youtube link", 
            style=discord.ButtonStyle.danger, 
            url='https://youtu.be/CVENTfDYJRs?si=LM7d4s3YcyujXG-T'
        )    

    # Add buttons to the view
    view.add_item(button1)
    view.add_item(button3)
    view.add_item(button2)
    await ctx.followup.send(embed=emmbed, view=view, ephemeral=True)
#--------- end link ---------


#--------- poke ---------
@bot.tree.command(name='poke', description='🔔 Wake someone up by moving them between voice channels!')
async def wakeMove(ctx: discord.Interaction, member: discord.Member, number: int):
    global stopLoop, nameMember
    nameMember = member.name
    # Acknowledge the interaction immediately
    await ctx.response.defer(ephemeral=True)
   
    if number <= 0:
        await ctx.followup.send("Please specify the number of rounds greater than 0!")
        return
    if not member.voice:
        await ctx.followup.send(f"{member.mention} Not In Voice Channel!")
        return

    originalChannel = member.voice.channel
    try:
        await ctx.followup.send(f"{ctx.user.name} move {member.mention} {number} times")  # Initial response
        room1 = "🔔 Poke room 1"
        room2 = "🔔 Poke room 2"
        channel1 = await ctx.guild.create_voice_channel(room1)
        channel2 = await ctx.guild.create_voice_channel(room2)

        for attempt in range(number):
            if not stopLoop:
                await asyncio.gather(
                    member.send(f"{ctx.user.mention} Calling you for the {attempt+1} time"),
                    member.move_to(channel1)
                )
                await asyncio.sleep(1)  # Wait for 1 second
                await member.move_to(channel2)
                

        # Move back to the original channel
        stopLoop = False
        await member.send(f"✅ {member.mention} We tried to wake you up!")
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
        stopLoop = None
        await channel1.delete()
        await channel2.delete()

@bot.tree.context_menu(name="Poke Until Stop")
async def menuWakeMove(ctx: discord.Interaction, member: discord.Member):
    global stopLoop, nameMember
    number = 4
    nameMember = member.name

    # Acknowledge the interaction immediately
    await ctx.response.defer(ephemeral=True)
   
    if number <= 0:
        await ctx.followup.send("Please specify the number of rounds greater than 0!")
        return
    if not member.voice:
        await ctx.followup.send(f"{member.mention} Not In Voice Channel!")
        return

    originalChannel = member.voice.channel
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
            if stopLoop and userStop == member or count >= 500:
                break
                

        # Move back to the original channel
        stopLoop = False
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
        stopLoop = None
        await channel1.delete()
        await channel2.delete()
#--------- end poke ---------

#--------- mic mute ---------
@bot.tree.command(name="micmute", description="Set time to mute microphone")
async def muteTime(ctx: discord.Interaction, member: discord.Member, time: int, unit: str = 's'):  
     
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}

    if unit not in units:
        await ctx.response.defer(ephemeral=True)
        await ctx.followup.send("❌ Invalid unit! Please use 's' for seconds, 'm' for minutes, or 'h' for hours.")
        return
    
    # Defer response to allow time to process
    await ctx.response.defer(ephemeral=True)

    # Calculate target time
    targetTime = now + timedelta(**{units[unit]: time})

    # Inform the user and wait
    if member.voice:
        try:
            await member.edit(mute=True)
            await ctx.followup.send(f"You mute {member.mention} until {targetTime.strftime('%H:%M:%S')} UTC+7")
            await discord.utils.sleep_until(targetTime)
            await member.edit(mute=False)
            await ctx.followup.send(f"Unmute! {member.mention}")
        except Exception as e:
            await ctx.followup.send(f"Error! {e}", ephemeral=True)
    else:
        await ctx.followup.send(f"{member.mention} not in a voice room")
#--------- end mic mute ---------

#--------- headphone mute ---------
@bot.tree.command(name="headphonemute", description="Set time to mute headphone.")
async def muteTime(ctx: discord.Interaction, member: discord.Member, time: int, unit: str = 's'):  
     
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}

    if unit not in units:
        await ctx.response.defer(ephemeral=True)
        await ctx.followup.send("❌ Invalid unit! Please use 's' for seconds, 'm' for minutes, or 'h' for hours.")
        return
    
    # Defer response to allow time to process
    await ctx.response.defer(ephemeral=True)

    # Calculate target time
    targetTime = now + timedelta(**{units[unit]: time})

    # Inform the user and wait
    if member.voice:
        try:
            await member.edit(deafen=True)
            await ctx.followup.send(f"You mute {member.mention} until {targetTime.strftime('%H:%M:%S')} UTC+7")
            await discord.utils.sleep_until(targetTime)
            await member.edit(deafen=False)
            await ctx.followup.send(f"Unmute! {member.mention}")
        except Exception as e:
            await ctx.followup.send(f"Error! {e}", ephemeral=True)
    else:
        await ctx.followup.send(f"{member.mention} not in a voice room")
#--------- end headphone mute ---------


#--------- call tah ---------
@bot.tree.command(name='tah', description='Call cheetah to your room')
async def callTah(ctx: discord.Interaction):
    tahId = 577053817674268673  # User ID as an integer
    tahMember = ctx.guild.get_member(tahId)  # Fetch the Member object

    if tahMember is None:
        await ctx.response.send_message("User with the specified ID is not in this server.")
        return

    tah = tahMember.mention  # Discord name

    if ctx.user.voice and ctx.user.voice.channel:
        targetChannel = ctx.user.voice.channel
    else:
        await ctx.response.send_message("You must be in a voice channel to call someone.")
        return

    if tahMember.voice and tahMember.voice.channel == targetChannel:
        await ctx.response.send_message(f"{tah} is already in your room.")
        return

    if tahMember.voice:
        try:
            await tahMember.move_to(targetChannel)
            await ctx.response.send_message(f"Called {tah} to room {targetChannel.name}.")
        except Exception as e:
            await ctx.response.send_message(f"Failed to move {tah}: {str(e)}")
    else:
        await ctx.response.send_message(f"{tah} is not currently in a voice channel.")
#--------- end call tah ---------


#--------- stop ---------
@bot.command()
async def stop(ctx):
    global stopLoop
    await ctx.response.defer(ephemeral=True)
    # Stop the loop
    stopLoop = True
    if nameMember:
        await ctx.followup.send(f'You stop poke {nameMember}.', ephemeral=True)
    else:
        await ctx.followup.send('There is no trigger currently operating.', ephemeral=True)

@bot.tree.command(name='stop', description='Stop Move Some Member')
async def stop(ctx: discord.Interaction):
    global stopLoop
    await ctx.response.defer(ephemeral=True)
    # Stop the loop
    stopLoop = True
    if nameMember:
        await ctx.followup.send(f'You stop poke {nameMember}.', ephemeral=True)
    else:
        await ctx.followup.send('There is no trigger currently operating.', ephemeral=True)

@bot.tree.context_menu(name="Stop Poke")
async def menuStop(ctx: discord.Interaction, user: discord.User):
    global stopLoop, userStop
    await ctx.response.defer(ephemeral=True)
    
    # Stop the loop
    userStop = user
    stopLoop = True
    if nameMember == userStop:
        await ctx.followup.send(f'You stop poke {nameMember}.', ephemeral=True)
        await ctx.followup.send('Please press stop on the person being poke.', ephemeral=True)
#--------- end stop ---------


  
server_on()
bot.run(TOKEN)



