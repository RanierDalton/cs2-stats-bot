import discord
from discord.ext import commands
from discord import app_commands

class PlayerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='create-player', description='Criar um player')
    @app_commands.describe(name='Nome do Jogador', nick='Nick do Jogador')
    async def create_player(self, interaction: discord.Interaction, name: str, nick: str):
        await interaction.response.defer(thinking=True, ephemeral=False)
        # TODO - implementar funcionalidade 
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier', 
            ephemeral=False
        )

    @app_commands.command(name='update-player', description='Atualizar um player')
    @app_commands.describe(id='ID do Jogador', name='Nome do Jogador', nick='Nick do Jogador')
    async def update_player(self, interaction: discord.Interaction, id:int, name: str, nick: str):
        await interaction.response.defer(thinking=True, ephemeral=False)
        # TODO - implementar funcionalidade 
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier', 
            ephemeral=False
        )

    @app_commands.command(name='get-player-id', description='Pegar o id de um player pelo nome ou nick')
    @app_commands.describe(name='Nome do Jogador', nick='Nick do Jogador')
    async def get_player_by_id(self, interaction: discord.Interaction, name: str=None, nick: str=None):
        await interaction.response.defer(thinking=True, ephemeral=False)
        # TODO - implementar funcionalidade 
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier', 
            ephemeral=False
        )