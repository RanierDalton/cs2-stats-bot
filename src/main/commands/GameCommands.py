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
from ..service.ImageService import ImageService
from ..base.Player import Player

# A classe precisa herdar de commands.Cog


class GameCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.map_service = MapService()

    async def map_autocomplete(self, interaction: discord.Interaction, current: str):
        try:
            maps = self.map_service.search_maps(current if current else "")
            return [app_commands.Choice(name=map_name, value=map_name) for map_name in maps[:25]]
        except Exception:
            return []

    @app_commands.command(name='save-game', description='Cadastrar um jogo')
    @app_commands.describe(
        imagem='Imagem do Final da Partida', 
        mapa='Nome do Mapa',
        placar='(Opcional) Placar do jogo no formato X-Y (ex: 13-10). Use se a imagem estiver ruim.',
        status='(Opcional) Status do jogo: win, lose ou draw. Use se a imagem estiver ruim.'
    )
    @app_commands.autocomplete(mapa=map_autocomplete)
    @app_commands.choices(status=[
        app_commands.Choice(name='Vitória', value='win'),
        app_commands.Choice(name='Derrota', value='lose'),
        app_commands.Choice(name='Empate', value='draw')
    ])
    async def save_game(
        self, 
        interaction: discord.Interaction, 
        imagem: discord.Attachment, 
        mapa: str,
        placar: str = None,
        status: str = None
    ):
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

        # Try to analyze the image
        data = await ImageDataLoader(caminho_local).analyse_scoreboard()

        # Use manual parameters if provided, otherwise use image analysis data
        score_final = placar if placar else (data.get('score', '') if data else '')
        status_final = status if status else (data.get('status', '') if data else '')
        
        # Validate that we have the critical data (score and status)
        if not score_final or not status_final:
            missing = []
            if not score_final:
                missing.append('placar')
            if not status_final:
                missing.append('status')
            
            await interaction.followup.send(
                f'❌ Não consegui extrair o **{" e ".join(missing)}** da imagem.\n\n'
                f'Por favor, execute o comando novamente informando manualmente:\n'
                f'• `placar`: formato X-Y (ex: 13-10)\n'
                f'• `status`: escolha Vitória, Derrota ou Empate\n\n'
                f'Exemplo: `/save-game imagem:<arquivo> mapa:{mapa} placar:13-10 status:Vitória`',
                ephemeral=True
            )
            return
        
        # If we didn't get player data from image but have score/status, that's still an issue
        if not data or not data.get('players'):
            await interaction.followup.send(
                '❌ Não consegui extrair os dados dos **jogadores** da imagem.\n'
                'Por favor, tente com uma imagem mais clara ou com melhor resolução.',
                ephemeral=True
            )
            return
        
        # Update data dict with final score and status
        data['score'] = score_final
        data['status'] = status_final

        map_id = MapService().get_id_by_name(mapa)

        if not map_id:
            await interaction.followup.send(
                f'Mapa informado "{mapa}" não consta no sistema.',
                ephemeral=True
            )
            return

        try:
            game = GameMapper.from_dict(data=data, map_id=map_id)
        except ValueError as e:
            await interaction.followup.send(
                f'Erro ao processar dados do jogo: {str(e)}',
                ephemeral=True
            )
            return

        uploaded_image = None
        try:
            with open(caminho_local, 'rb') as f:
                file_bytes = f.read()

            image_service = ImageService()
            uploaded_image = image_service.upload_image(
                file_data=file_bytes,
                original_filename=nome_arquivo,
                content_type=imagem.content_type
            )

            if uploaded_image:
                game.set_image_id(uploaded_image.id)
        except Exception as e:
            print(f"Erro ao fazer upload para MinIO: {e}")

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
        
        saved_count = 0
        skipped_players = []

        for stat in stats:
            player = player_service.get_player_by_nick(stat.player_nick)

            if player:
                stat.fk_player = player.id
                stat.fk_game = game_id
                stat_service.save_stat(stat)
                saved_count += 1
            else:
                # Skip stats for unregistered players
                skipped_players.append(stat.player_nick)

        # Build success message
        message = f'✅ Jogo salvo com sucesso! ID: {game_id}\n'
        message += f'📊 Estatísticas salvas: {saved_count}/{len(stats)} jogadores'
        
        if skipped_players:
            message += f'\n\n⚠️ Jogadores não registrados (estatísticas ignoradas):\n'
            message += '\n'.join([f'• `{nick}`' for nick in skipped_players])
            message += '\n\n💡 Use `/register-player` para cadastrar jogadores antes de salvar jogos.'

        await interaction.followup.send(message, ephemeral=False)

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
