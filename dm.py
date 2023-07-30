import discord
from discord.ext import commands



intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def pv(ctx, *, msg: str):
    await ctx.message.delete() # Deleta a mensagem do autor
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Você precisa ter permissão de administrador para executar esse comando.")
        return
    count = 0
    for member in ctx.guild.members:
        try:
            await member.send(msg)
            count += 1
        except discord.Forbidden:
            pass
        except:
            pass
    await ctx.send(f'{count} mensagens enviadas!')

#!pv live hoje aqui --> https://www.twitch.tv/lmsmrgamer

@bot.event
async def on_ready():
    activity = discord.Activity(name='Desenvolvido por Marcus7170', type=discord.ActivityType.playing)
    await bot.change_presence(activity=discord.Streaming(name='Assista o Corujão', url='https://www.twitch.tv/lmsmrgamer'))
    
# Inicialização do bot    
bot.run("Seu Token")
