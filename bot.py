#!/usr/bin/env python
# encoding: utf-8

import discord
from discord.ext import commands
from gogdbapi import API
from printer import *

from datetime import datetime
import config

bot = commands.Bot(command_prefix='!')
api = API(config.GOGDBHOST)
#author = Author('GOGDB Discord Bot')
author = Author('')
footer = Footer('Powered by GOGDB')
printer = Printer(author, footer)


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


bot.run(config.BOTTOKEN)
