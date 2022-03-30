from datetime import datetime, time
import discord
from discord.ext import commands
from discord import Embed, Member
import asyncio
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import numpy as np


'''Practice Game with random values and questions'''

class Practice(commands.Cog):
    def __init__(self, client):
        self.client = client  

    @commands.command()
    async def start(self, ctx):

        # Make temporary embed: Loading 
        temp_embed = discord.Embed(description=f"Loading your game...", color=16742893)
        temp_embed.set_thumbnail(url=f'https://png.pngtree.com/element_our/20200610/ourlarge/pngtree-confucian-confucius-image_2249173.jpg')
        msg = await ctx.send(embed=temp_embed)

        # Describe game rules
        embed = discord.Embed(title=f'How To Play', description=f"You are the dictator of a country named *Luke's Section*. It is your responsibility to appease to 6 different factions: \
                            Police, Military, People, Opposition, Mafia, and Oligarchs. Failure to do so will lead to you being overthrown and losing the game.\
                            With each turn, you will have to attend to a faction of your choice. Your decision to their request will impact their approval of you, which is represented by emojis.\n\
                            *Note: You cannot attend to the same faction consecutively.*\n\n\
                            Press an emoji reaction under a post to interact with the game. You can do this when you pick the faction to attend to and make a decision on how to respond to a faction's request.\n\n\
                            If you are ready, press the blue check below.", 
                            color=16742893)
        embed.set_thumbnail(url=f'https://1.bp.blogspot.com/-Bde2BR5HKRM/Wbw2O_Jt9TI/AAAAAAAAulg/-QLZm5fFqSMFWePl0wufdazs8shAIeYyQCLcBGAs/s1600/0548016fe53b92b7.jpg')

        # Embed Footer
        embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)

        # Replace temporary embed with real embed 
        await asyncio.sleep(1)
        await msg.edit(embed=embed) 
        await msg.add_reaction("☑️")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['☑️']

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)

            def check_faction(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣']

            if reaction.emoji == '☑️':
                # Get questions from file 
                questions = pd.read_csv("data/actualquestions.csv").sample(frac=1).reset_index(drop=True)
                last_faction = ""

                starting_score = 3
                faction_scores = {
                    "police": starting_score,
                    "military": starting_score,
                    "people": starting_score,
                    "opposition": starting_score,
                    "mafia": starting_score,
                    "oligarchs": starting_score
                }

                phil_scores = {
                    "kongzi": 0,
                    "xunzi": 0,
                    "hanfeizi": 0,
                    "lordshang": 0,
                    "mozi": 0
                }
                first_below_zero = ""
                faction_score_summary = ""
                game_end = False
                timeout_flag = False

                # Calculate the philosopher values
                philosophers = ["KONGZI", "XUNZI", "HANFEIZI", "LORDSHANG", "MOZI"]
                philosopher_formulas = {}
                for phil in philosophers:
                    p = questions[phil]
                    p_min = np.sum(p.where(p < 0))
                    p_max = np.sum(p.where(p > 0))
                    p_range = p_max - p_min
                    p_slope = 1 / p_range
                    p_intercept = 1 - p_max * p_slope
                    philosopher_formulas[phil.lower()] = lambda x: (p_slope * x + p_intercept) * 100

                while True:
                    temp_embed = discord.Embed(description=f"Loading your game...", color=16742893)
                    temp_embed.set_thumbnail(url=f'https://png.pngtree.com/element_our/20200610/ourlarge/pngtree-confucian-confucius-image_2249173.jpg')
                    msgf = await ctx.send(embed=temp_embed)

                    police_score = f"{faction_scores['police']} " + " ".join(['\U0001F694' for _ in range(faction_scores["police"])])
                    military_score = f" {faction_scores['military']} " + " ".join(['\U0001F396' for _ in range(faction_scores["military"])])
                    people_score = f" {faction_scores['people']} " + " ".join(['\U0001F9CD ' for _ in range(faction_scores["people"])])
                    opposition_score = f" {faction_scores['opposition']} " + " ".join(['\U0001F9B9' for _ in range(faction_scores["opposition"])])
                    mafia_score = f" {faction_scores['mafia']} " + " ".join(['\U0001F52B' for _ in range(faction_scores["mafia"])])
                    oligarchs_score = f" {faction_scores['oligarchs']} " + " ".join(['\U0001F4B5' for _ in range(faction_scores["oligarchs"])])

                    faction_score_summary = f"1) Police: {police_score}\n2) Military: {military_score} \n3) People: {people_score} \n4) Opposition: {opposition_score} \n5) Mafia: {mafia_score} \n6) Oligarchs: {oligarchs_score}"

                    # Ask for faction
                    embedf = discord.Embed(title=f'Factions', description=f"**Which faction would you like to address?**\n\n\
                            {faction_score_summary}", color=16742893)
                    embedf.set_thumbnail(url=f'https://1.bp.blogspot.com/-Bde2BR5HKRM/Wbw2O_Jt9TI/AAAAAAAAulg/-QLZm5fFqSMFWePl0wufdazs8shAIeYyQCLcBGAs/s1600/0548016fe53b92b7.jpg')
                    embedf.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)
                    # Replace temporary embed with real embed 
                    await asyncio.sleep(1)
                    await msgf.edit(embed=embedf) 
                    if len(questions.FACTION) == 0:
                        break
                    if last_faction != "police" and len(questions[questions.FACTION == "police"].FACTION): 
                        await msgf.add_reaction("1️⃣")
                    if last_faction != "military" and len(questions[questions.FACTION == "military"].FACTION): 
                        await msgf.add_reaction("2️⃣")
                    if last_faction != "people" and len(questions[questions.FACTION == "people"].FACTION): 
                        await msgf.add_reaction("3️⃣")
                    if last_faction != "opposition" and len(questions[questions.FACTION == "opposition"].FACTION): 
                        await msgf.add_reaction("4️⃣")
                    if last_faction != "mafia" and len(questions[questions.FACTION == "mafia"].FACTION): 
                        await msgf.add_reaction("5️⃣")
                    if last_faction != "oligarchs" and len(questions[questions.FACTION == "oligarchs"].FACTION): 
                        await msgf.add_reaction("6️⃣")

                    faction = ""
                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check_faction)
                        if reaction.emoji == '1️⃣':
                            faction = "police"
                        elif reaction.emoji == '2️⃣':
                            faction = "military"
                        elif reaction.emoji == '3️⃣':
                            faction = "people"
                        elif reaction.emoji == '4️⃣':
                            faction = "opposition"
                        elif reaction.emoji == '5️⃣':
                            faction = "mafia"
                        elif reaction.emoji == '6️⃣':
                            faction = "oligarchs"
                        last_faction = faction

                    except asyncio.TimeoutError: #Indent error here, delete one tabulation
                        timeout_flag = True
                        await ctx.send("No faction chosen") #Also Delete one tabulation here
                        break
                    
                    question = questions[questions.FACTION == faction].iloc[0]
                    questions = questions[questions.SCENARIO != question.SCENARIO]

                    # Send proceeding embed 
                    temp_embed = discord.Embed(description=f"Loading your game...", color=16742893)
                    temp_embed.set_thumbnail(url=f'https://png.pngtree.com/element_our/20200610/ourlarge/pngtree-confucian-confucius-image_2249173.jpg')
                    msg1 = await ctx.send(embed=temp_embed)
                    # Make actual embed
                    embed = discord.Embed(title=f'Request from {question.FACTION}', description=f"{question.SCENARIO}\n\n{question.RESPONSE1} ✅ or {question.RESPONSE2} ❌", color=16742893)
                    embed.set_thumbnail(url=f'https://1.bp.blogspot.com/-Bde2BR5HKRM/Wbw2O_Jt9TI/AAAAAAAAulg/-QLZm5fFqSMFWePl0wufdazs8shAIeYyQCLcBGAs/s1600/0548016fe53b92b7.jpg')

                    # Embed Footer
                    embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)

                    # Replace temporary embed with real embed 
                    await asyncio.sleep(1)
                    await msg1.edit(embed=embed)
                    await msg1.add_reaction("✅")
                    await msg1.add_reaction("❌")

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅','❌']

                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
                        if reaction.emoji == '✅':
                            faction_scores["police"] += question.POLICE
                            faction_scores["military"] += question.MILITARY
                            faction_scores["people"] += question.PEOPLE
                            faction_scores["opposition"] += question.OPPOSITION
                            faction_scores["mafia"] += question.MAFIA
                            faction_scores["oligarchs"] += question.OLIGARCHS
                            phil_scores["kongzi"] += question.KONGZI
                            phil_scores["xunzi"] += question.XUNZI
                            phil_scores["hanfeizi"] += question.HANFEIZI
                            phil_scores["lordshang"] += question.LORDSHANG
                            phil_scores["mozi"] += question.MOZI
                        elif reaction.emoji == '❌':
                            faction_scores["police"] -= question.POLICE
                            faction_scores["military"] -= question.MILITARY
                            faction_scores["people"] -= question.PEOPLE
                            faction_scores["opposition"] -= question.OPPOSITION
                            faction_scores["mafia"] -= question.MAFIA
                            faction_scores["oligarchs"] -= question.OLIGARCHS
                            phil_scores["kongzi"] -= question.KONGZI
                            phil_scores["xunzi"] -= question.XUNZI
                            phil_scores["hanfeizi"] -= question.HANFEIZI
                            phil_scores["lordshang"] -= question.LORDSHANG
                            phil_scores["mozi"] -= question.MOZI

                    except asyncio.TimeoutError: #Indent error here, delete one tabulation
                        await ctx.send("No response chosen") #Also Delete one tabulation here
                        timeout_flag = True
                        break

                    if timeout_flag: break

                    for faction in faction_scores.keys():
                        if faction_scores[faction] <= 0:
                            game_end = True
                            first_below_zero = faction
                            break
                    
                    # Capitalize factions
                    factions = {'police':'Police','military':'Military','people':'People','opposition':'Opposition','mafia':'Mafia','oligarchs':'Oligarchs'}
                    factionUpper = ""
                    for k,v in factions.items():
                        if first_below_zero.lower() == k:
                            factionUpper = v

                    if game_end: break

                if not timeout_flag:
                    police_score = f"{faction_scores['police']} " + " ".join(['\U0001F694' for _ in range(faction_scores["police"])])
                    military_score = f" {faction_scores['military']} " + " ".join(['\U0001F396' for _ in range(faction_scores["military"])])
                    people_score = f" {faction_scores['people']} " + " ".join(['\U0001F9CD ' for _ in range(faction_scores["people"])])
                    opposition_score = f" {faction_scores['opposition']} " + " ".join(['\U0001F9B9' for _ in range(faction_scores["opposition"])])
                    mafia_score = f" {faction_scores['mafia']} " + " ".join(['\U0001F52B' for _ in range(faction_scores["mafia"])])
                    oligarchs_score = f" {faction_scores['oligarchs']} " + " ".join(['\U0001F4B5' for _ in range(faction_scores["oligarchs"])])

                    faction_score_summary = f"1) Police: {police_score}\n2) Military: {military_score} \n3) People: {people_score} \n4) Opposition: {opposition_score} \n5) Mafia: {mafia_score} \n6) Oligarchs: {oligarchs_score}"

                    temp_embed = discord.Embed(description=f"Loading your game...", color=16742893)
                    temp_embed.set_thumbnail(url=f'https://png.pngtree.com/element_our/20200610/ourlarge/pngtree-confucian-confucius-image_2249173.jpg')
                    # msgf = await ctx.send(embed=temp_embed)
                    
                    embedf = discord.Embed(title=f'You were overthrown by the {factionUpper}', description=f"Final score:\n{faction_score_summary}", color=16742893)
                    embedf.set_thumbnail(url=f'https://1.bp.blogspot.com/-Bde2BR5HKRM/Wbw2O_Jt9TI/AAAAAAAAulg/-QLZm5fFqSMFWePl0wufdazs8shAIeYyQCLcBGAs/s1600/0548016fe53b92b7.jpg')


                    # Standard values for graph aesthetics and values 
                    colors = ['#6cace2','#c0964c','#cc708d','#916063','#1eb59b','#888690']
                    bc = '#8b8ba2'

                    philosophers = {'kongzi':'Kongzi','xunzi':'Xunzi','hanfeizi':'Han Feizi','lordshang':'Lord Shang','mozi':'Mozi'}
                    analysis = {'Kongzi': 'Your views revolve around ritual and filial piety. You believe that a government\'s ruler, as long as they behave morally, is justified in their actions as they are granted the Mandate of Heaven.',
                                'Xunzi': 'Your views are similar to Kongzi\'s in that they emphasize ritual and filial piety. In contrast, you place greater emphasis that self-cultivation is attained individually and through persistent endeavor through difficulty.',
                                'Han Feizi': 'While you are a strong believer in a powerful central government, you also believe in the importance of enacting consistent rewards and punishments. You place emphasis on having the rule of law, where the law must be clear and consistent. You also believe in the importance of a ruler keeping their opinions private from the eyes of their subordinates.',
                                'Lord Shang': 'You are a strong proponent of a centralized and militaristic form of government. You place considerable emphasis on empowering the military and having harsh punishments for infractions.',
                                'Mozi': 'Your style of governing is all about universal love. Your choices to rule can be characterized by elements of impartiality and utilitarianism. You want the best for everyone, fairly, and highly value the strength of a state.'}

                    phil_score_normalized = {p: philosopher_formulas[p](s) for p, s in phil_scores.items()}
                    xValuesLower = list(phil_score_normalized.keys())
                    yValues = list(phil_score_normalized.values())

                    # Change philosopher name to proper capitalization/format
                    xValues = []
                    for x in range(len(xValuesLower)):
                        for k,v in philosophers.items():
                            if xValuesLower[x].lower() == k:
                                xValues.append(v)

                    # Get highest philosopher score and names of top philosophers 
                    fin_max = max(yValues)
                    topPhilosophers = []
                    for y in range(len(yValues)):
                        if int(yValues[y]) == int(fin_max):
                            topPhilosophers.append(xValues[y])

                    analysisTop = []
                    # Get highest philosopher's analysis 
                    for t in range(len(topPhilosophers)):
                        for k,v in analysis.items():
                            if topPhilosophers[t] == k:
                                analysisTop.append(v)

                    # Plot and set axis colors 
                    fig, ax = plt.subplots()
                    ax.bar(xValues, yValues, color=colors)
                    ax.spines['bottom'].set_color(bc)
                    ax.spines['top'].set_color(bc) 
                    ax.spines['right'].set_color(bc)
                    ax.spines['left'].set_color(bc)

                    # Label axis 
                    ax.set_xlabel('Philosophers')
                    ax.set_ylabel('Percentage')

                    # Axis color 
                    ax.xaxis.label.set_color(bc)
                    ax.yaxis.label.set_color(bc)

                    # Axis ticks colors 
                    ax.tick_params(axis='x', colors=bc)
                    ax.tick_params(axis='y', colors=bc)

                    # Save graph 
                    plt.savefig('example.png', transparent=True)

                    # Make embed 
                    file = discord.File('example.png',filename='example.png')
                    embedf.set_thumbnail(url=f'https://1.bp.blogspot.com/-Bde2BR5HKRM/Wbw2O_Jt9TI/AAAAAAAAulg/-QLZm5fFqSMFWePl0wufdazs8shAIeYyQCLcBGAs/s1600/0548016fe53b92b7.jpg')
                    embedf.set_image(url='attachment://example.png')
                    
                    # Add embed for philosopher alignment   
                    for x in range(len(xValues)):
                        embedf.add_field(name=f'{xValues[x]}', value = f'{round(yValues[x])}% alignment', inline=True)
                    embedf.add_field(name='\u200B', value='\u200B', inline=True)
                    embedf.add_field(name="Brief Analysis", value=f'You received the highest alignment for the following philosopher(s): {", ".join(str(x) for x in topPhilosophers)}.', inline=False)

                    for x in range(len(analysisTop)):
                        embedf.add_field(name=f'{topPhilosophers[x]}', value=f'{analysisTop[x]}', inline=False)
                    
                    await ctx.send(embed=embedf, file=file)

        except asyncio.TimeoutError: #Indent error here, delete one tabulation
            await ctx.send("Timed out") #Also Delete one tabulation here


def setup(client):
    client.add_cog(Practice(client))