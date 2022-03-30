from datetime import datetime
import discord
from discord.ext import commands
from discord import Embed, Member

import DiscordUtils

class Template(commands.Cog):
    def __init__(self, client):
        self.client = client   

    @commands.command()
    async def repeat(self, ctx, *args):
        message = ' '.join(map(str, args)) or "Hello ;)"
        author = ctx.author
        await ctx.send(f'{author} sent "{message}"')

def setup(client):
    client.add_cog(Template(client))