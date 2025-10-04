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

        # data = ImageDataLoader(caminho_local).analyse_scoreboard()
        data = {
        "score":"13-9",
        "status":"VITÓRIA",
        "players":[
            {
                "nick":"Lucas Foguetes ツ",
                "kda":"16/7/7",
                "tag":"Amaciador",
                "hs":"40%"
            },
            {
                "nick":"Mr.Azeitona",
                "kda":"27/12/1",
                "tag":"Matador quádruplo",
                "hs":"55%"
            },
            {
                "nick":"raynier",
                "kda":"22/15/2",
                "tag":"Senhor das armas",
                "hs":"50%"
            },
            {
                "nick":"Латинский алфави",
                "kda":"13/16/5",
                "tag":"Incendiário",
                "hs":"15%"
            },
            {
                "nick":"Tu-π",
                "kda":"8/12/5",
                "tag":"Ofuscante",
                "hs":"12%"
            }
        ]
        }

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
            'Jogo e estatísticas salvos com sucesso!',
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(GameCommands(bot))