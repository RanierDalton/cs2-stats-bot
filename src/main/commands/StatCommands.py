import discord
from discord.ext import commands
from discord import app_commands

from ..service.PlayerService import PlayerService
from ..service.MapService import MapService
from ..service.StatService import StatService

class StatCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='get-player-stat', description='Pegar stats de um jogador pelo Nick dele')
    @app_commands.describe(nick='Nick do Jogador')
    async def get_player_stat(self, interaction: discord.Interaction, nick: str): 
        await interaction.response.defer(thinking=True, ephemeral=False)
        # TODO - Implementar funcionalidade
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier', 
            ephemeral=False
        )

    @app_commands.command(name='get-all-player-stats', description='Mostra as estatísticas agregadas de TODOS os jogadores.')
    async def get_all_player_stats(self, interaction: discord.Interaction):
        
        await interaction.response.defer(thinking=True, ephemeral=False)
        
        players_stats = StatService().get_all_players_stats()

        embed = discord.Embed(
            title="🏆 Ranking de Estatísticas da Comunidade",
            description=f"Top {len(players_stats)} jogadores ranqueados por KDA.",
            color=discord.Color.blue() # Escolha uma cor vibrante
        )

        nicks_column = []
        kda_column = []
        winrate_column = []

        best_map_column = []
        worse_map_column = []

        for rank, player in enumerate(players_stats[:15]): 
            nicks_column.append(f"#{rank + 1} {player.nick}")
            kda_column.append(player.kda)
            winrate_column.append(player.winrate)
            best_map_column.append(player.best_map)
            worse_map_column.append(player.worse_map)

        if nicks_column:
            embed.add_field(name="Jogador", value='\n'.join(nicks_column), inline=True)
            embed.add_field(name="KDA", value='\n'.join(kda_column), inline=True)
            embed.add_field(name="Win Rate", value='\n'.join(winrate_column), inline=True)
            embed.add_field(name="Melhor Mapa", value='\n'.join(best_map_column), inline=True)
            embed.add_field(name="Pior Mapa", value='\n'.join(worse_map_column), inline=True)
            
        await interaction.followup.send(embed=embed)

    @app_commands.command(name='get-map-stats', description='Pegar stats de um mapa')
    @app_commands.describe(mapa='Nome do Mapa')
    async def get_map_stats(self, interaction: discord.Interaction, mapa: str): 
        await interaction.response.defer(thinking=True, ephemeral=False)
        # TODO - Implementar funcionalidade 
        # TODO - Ver algo sobre listagem de mapas por ui.Select do proprio discord
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier', 
            ephemeral=False
        )

    @app_commands.command(name='get-maps-stats', description='Pegar stats de TODOS os mapas')
    @app_commands.describe()
    async def get_all_maps_stats(self, interaction: discord.Interaction): 
        await interaction.response.defer(thinking=True, ephemeral=False)
        # TODO - Implementar funcionalidade 
        await interaction.followup.send(
            f'Funcionalidade ainda não implementada, fale com o @Ranier', 
            ephemeral=False
        )