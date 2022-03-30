from datetime import datetime
import discord
from discord.ext import commands
import json
import traceback
import re
import os
from discord import Embed, Member

import asyncio
import urllib

import DiscordUtils

class Samples(commands.Cog):
    def __init__(self, client):
        self.client = client   

    @commands.command()
    async def repeat(self, ctx, *args):
        message = ' '.join(map(str, args)) or "Hello ;)"
        author = ctx.author
        await ctx.send(f'{author} sent "{message}"')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def help(self, ctx):
        await ctx.send('Fuccoffuwu!')

    @commands.command()
    async def pretty(self, ctx, *args):
        # Make temporary embed 
        temp_embed = discord.Embed(description=f"This is a temporary embed...", color=16742893)
        temp_embed.set_thumbnail(url=f'https://png.pngtree.com/element_our/20200610/ourlarge/pngtree-confucian-confucius-image_2249173.jpg')
        msg = await ctx.send(embed=temp_embed)

        # Make completed profile embed 
        embed = discord.Embed(title=f'Embed Title Here', description=f"Embed Description Here", color=16742893)
        embed.set_thumbnail(url=f'https://1.bp.blogspot.com/-Bde2BR5HKRM/Wbw2O_Jt9TI/AAAAAAAAulg/-QLZm5fFqSMFWePl0wufdazs8shAIeYyQCLcBGAs/s1600/0548016fe53b92b7.jpg')
        embed.add_field(name='Field 1 Name', value=f'Field 1 Value')

        # Leave a section blank 
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(name='\u200B', value='\u200B')

        # Embeds for next line 
        embed.add_field(name='Another Field', value = f'Another Value')
        embed.add_field(name='Another Field', value = f'Another Value')
        embed.add_field(name='Another Field', value = f'Another Value')

        # Get user's inputs 
        inputs = list(args)
        inputLength = len(inputs)
        
        # Make new fields based on user's inputs 
        for x in range(len(inputs)):
            embed.add_field(name=f'Input {x+1}', value=f'{inputs[x]}')

        # Fill extra spaces to make row fields even
        if inputLength % 3 > 0:
            extra = inputLength % 3
        for k in range(0, extra):
            embed.add_field(name='\u200B', value='\u200B')

        # Embed Footer
        embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)

        # Replace temporary embed with real embed 
        await asyncio.sleep(1)
        await msg.edit(embed=embed) 



def setup(client):
    client.add_cog(Samples(client))