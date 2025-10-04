import discord
from discord.ext import commands
from discord import app_commands

class PlayerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='create-player', description='Criar um player')
    @app_commands.describe(name='Nome do Jogador', nick='Nick do Jogador')
    async def save_game(self, interaction: discord.Interaction, name: str, nick: str):
        # TODO - implementar funcionalidade 
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier`).', 
            ephemeral=True
        )

    @app_commands.command(name='update-player', description='Atualizar um player')
    @app_commands.describe(id='ID do Jogador', name='Nome do Jogador', nick='Nick do Jogador')
    async def save_game(self, interaction: discord.Interaction, name: str, nick: str):
        # TODO - implementar funcionalidade 
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier`).', 
            ephemeral=True
        )

    @app_commands.command(name='get-player-id', description='Pegar o id de um player pelo nome ou nick')
    @app_commands.describe(name='Nome do Jogador', nick='Nick do Jogador')
    async def save_game(self, interaction: discord.Interaction, name: str=None, nick: str=None):
        # TODO - implementar funcionalidade 
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier`).', 
            ephemeral=True
        )