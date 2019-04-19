#!/usr/bin/env python
# encoding: utf-8

import discord
from discord.ext import commands
from gogdbapi import API
from printer import *

from datetime import datetime
import config


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(bot.user.id)


bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = printer.gen_embed('GOGDB Discord Bot', 'Discord Bot powered by **GOG DataBase**\n\u200b')
    embed.add_field(name='!help', value='Show this message\n\u200b')
    embed.add_field(name='!query [string]',
            value='Query products with [string] in their names on GOG, the result format is as follows: \n\u200b\n**[Product Name]**\n[product id]\n\u200b',
            inline=False)
    embed.add_field(name='!detail [product id]', value='Display product detail\n\u200b', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def query(ctx, args=''):
    if args=='':
        embed = discord.Embed(title='Lack of Args!', description='use **!query [string]**')
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(title="Loading...")
    msg = await ctx.send(embed=embed)

    result = await api.query_products(args)

    embed = printer.query_result(result)

    await msg.edit(embed=embed)


@bot.command()
async def detail(ctx, args=''):
    if args == '':
        embed = discord.Embed(title='Lack of Args!', description='use **!detail [product id]**')
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(title='Loading...')
    msg = await ctx.send(embed=embed)

    result = await api.product_detail(args)

    if len(result) == 0:
        embed = discord.Embed(title='Oops, something wrong, please check product id')
        await msg.edit(embed=embed)
        return

    desc = printer.links_parse(result)
    embed = printer.gen_embed(result['title'], description=desc)
    embed = printer.generic_field(embed, result,
            ['inDevelopment',
                'averageRating',
                'inDevelopment',
                'isAvailableForSale',
                'isPreorder',
                'productType',
                'id',
                'globalReleaseDate'])
    embed = printer.list_field(embed, result,
            ['tags',
                'features',
                'developers',
                'publishers',
                'supportedOS'])
    embed = printer.image_parse(embed, result)
    await msg.edit(embed=embed)


if __name__ == '__main__':
    api = API(config.GOGDBHOST)

    author = Author('')
    footer = Footer('Powered by GOGDB')
    printer = Printer(author, footer)

    bot.run(config.BOTTOKEN)
