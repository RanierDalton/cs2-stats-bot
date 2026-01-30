import discord
from discord.ext import commands
from discord import app_commands
from ..service.PlayerService import PlayerService
from ..base.Player import Player

class PlayerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.player_service = PlayerService()

    @app_commands.command(name='create-player', description='Criar um player')
    @app_commands.describe(name='Nome do Jogador', nick='Nick do Jogador')
    async def create_player(self, interaction: discord.Interaction, name: str, nick: str):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            if not name or not nick:
                await interaction.followup.send('Nome e Nick são obrigatórios.', ephemeral=True)
                return

            player = Player(None, name, nick)
            self.player_service.save(player)
            
            await interaction.followup.send(
                f'Jogador **{name}** ({nick}) criado com sucesso!', 
                ephemeral=False
            )
        except Exception as e:
             await interaction.followup.send(f'Erro ao criar jogador: {e}', ephemeral=True)

    @app_commands.command(name='update-player', description='Atualizar um player')
    @app_commands.describe(id='ID do Jogador', name='Nome do Jogador', nick='Nick do Jogador')
    async def update_player(self, interaction: discord.Interaction, id:int, name: str=None, nick: str=None):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            player = self.player_service.get_player_by_id(id)
            if not player:
                await interaction.followup.send(f'Jogador com ID {id} não encontrado.', ephemeral=True)
                return

            player.set_name(name)
            player.set_nick(nick)
            self.player_service.update(player)

            await interaction.followup.send(
                f'Jogador **{name}** ({nick}) atualizado com sucesso!', 
                ephemeral=False
            )
        except Exception as e:
            await interaction.followup.send(f'Erro ao atualizar jogador: {e}', ephemeral=True)

    @app_commands.command(name='get-player-id', description='Pegar o id de um player pelo nome ou nick')
    @app_commands.describe(name='Nome do Jogador', nick='Nick do Jogador')
    async def get_player_by_id(self, interaction: discord.Interaction, name: str=None, nick: str=None):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            if not name and not nick:
                await interaction.followup.send('Forneça pelo menos o Nome ou Nick para busca.', ephemeral=True)
                return

            player = None
            if nick:
                player = self.player_service.get_player_by_nick(nick)
            elif name:
                player = self.player_service.get_player_by_name(name)

            if player:
                await interaction.followup.send(
                    f'Jogador encontrado: **{player.name}** ({player.nick}) - ID: **{player.id}**', 
                    ephemeral=False
                )
            else:
                search_term = nick if nick else name
                await interaction.followup.send(
                    f'Nenhum jogador encontrado com o nick/nome: {search_term}', 
                    ephemeral=True
                )
        except Exception as e:
            await interaction.followup.send(f'Erro ao buscar jogador: {e}', ephemeral=True)