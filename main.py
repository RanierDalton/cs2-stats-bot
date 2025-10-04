import discord
from discord import app_commands
import os
from dotenv import load_dotenv
from src.main.Bot import Bot

if __name__ == "__main__":
    load_dotenv()
    bot = Bot()

    @bot.tree.command(name='ping', description='Teste de resposta')
    async def ping_command(interaction: discord.Interaction): # Renomeado para evitar conflito
        await interaction.response.send_message(f'Pong!', ephemeral=True)
        
    bot.run(os.getenv('BOT_TOKEN'))