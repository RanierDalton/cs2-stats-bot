import discord
from discord.ext import commands
from discord import app_commands
from .commands.GameCommands import GameCommands

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
        await self.tree.sync() 
        
    async def on_ready(self):
        print(f'Bot {self.user} ligado com sucesso!')