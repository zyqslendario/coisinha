import asyncio, random, string, json 
from discord.ext import commands, tasks
import re, discord
import subprocess

TOKEN = "token"
PREFIX = "prefix"
CAPTCHA_CHANNEL_id = 

with open('pokemon', 'r', encoding='utf8') as file: 
    pokemon_list = file.read()

client = commands.Bot(command_prefix=PREFIX)
client.remove_command('help')
captcha = True

def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != "\\":
            hint.append(message[i])
    hint_string = "".join(hint)
    hint_replaced = hint_string.replace("_", ".")
    solution = re.findall("^" + hint_replaced + "$", pokemon_list, re.MULTILINE)
    return solution

@client.event
async def on_ready():
    print(f'Auto catcher foi iniciado como: {client.user.name}')
    channel = client.get_channel(CAPTCHA_CHANNEL_id)
    await channel.send("Iniciado com sucesso.")

@client.event 
async def on_message(message): 
     if message.author.id == 854233015475109888 and captcha and message.content.startswith("@Pokétwo#8236 ev m shoot"): 
     await message.channel.send(message.content)
    

@client.event
async def on_message(message):
    global captcha
    if message.author.id == 716390085896962058 and captcha:
            if message.embeds:
                embed_title = message.embeds[0].title
                if 'wild pokémon has appeared!' in embed_title:
                    await asyncio.sleep(1)
                    await message.channel.send('<@716390085896962058> hint')

    if captcha:
        content = message.content
        if 'The pokémon is ' in content:
            if not len(solve(content)):
                print('Pokemon not found.')
            else:
                for i in solve(content):
                    await asyncio.sleep(random.randint(3, 4))
                    await message.channel.send(f'<@716390085896962058> c {i.lower()}')

        elif 'human' in content:
            captcha = False
            channel = client.get_channel(CAPTCHA_CHANNEL_id)
            await channel.send(f"@everyone ``Captcha identificado! n\Após concluir, inicie o auto catcher novamente com o comando`` ```iniciar```` [**CAPTCHA**](https://verify.poketwo.net/captcha/{client.user.id})")

    await client.process_commands(message)

@client.command()
async def iniciar(ctx):
    global captcha
    captcha = True
    await ctx.send("Auto catcher iniciado com sucesso.")

@client.command()
async def parar(ctx):
    global captcha
    captcha = False
    await ctx.send("Auto catcher desativado com sucesso.")

@client.command()
async def falar(ctx, *, text):
    await ctx.send(text)

client.run(TOKEN)
