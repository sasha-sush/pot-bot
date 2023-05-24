import discord
from discord.ext import commands
import asyncio
import argparse
import random
import json
import datetime
import openai

settings = None
with open('settings.json') as file:
    settings = json.load(file)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)
TOKEN = settings["ds-bot-token"]
openai.api_key = settings['openai-api-key']

def datetime_string():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%d.%m.%Y | %H:%M:%S")
    return formatted_datetime

def log(str, time=True):
    if time:
        text = datetime_string() + ' ' + str
    else:
        text = str
    with open('log.txt', 'a') as file:
        file.write(text + '\n')
    print(text)


@bot.listen()
async def on_ready():
    log('', time=False)
    log(f"| Bot is connected as {bot.user} |")
    
    #await msg('testing pesting')

@bot.command(name="ping", aliases=['p'])
async def ping_command(ctx: commands.Context):
    log(f'{ctx.author.name} : ping')

    embed = discord.Embed()
    embed.add_field(name="Latency:", value=f"{bot.latency*1000:.2f} ms")

    await ctx.send('Pong!',embed=embed)
    log(f'Pong! {bot.latency*1000:.2f} ms')

@bot.command(name='echo', aliases=['e'])
async def echo_command(ctx: commands.Context, *, message: str = ' '):
    log(f'{ctx.author.name} : echo {message}')
    await ctx.send(message)

@bot.command(name='percent', aliases=['per'])
async def percent_command(ctx: commands.Context, mention = None, role = None):
    if mention == None or role == None:
        await ctx.send('Ти трошки проїбався в написанні. Правильно `/percent <хто> <ким>`', reference=ctx.message)
        return

    percent = random.randint(0,100)

    log(f'{ctx.author.name} : pecent {mention} {role}')

    if mention == bot.user.mention or mention == 'я' or mention == 'me':
        await ctx.send(f'{ctx.author.mention} на 100% ахуєвший')
    else:
        await ctx.send(f'{mention} на {percent}% {role}', reference=ctx.message)

def vroll_info():
    maps = []
    with open('D:\\Documents\\python\\_bots_shared_data\\val\\maps.txt', 'r') as file:
        text = file.read()
        maps = text.split(' ')
    res = f'''
### /vroll /v
Ролить гравців і карту для кастомних пососалок в гівноранті

`/vroll --players (-p) <хуєсос1> <хуєсос2>..` - ролить із заданим списком гравців
якщо `--players` не вказано, то ролить із останнім набором гравців
`/vroll --only (-o) <карта1> <карта2>..` - ролить із заданим списком карт
`/vroll --except (-e) <карта1> <карта2>..` - ролить із всіма картами окрім заданих
`/vroll --last-maps (-lm)` - ролить із останніми картами
карти можна писати і маленькими буквами
`/vroll --spoilers (-s)` - додає трішечки інтриги
`/vroll --help -h -?` - довідка

доступні карти:
`{' '.join(maps)}`
'''
    return res

def vroll_wishes():
    best_before = ['Знов кастомки в валіку <:pain:1105874915363672135>', 
                   'Знову гівно їсти <:maaan:977133773571375104> ', 
                   'Необучаємі <:VetalPog:1058726207576883220> ',
                   'Вам буде всело до початку першого раунду <:BASED:978357026776301668>']
    best_wishes_after = ['Приємного сосання🍌', 
                         'Обережно не паліть сраки занадто сильно🔥', 
                         'Пам\'ятайте - <@307774926574583808> не має особистого життя🤓',
                         'Розчехляйте сраки 🍑']
    wish_before = random.choice(best_before)
    wish_after = random.choice(best_wishes_after)
    return {'before':wish_before, 'after':wish_after}

def make_strings_equal_length(strings1, strings2):
    max_length = max(
        max(len(string) for string in strings1),
        max(len(string) for string in strings2)
    )

    modified_strings1 = []
    modified_strings2 = []

    for string in strings1:
        if len(string) < max_length:
            modified_string = string + ' ' * (max_length - len(string))
        else:
            modified_string = string
        modified_strings1.append(modified_string)

    for string in strings2:
        if len(string) < max_length:
            modified_string = string + ' ' * (max_length - len(string))
        else:
            modified_string = string
        modified_strings2.append(modified_string)

    return modified_strings1, modified_strings2

@bot.command(name='vroll', 
             aliases=['v'], 
             help='For more info type !vroll --help')
async def vroll_command(ctx: commands.Context, *args):   
    log(f'{ctx.author.name} : vroll') 
    # Створення парсера аргументів
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', '-h', '-?', action='store_true')
    parser.add_argument('--last-maps', '-lm', action='store_true')
    parser.add_argument('--spoilers', '-s', action='store_true')
    parser.add_argument('--players', '-p', nargs='+')
    parser.add_argument('--exc', '-e', nargs='+')
    parser.add_argument('--only', '-o', nargs='+')

    # Розбір аргументів командного рядка
    try:
        args = parser.parse_args(args)
    except SystemExit as e:
        #error_text = f'Шось ти неправильно натикав, запишу тебе в список підарів але поки шо тільки олівцем📝'
        #log('INPUT EXCEPTION')
        #context.bot.send_message(chat_id=message.chat_id, text=error_text, parse_mode='HTML')
        return

    if args.help:
        await ctx.send(vroll_info())
        return
    
    players = []
    val_last_players_file = 'D:\\Documents\\python\\_bots_shared_data\\val\\last_players.txt'
    if args.players:
            players = args.players
            with open(val_last_players_file, 'w') as file:
                file.write(' '.join(players))
    else:
        with open(val_last_players_file, 'r') as file:
            text = file.read()
            players = text.split(' ')

    maps = []
    val_last_maps_file = 'D:\\Documents\\python\\_bots_shared_data\\val\\last_maps.txt'
    if args.last_maps:
        with open(val_last_maps_file, 'r') as file:
            text = file.read()
            maps = text.split(' ')
    else:
        with open('D:\\Documents\\python\\_bots_shared_data\\val\\maps.txt', 'r') as file:
            text = file.read()
            maps = text.split(' ')
        if args.exc:
            except_maps = args.exc
            maps = [element for element in maps if element.lower() not in [em.lower() for em in except_maps]]
        elif args.only:
            only_maps = args.only
            maps = [element for element in maps if element.lower() in [em.lower() for em in only_maps]]

        with open(val_last_maps_file, 'w') as file:
                file.write(' '.join(maps))
    
    wishes = vroll_wishes()

    text_info = f'''
*{wishes['before']}*
**Вибираю із карт**:
`{' '.join(maps)}`
**Хуєсоси**:
`{' '.join(players)}`
для кастомних пососалок
'''

    await ctx.send(text_info, reference=ctx.message)

    rand_map = maps[random.randint(0,len(maps)-1)]
    team_atk = []
    team_def = []
    for i in range(int(len(players)/2)):
        team_def.append(players.pop(random.randint(0,len(players)-1)))
    team_atk = players

    text_team_atk = None
    text_team_def = None

    if args.spoilers:
        rand_map = '||'+rand_map+'||'

        team_atk, team_def = make_strings_equal_length(team_atk, team_def)

        text_team_atk = '\n'.join(['♿️ ||`' + m + '`||' for m in team_atk])
        text_team_def = '\n'.join(['♿️ ||`' + m + '`||' for m in team_def])
    else:
        text_team_atk = '\n'.join(['♿️ *' + m + '*' for m in team_atk])
        text_team_def = '\n'.join(['♿️ *' + m + '*' for m in team_def])

    text_result = f'''
>>> ### 🍆Сосання відбувається на мапі 🏞 __{rand_map}__ 🏞
    
💥**Атакери:**
{text_team_atk}

🛡**Дефендери:**
{text_team_def}

{wishes['after']}'''

    await ctx.send(text_result)

def generate_gpt_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Використання моделі ChatGPT
        prompt=prompt,
        max_tokens=1000,  # Максимальна кількість токенів в відповіді
        temperature=1,  # Параметр, що контролює "творчість" відповідей (від 0 до 1)
        n=1,  # Кількість варіантів відповідей для генерації
        stop=None,  # Рядок, що вказує, коли зупинити генерацію тексту
    )
    return response.choices[0].text.strip()

@bot.command(name='gpt')
async def gpt_command(ctx, *, query=' '):
    if ctx.message.reference:
        query = ctx.message.reference.resolved.content

    log(f'{ctx.author.name} витратив твої безкоштовні долари : gpt {query}') 
    message = await ctx.send(f'*Дай подумати {query}*', reference=ctx.message)

    # Створення окремого завдання (job) для some_task()
    asyncio.create_task(gpt_task(message, query))

async def gpt_task(message, query):
    try:
        response = generate_gpt_response(query)
    except:
        await message.edit(content='Сталася якась хуйня. Я поломався☠️')
        log('ERROR on gpt response')
        return
    log(f'response to {query} : {response}')
    # Зміна повідомлення після виконання задачі
    await message.edit(content='>>> ' + response)

async def msg(msg):
    print('entry')
    channel_id = 1110582353828528182
    server_id = 1110582353828528179
    message = msg

    channel = bot.get_channel(channel_id)
    server = bot.get_guild(server_id)

    print(channel)
    print(server)

    if channel and server:
        target_channel = server.get_channel(channel.id)
        await target_channel.send(message)
    else:
        print("Помилка: неможливо знайти сервер або канал")


bot.run(TOKEN)
