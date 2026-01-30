import discord
from discord.ext import commands
from discord import app_commands

from ..service.PlayerService import PlayerService
from ..service.MapService import MapService
from ..service.StatService import StatService

class StatCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.stat_service = StatService()

    @app_commands.command(name='player-stats', description='Pegar stats de um jogador pelo Nick dele')
    @app_commands.describe(nick='Nick do Jogador')
    async def get_player_stat(self, interaction: discord.Interaction, nick: str): 
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            stats = self.stat_service.get_player_stats(nick)
            
            if not stats:
                await interaction.followup.send(f'Nenhuma estatística encontrada para o jogador **{nick}**.', ephemeral=True)
                return

            embed = discord.Embed(
                title=f"📊 Estatísticas: {stats['nick']}",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Jogos", value=str(stats['games']), inline=True)
            embed.add_field(name="Win Rate", value=f"{stats['win_rate']:.1f}%", inline=True)
            embed.add_field(name="KDA", value=f"{stats['kda']:.2f}", inline=True)
            
            embed.add_field(name="Kills", value=str(stats['kills']), inline=True)
            embed.add_field(name="Deaths", value=str(stats['deaths']), inline=True)
            embed.add_field(name="Assists", value=str(stats['assists']), inline=True)
            
            embed.add_field(name="Headshots", value=str(stats['headshots']), inline=True)
            embed.add_field(name="Dano Total", value=str(stats['damage']), inline=True)

            await interaction.followup.send(embed=embed)

        except Exception as e:
             await interaction.followup.send(f'Erro ao buscar stats: {e}', ephemeral=True)


    @app_commands.command(name='get-all-player-stats', description='Mostra as estatísticas agregadas de TODOS os jogadores.')
    async def get_all_player_stats(self, interaction: discord.Interaction):
        
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            players_stats = self.stat_service.get_all_players_stats()

            if not players_stats:
                 await interaction.followup.send("Nenhum dado encontrado.", ephemeral=True)
                 return

            embed = discord.Embed(
                title="🏆 Ranking de Estatísticas da Comunidade",
                description=f"Top {len(players_stats)} jogadores ranqueados por KDA.",
                color=discord.Color.blue()
            )

            nicks_column = []
            kda_column = []
            winrate_column = []

            for rank, player in enumerate(players_stats[:15]): 
                nicks_column.append(f"#{rank + 1} {player.nick}")
                kda_column.append(player.kda)
                winrate_column.append(player.winrate)

            if nicks_column:
                embed.add_field(name="Jogador", value='\n'.join(nicks_column), inline=True)
                embed.add_field(name="KDA", value='\n'.join(kda_column), inline=True)
                embed.add_field(name="Win Rate", value='\n'.join(winrate_column), inline=True)
                
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f'Erro ao buscar ranking: {e}', ephemeral=True)

    @app_commands.command(name='map-stats', description='Pegar stats detalhados de um mapa')
    @app_commands.describe(mapa='Nome do Mapa')
    async def get_map_stats(self, interaction: discord.Interaction, mapa: str): 
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            stats = self.stat_service.get_map_stats(mapa)
            
            if not stats:
                 await interaction.followup.send(f'Nenhuma estatística encontrada para o mapa **{mapa}**.', ephemeral=True)
                 return

            embed = discord.Embed(
                title=f"🗺️ Estatísticas do Mapa: {stats['name']}",
                color=discord.Color.orange()
            )
            
            embed.add_field(name="Partidas Jogadas", value=str(stats['games']), inline=False)
            
            embed.add_field(name="Vitórias (Allies)", value=str(stats['wins']), inline=True)
            embed.add_field(name="Derrotas (Allies)", value=str(stats['losses']), inline=True)
            embed.add_field(name="Empates", value=str(stats['draws']), inline=True)
            
            embed.add_field(name="Média Rounds (Allies)", value=f"{stats['avg_rounds_won']:.1f}", inline=True)
            embed.add_field(name="Média Rounds (Adversary)", value=f"{stats['avg_rounds_lost']:.1f}", inline=True)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f'Erro ao buscar stats do mapa: {e}', ephemeral=True)

    @app_commands.command(name='get-all-maps-stats', description='Mostra ranking de mapas mais jogados.')
    async def get_all_maps_stats(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            maps_stats = self.stat_service.get_all_maps_stats()
            if not maps_stats:
                await interaction.followup.send("Nenhum dado encontrado.", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="🗺️ Ranking de Mapas",
                description="Mapas ordenados por quantidade de partidas jogadas.",
                color=discord.Color.purple()
            )

            name_col = []
            games_col = []
            winrate_col = []

            for m in maps_stats:
                name_col.append(m['name'])
                games_col.append(str(m['games']))
                
                total_decisive_games = m['wins'] + m['losses'] 
                winrate = (m['wins'] / total_decisive_games * 100) if total_decisive_games > 0 else 0.0
                winrate_col.append(f"{winrate:.1f}%")

            if name_col:
                embed.add_field(name="Mapa", value='\n'.join(name_col), inline=True)
                embed.add_field(name="Jogos", value='\n'.join(games_col), inline=True)
                embed.add_field(name="Win Rate (Allies)", value='\n'.join(winrate_col), inline=True)
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f'Erro ao buscar ranking de mapas: {e}', ephemeral=True)