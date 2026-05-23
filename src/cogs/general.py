import discord
from discord.ext import commands
from discord import app_commands
import discord.utils

baseColor = 0xECE7D9
botLink = "https://discord.com/oauth2/authorize?client_id=1208764608727359601"
youtubeLink = "https://youtu.be/CVENTfDYJRs?si=LM7d4s3YcyujXG-T"

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


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['help', 'help_me', 'hp'])
    async def _help(self, ctx):
        embed = get_embed('en')  

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
    async def help(self, interaction: discord.Interaction):
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

    @app_commands.command(name="help", description="Show help information")
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

    @app_commands.command(name='invite', description='Get Link To Invite')
    async def sendLink(self, ctx: discord.Interaction):
        await ctx.response.defer(ephemeral=True)
        
        emmbed = discord.Embed(
            title='Link for invite this bot',
            description='Click the button below to invite bot.',
            color=baseColor,
            timestamp=discord.utils.utcnow()
        )
        
        view = discord.ui.View()
        button1 = discord.ui.Button(
            label="Invite bot", 
            style=discord.ButtonStyle.link, 
            url=botLink
        )
        
        async def button2Callback(interaction: discord.Interaction):
            await interaction.response.send_message(
                f"Here is the invite link for the bot: {botLink}", 
                ephemeral=True
            )
        button2 = discord.ui.Button(
            label="Invite link", 
            style=discord.ButtonStyle.primary
        )
        button2.callback = button2Callback
        
        button3 = discord.ui.Button(
            label="Youtube link", 
            style=discord.ButtonStyle.danger, 
            url=youtubeLink
        )    
        view.add_item(button1)
        view.add_item(button3)
        view.add_item(button2)
        await ctx.followup.send(embed=emmbed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Genernal(bot))