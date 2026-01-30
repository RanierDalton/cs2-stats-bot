import discord
from discord.ext import commands
from discord import app_commands
import os
from ..ImageDataLoader import ImageDataLoader
from ..mapper.GameMapper import GameMapper
from ..service.GameService import GameService
from ..mapper.StatMapper import StatMapper
from ..service.PlayerService import PlayerService
from ..service.MapService import MapService
from ..service.StatService import StatService
from ..base.Player import Player

# A classe precisa herdar de commands.Cog
class GameCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='save-game', description='Cadastrar um jogo')
    @app_commands.describe(imagem='Imagem do Final da Partida', mapa='Nome do Mapa')
    async def save_game(self, interaction: discord.Interaction, imagem: discord.Attachment, mapa: str): 
        if not imagem.content_type.startswith('image/'):
            await interaction.followup.send(
                f'Ops! O anexo precisa ser uma imagem (recebido: `{imagem.content_type}`).', 
                ephemeral=True
            )
            return

        await interaction.response.send_message('Calma kyuzans, recebendo e processando a imagem...', ephemeral=False)
        nome_arquivo = imagem.filename
        try:
            os.makedirs('image', exist_ok=True)
            caminho_local = os.path.join('image', nome_arquivo)
            
            await imagem.save(caminho_local) 
        except Exception as e:
            await interaction.followup.send(
                f'Erro ao salvar a imagem: `{e}`', 
                ephemeral=True
            )
            return

        data = ImageDataLoader(caminho_local).analyse_scoreboard()

        if not data:
            await interaction.followup.send(
                'Desculpe, não consegui analisar a imagem. Tente novamente com uma imagem mais clara.', 
                ephemeral=True
            )
            return
        
        map_id = MapService().get_id_by_name(mapa)

        if not map_id:
            await interaction.followup.send(
                f'Mapa informado "{mapa}" não consta no sistema.', 
                ephemeral=True
            )
            return

        game = GameMapper.from_dict(data=data, map_id=map_id)
        game_id = GameService().save_game(game)

        if not game_id:
            await interaction.followup.send(
                'Erro ao salvar os dados do jogo. Tente novamente mais tarde.', 
                ephemeral=True
            )
            return

        stats = StatMapper.from_dict_list(data.get('players'), game_id=game_id)
        player_service = PlayerService()
        stat_service = StatService()
        
        for stat in stats:
            player = player_service.get_player_by_nick(stat.player_nick)
            
            if not player:
                # Auto-create player if not exists
                # Using nick as name as fallback
                try: 
                    new_player = Player(None, stat.player_nick, stat.player_nick)
                    player_service.save(new_player)
                    # Retrieve again to get ID
                    player = player_service.get_player_by_nick(stat.player_nick)
                except Exception as e:
                    print(f"Erro ao criar jogador automaticamente: {e}")
                    continue # Skip stat save if player creation fails
            
            if player:
                stat.fk_player = player.id
                stat.fk_game = game_id
                stat_service.save_stat(stat)

        await interaction.followup.send(
            f'Jogo e estatísticas salvos com sucesso! Com o ID: {game_id}',
            ephemeral=False
        )

    @app_commands.command(name='delete-game', description='Deletar um jogo')
    @app_commands.describe(id='Id do Jogo')
    async def delete_game(self, interaction: discord.Interaction, id: int):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            game_service = GameService()
            game = game_service.get_game_by_id(id)
            if not game:
                await interaction.followup.send(f'Jogo com ID {id} não encontrado.', ephemeral=True)
                return
            
            game_service.delete_game(id)
            
            await interaction.followup.send(
                f'Jogo com ID {id} deletado com sucesso.', 
                ephemeral=False
            )
        except Exception as e:
            await interaction.followup.send(
                f'Erro ao deletar jogo: {e}', 
                ephemeral=True
            )