import discord
from discord.ext import commands
from discord import app_commands
import discord.utils
import os
from data.help_data import HELP_TEXTS, COMMANDS_METADATA

baseColor = 0x7669FD
botLink = "https://discord.com/oauth2/authorize?client_id=1208764608727359601"
youtubeLink = "https://youtu.be/CVENTfDYJRs?si=LM7d4s3YcyujXG-T"

def get_embed(language='th', bot_avatar_url=None):
    embedColor = baseColor
    texts = HELP_TEXTS.get(language, HELP_TEXTS['en'])
    
    # Build description dynamically
    description_parts = [texts['description_header']]
    
    categories = ['prefix', 'slash', 'context']
    for cat in categories:
        description_parts.append(texts['category_headers'][cat])
        
        # Filter commands of this category
        cat_commands = [c for c in COMMANDS_METADATA if c['type'] == cat]
        for cmd in cat_commands:
            emoji = cmd.get('emoji', '')
            emoji_str = f"{emoji} " if emoji else ""
            name = cmd['name']
            desc = cmd['description'].get(language, cmd['description']['en'])
            
            # Format command based on type
            if cat == 'prefix':
                formatted_cmd = f"**\\{name}** : {emoji_str}{desc}"
            elif cat == 'slash':
                formatted_cmd = f"**/{name}** : {emoji_str}{desc}"
            else: # context
                formatted_cmd = f"**{name}** : {emoji_str}{desc}"
                
            description_parts.append(formatted_cmd)
        description_parts.append("") # blank line for spacing
        
    # Add Note section
    description_parts.append(f"### {texts['note_title']}")
    description_parts.append(texts['note_description'])
    
    description = "\n".join(description_parts)
    
    embed = discord.Embed(
        title=texts['title'],
        description=description,
        color=embedColor,
        timestamp=discord.utils.utcnow()
    )
    
    if bot_avatar_url:
        embed.set_thumbnail(url=bot_avatar_url)
        
    embed.set_footer(text=texts['footer_text'])
    return embed


class HelpView(discord.ui.View):
    def __init__(self, current_lang='en', bot_avatar_url=None):
        super().__init__(timeout=180)
        self.current_lang = current_lang
        self.bot_avatar_url = bot_avatar_url
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        
        # Language switcher buttons
        th_style = discord.ButtonStyle.primary if self.current_lang == 'th' else discord.ButtonStyle.secondary
        en_style = discord.ButtonStyle.primary if self.current_lang == 'en' else discord.ButtonStyle.secondary
        
        th_button = discord.ui.Button(label="ภาษาไทย", emoji="🇹🇭", style=th_style, custom_id="lang_th")
        en_button = discord.ui.Button(label="English", emoji="🇬🇧", style=en_style, custom_id="lang_en")
        
        th_button.callback = self.lang_th_callback
        en_button.callback = self.lang_en_callback
        
        self.add_item(th_button)
        self.add_item(en_button)
        
        # Action/Link buttons
        invite_button = discord.ui.Button(label="Invite Bot", style=discord.ButtonStyle.link, url=botLink)
        
        self.add_item(invite_button)

    async def lang_th_callback(self, interaction: discord.Interaction):
        self.current_lang = 'th'
        self.update_buttons()
        embed = get_embed('th', self.bot_avatar_url)
        await interaction.response.edit_message(embed=embed, view=self)

    async def lang_en_callback(self, interaction: discord.Interaction):
        self.current_lang = 'en'
        self.update_buttons()
        embed = get_embed('en', self.bot_avatar_url)
        await interaction.response.edit_message(embed=embed, view=self)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['help', 'help_me', 'hp'])
    async def _help(self, ctx):
        avatar_url = self.bot.user.avatar.url if self.bot.user.avatar else None
        embed = get_embed('en', avatar_url)
        view = HelpView(current_lang='en', bot_avatar_url=avatar_url)
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="help", description="Show help information")
    async def help(self, interaction: discord.Interaction):
        avatar_url = self.bot.user.avatar.url if self.bot.user.avatar else None
        embed = get_embed('en', avatar_url)
        view = HelpView(current_lang='en', bot_avatar_url=avatar_url)
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

    # Slash Command: /tah
    @app_commands.command(name='tah', description='Call cheetah to your room')
    async def callTah(self, ctx: discord.Interaction):
        tahId = int(os.environ.get('OWNER_ID', '123123123'))
        tahMember = ctx.guild.get_member(tahId)

        await ctx.response.defer(ephemeral=True) 

        if tahMember is None:
            await ctx.followup.send("User with the specified ID is not in this server.", ephemeral=True)
            return

        tah = tahMember.mention

        if ctx.user.voice and ctx.user.voice.channel:
            targetChannel = ctx.user.voice.channel
        else:
            await ctx.followup.send("You must be in a voice channel to call someone.", ephemeral=True)
            return

        if tahMember.voice and tahMember.voice.channel == targetChannel:
            await ctx.followup.send(f"{tah} is already in your room.", ephemeral=True)
            return

        if tahMember.voice:
            try:
                await tahMember.move_to(targetChannel)
                await ctx.followup.send(f"Called {tah} to room {targetChannel.name}.", ephemeral=True)
            except Exception as e:
                await ctx.followup.send(f"Failed to move {tah}: {str(e)}", ephemeral=True)
        else:
            await ctx.followup.send(f"{tah} is not currently in a voice channel.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(General(bot))