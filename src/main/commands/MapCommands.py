import discord
from discord.ext import commands
from discord import app_commands
from ..service.MapService import MapService


class MapCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.map_service = MapService()

    @app_commands.command(name='create-map', description='Cadastrar novo mapa')
    @app_commands.describe(name='Nome do Mapa', active='Mapa está na rotação ativa?')
    async def create_map(self, interaction: discord.Interaction, name: str, active: bool = True):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            if not name:
                await interaction.followup.send('Nome do mapa é obrigatório.', ephemeral=True)
                return

            self.map_service.create(name, active)
            status = "Ativo" if active else "Inativo"
            await interaction.followup.send(f'Mapa **{name}** cadastrado com sucesso! Status: {status}', ephemeral=False)

        except Exception as e:
            await interaction.followup.send(f'Erro ao cadastrar mapa: {e}', ephemeral=True)

    @app_commands.command(name='list-maps', description='Listar todos os mapas')
    async def list_maps(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            maps = self.map_service.get_all()
            if not maps:
                await interaction.followup.send('Nenhum mapa cadastrado.', ephemeral=True)
                return

            msg = "**Mapas Cadastrados:**\n"
            for m in maps:
                status_icon = "✅" if m.is_active else "❌"
                msg += f"{status_icon} **{m.name}** (ID: {m.id})\n"

            await interaction.followup.send(msg, ephemeral=False)

        except Exception as e:
            await interaction.followup.send(f'Erro ao listar mapas: {e}', ephemeral=True)

    @app_commands.command(name='update-map', description='Atualizar nome de um mapa')
    @app_commands.describe(id='ID do Mapa', new_name='Novo Nome do Mapa')
    async def update_map(self, interaction: discord.Interaction, id: int, new_name: str):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            map_obj = self.map_service.get_by_id(id)
            if not map_obj:
                await interaction.followup.send(f'Mapa com ID {id} não encontrado.', ephemeral=True)
                return

            old_name = map_obj.name
            map_obj.set_name(new_name)
            self.map_service.update(map_obj)

            await interaction.followup.send(f'Mapa ID {id} atualizado: **{old_name}** -> **{new_name}**', ephemeral=False)

        except Exception as e:
            await interaction.followup.send(f'Erro ao atualizar mapa: {e}', ephemeral=True)

    @app_commands.command(name='map-rotation', description='Ligar/Desligar mapa da rotação')
    @app_commands.describe(id='ID do Mapa', active='Ativar (True) ou Desativar (False)')
    async def map_rotation(self, interaction: discord.Interaction, id: int, active: bool):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            map_obj = self.map_service.get_by_id(id)
            if not map_obj:
                await interaction.followup.send(f'Mapa com ID {id} não encontrado.', ephemeral=True)
                return

            map_obj.set_is_active(active)
            self.map_service.update(map_obj)

            status_msg = "Adicionado à rotação" if active else "Removido da rotação"
            await interaction.followup.send(f'Mapa **{map_obj.name}** {status_msg}.', ephemeral=False)

        except Exception as e:
            await interaction.followup.send(f'Erro ao alterar rotação: {e}', ephemeral=True)

    @app_commands.command(name='delete-map', description='Deletar um mapa')
    @app_commands.describe(id='ID do Mapa')
    async def delete_map(self, interaction: discord.Interaction, id: int):
        await interaction.response.defer(thinking=True, ephemeral=False)
        try:
            # Check for dependencies (fk_game) could cause DB error.
            # Letting DB error propagate for now or handle gracefully.
            self.map_service.delete(id)
            await interaction.followup.send(f'Mapa ID {id} deletado com sucesso.', ephemeral=False)
        except Exception as e:
            await interaction.followup.send(f'Erro ao deletar mapa (Verifique se não existem partidas vinculadas): {e}', ephemeral=True)
