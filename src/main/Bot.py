import discord
from discord.ext import commands
from .commands.GameCommands import GameCommands
from .commands.StatCommands import StatCommands
from .commands.PlayerCommands import PlayerCommands
from .commands.MapCommands import MapCommands


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True
        intents.guilds = True

        super().__init__(
            command_prefix='$',
            intents=intents
        )

    async def setup_hook(self):
        await self.add_cog(GameCommands(self))
        await self.add_cog(StatCommands(self))
        await self.add_cog(PlayerCommands(self))
        await self.add_cog(MapCommands(self))
        
        print("Sincronizando comandos com o Discord...")
        try:
            synced = await self.tree.sync()
            print(f"✅ {len(synced)} comandos sincronizados com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao sincronizar comandos: {e}")

    async def on_ready(self):
        print(f'Bot {self.user} ligado com sucesso!')
