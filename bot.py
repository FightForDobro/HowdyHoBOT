import discord
from discord.ext import commands

from random import randint

import config



bot = commands.Bot(command_prefix='!')


@bot.command()
async def add_new_role(ctx):
    await ctx.message.delete()
    await ctx.author.send('Скинь мне название смайла и название роли через "-"\n'
                          'Например Clang-C')


@bot.event
async def on_ready():
    print('Im Alive!')
    print(config.bot_pic)
    print(f'My name is: {bot.user.name} || My id: {bot.user.id}')


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.guild is None and not message.author.bot:
        messages = await message.channel.history(limit=2).flatten()

        if messages[1].content == 'Скинь мне название смайла и название роли через "-"\nНапример Clang-C':
            emoji_name, role_title = message.content.split('-')

            guild = discord.utils.find(lambda g: 443823271566245888, bot.guilds)
            await guild.create_role(name=role_title, reason='Bot Power', hoist=True,
                                    mentionable=True, colour=discord.Colour.from_rgb(randint(0, 255),
                                                                                     randint(0, 255),
                                                                                     randint(0, 255)))


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id

    role_limit = 5
    emoji_roles = ['Python', 'Java', 'C++', 'C#', 'PHP', 'JavaScript', '1C', 'Kotlin', 'Swift']

    if message_id == 665132823564255233:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: guild_id, bot.guilds)

        if payload.emoji.name == 'CSharp':
            role = discord.utils.get(guild.roles, name='C#')

        elif payload.emoji.name == 'CPP':
            role = discord.utils.get(guild.roles, name='C++')

        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

            if member is not None:

                if len(set(r.name for r in member.roles) & set(emoji_roles)) >= role_limit:
                    await member.send(f'{member.name}, '
                                      f'у тебя уже есть {role_limit} роли убери одну если хочешь получить новую')

                else:
                    await member.add_roles(role)

            else:
                print(f'Member: {member} not found')
        else:
            print(f'Role: {role} not found')


@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id

    if message_id == 665132823564255233:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: guild_id, bot.guilds)

        if payload.emoji.name == 'CSharp':
            role = discord.utils.get(guild.roles, name='C#')

        elif payload.emoji.name == 'CPP':
            role = discord.utils.get(guild.roles, name='C++')

        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

            if member is not None:
                await member.remove_roles(role)

            else:
                print(f'Member: {member} not found')
        else:
            print(f'Role: {role} not found')


bot.run(config.TOKEN, bot=True)
