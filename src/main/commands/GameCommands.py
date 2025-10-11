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

        data = ImageDataLoader(caminho_local).analyse_scoreboard()

        if not data:
            await interaction.followup.send(
                'Desculpe, não consegui analisar a imagem. Tente novamente com uma imagem mais clara.', 
                ephemeral=True
            )
            return
        
        mapa = MapService().get_id_by_name(mapa)

        game = GameMapper.from_dict(data=data, map_id=mapa)
        game_id = GameService().save_game(game)

        if not game_id:
            await interaction.followup.send(
                'Erro ao salvar os dados do jogo. Tente novamente mais tarde.', 
                ephemeral=True
            )
            return

        if not mapa:
            await interaction.followup.send(
                'Mapa informado não consta no sistema', 
                ephemeral=True
            )
            return

        game = GameMapper.from_dict(data=data, map_id=mapa)
        game_id = GameService().save_game(game)
        stats = StatMapper.from_dict_list(data.get('players'), game_id=game_id)
        
        for stat in stats:
            player = PlayerService().get_player_by_nick(stat.player_nick)
            if player:
                stat.fk_player = player.id
                stat.fk_game = game_id
                StatService().save_stat(stat)

        await interaction.followup.send(
            f'Jogo e estatísticas salvos com sucesso! Com o ID: {game_id}',
            ephemeral=False
        )

    @app_commands.command(name='delete-game', description='Deletar um jogo')
    @app_commands.describe(id='Id do Jogo')
    async def delete_game(self, interaction: discord.Interaction, id: int):
        await interaction.response.defer(thinking=True, ephemeral=False)
        # TODO - implementar funcionalidade 
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier.', 
            ephemeral=False
        )