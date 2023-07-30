import random
from time import sleep
from discord_webhook import DiscordWebhook
print('\033[1;37;46m=\033[m'*148)
print('')
print(f'\033[1;33m{" Marcus DEV ":-^147}\033[m')
print('                                                         \033[1;36m BRAZILIAN SPORTS LEAGUE (BSL)\033[m')
print('                                                               \033[1;31m '
                '    SORTEADOR')
print('')
print('\033[1;37;46m=\033[m'*148)
print('')
#introdução
print('='*26)
sleep(1)
print('''\033[1;36m Nesse programa vamos fazer o sorteio dos times e jogadores da competição. \033[m''')
webhook = DiscordWebhook(url='Sua Webhook', content= f'\n```prolog\nNesse Programa Vamos Fazer O Sorteio Dos Times E Jogadores Dessa Competição. Com Uma Pequena Contagem Regressiva A Cada 3 Segundos Saberemos Os times E Seus Jogadors, A BSL Deseja Boa Sorte\r```')
response = webhook.execute()
sleep(1)
webhook = DiscordWebhook(url='Sua Webhook', content= f'\n```prolog\nO Sorteio Começa Em 10 Segundos.\r```')
response = webhook.execute()
for x in range(10, 0, -1):
    sleep(1)
    print(x)
    webhook = DiscordWebhook(url='Sua Webhook', content= f'\n```prolog\n{x}\r```')
    response = webhook.execute()
sleep(1)
lista = ['Marcus7170', 'Jrteeixeira', 'GuAmaral', 'Pedro_14', 'RDD-Diogo', '11tales07', 'Fernando23213', 'Kangooswi', 'Teesgo','SccpOz', 'Vinimudo', 'Latreeel', 'Marlon1131', 'Deco', 'Rodri', 'JeeeffiiN']
times = ['Man. City', 'PSG', 'Real Madrid', 'Chelsea', 'Liverpool', 'Bayern', 'Barcelona', 'Inter', 'Atlético de Madrid', 'Man. United', 'Juventus', 'Tottenham', 'Borussia', 'RB Leipzig', 'AC Milan', 'Arsenal']
for i in range(len(lista)):
    sorteado = random.choice(times)
    sorteado2 = random.choice(lista)

    lista.remove(sorteado2)
    times.remove(sorteado)
    print(f'Jogadores a serem sorteados \033[1;31m{lista}\033[m')
    print(f'Times a serem sorteados \033[1;33m{times}\033[m')
    print(f'\033[1;36m O JOGADOR SORTEADO FOI\033[1;33m {sorteado2}\033[1;31m  E O SEU TIME É \033[1;33m{sorteado}\033[m')

    webhook = DiscordWebhook(url='Sua Webhook', content= f'\n||---------------------------------------------------------------------||\n***BRAZILIAN SPORTS LEAGUE (BSL)***\n<@202238690536325120> ||***SORTEIOU***|| @here ```prolog\nO Jogador --> {sorteado2} <-- Foi Sorteado Para Jogar Com O Time --> {sorteado} <-- \nJogadores Ainda Não Sorteados {lista}\nTimes Ainda Não Sorteados {times}\r```')
    response = webhook.execute()
    for c in range(3, 0, -1):
        sleep(1)
        print(c)
        webhook = DiscordWebhook(url='Sua Webhook', content= f'\n```prolog\n{c}\r```')
        response = webhook.execute()
webhook = DiscordWebhook(url='Sua Webhook', content= f'\n```prolog\nSorteio Realizado Pela Equipe BSL.\r``` `Escravos do JUNIN :D` ')
response = webhook.execute()
