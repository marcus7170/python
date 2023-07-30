import os
import discord
from discord.ext import tasks, commands
import pymysql



intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True


# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_database = '' #coloque o nome da sua DB

# Configurações do bot

bot = commands.Bot(command_prefix="$", intents=intents)

# Função para realizar o backup do banco de dados
def fazer_backup():
    # Conectar ao banco de dados e criar o arquivo de backup SQL
    db = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # Criar um novo arquivo de backup
    temp_backup_path = f"{db_database}_temp.sql"
    backup_file = open(temp_backup_path, "w")

    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        backup_file.write(f"DROP TABLE IF EXISTS {table_name};\n")
        create_table_query = cursor.execute(f"SHOW CREATE TABLE {table_name}")
        create_table_statement = cursor.fetchone()[1]
        backup_file.write(f"{create_table_statement};\n")

        for row in rows:
            values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in row])
            backup_file.write(f"INSERT INTO {table_name} VALUES ({values});\n")

    backup_file.close()
    cursor.close()
    db.close()

    # Substituir o arquivo de backup antigo pelo novo
    os.replace(temp_backup_path, f"{db_database}.sql")

# Evento de inicialização do bot
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

    # Iniciar a tarefa de backup a cada 10 minutos
    backup_task.start()

# Comando para executar manualmente o backup
@bot.command()
async def backup(ctx):
    fazer_backup()
    backup_file = discord.File(f"{db_database}.sql")
    
    # Criar uma mensagem embutida com uma imagem de tubo
    embed = discord.Embed(title='Backup do banco de dados realizado com sucesso!')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1034352909221117982/1045932531251433472/VERMELHO_E_PRATA.png')
    
    # Enviar a mensagem embutida junto com o arquivo de backup
    await ctx.send(embed=embed, file=backup_file)

# Tarefa agendada para executar o backup a cada 10 minutos
@tasks.loop(minutes=5)
async def backup_task():
    fazer_backup()
    channel = bot.get_channel(SEU_ID)  # ID do canal onde a mensagem será enviada
    backup_file = discord.File(f"{db_database}.sql")
    
    # Criar uma mensagem embutida com uma imagem de tubo
    embed = discord.Embed(title='Backup do banco de dados realizado com sucesso!')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1034352909221117982/1045932531251433472/VERMELHO_E_PRATA.png')
    
    # Enviar a mensagem embutida junto com o arquivo de backup
    await channel.send(embed=embed, file=backup_file)

# Executar o bot
bot.run('Seu Token')
