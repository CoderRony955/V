import discord
from discord.ext import commands
import logging
import ollama

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)


# ----------- Enable bot logging --------------
logging.basicConfig(filename="V-discord-bot/bot-logs/V_bot.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

# ---------------- Bot commands --------------------------


@bot.event
async def on_ready():
    Activity = discord.Game(name='-q <question>')
    await bot.change_presence(status=discord.Status.online, activity=Activity)
    print(f'Bot {bot.user.name} has connected to Discord!')
    await bot.tree.sync()


@bot.command(name='q', description='chat with bot')
async def ask(ctx, query: str):
    try:
        user = ctx.author
        stream = ollama.chat(
            model='V:latest',
            messages=[{'role': 'user', 'content': query}],
        )

        embed = discord.Embed(
            description=f'{stream['message']['content']}',
            color=0x15161E
        )
        embed.set_footer(text=f"Requested by {user.name}",
                         icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

        logger.info(
            f'User ask: {query}\nBot response: {stream['message']['content']}')
        await ctx.send(embed=embed)

    except discord.DiscordException as e:

        embed = discord.Embed(
            title='Oops!',
            description=f'An Exception error occurred: {e}',
            color=0xFD1717
        )
        logger.error(f'An Exception error occurred: {e}')
        await ctx.send(embed=embed)


# ------------------------- Slash commands---------------------------------------

@bot.tree.command(name='help', description='get bot help')
async def help(interaction: discord.Interaction):
    try:
        help_des = """
        A *Space Science* AI Chatbot Powered by **Qwen2.5 model**. Designed to engage users in insightful discussions about space, astronomy, astrophysics, and the mysteries of the universe, whether you are a space enthusiast, a student, or a professional researcher, this chatbot serves as a knowledgeable and interactive companion for exploring the cosmos.
        
        **For chatting use given specific command:**
        ```
        -q what is the age of universe?
        ```
        
        *Let's chat!*
        """

        embed = discord.Embed(
            title='V here',
            description=help_des,
            color=0x1C1C26
        )
        logger.info('User use help command')
        await interaction.response.send_message(embed=embed)

    except discord.DiscordException as e:
        logger.error(f'An Exception error occurred: {e}')
        embed = discord.Embed(
            title='Oops!',
            description=f'An Exception error occurred: {e}',
            color=0xEA0707
        )
        logger.error(f'An exception error occurred: {e}')
        await interaction.response.send_message(embed=embed)


# Run the bot
TOKEN = "BOT-TOKEN"
bot.run(TOKEN)
