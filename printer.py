#!/usr/bin/env python
# encoding: utf-8

from discord import Embed
from datetime import datetime
import re

class Author:

    def __init__(self, name, url=Embed.Empty, iconurl=Embed.Empty):
        self.__name = name
        self.__url = url
        self.__icon = iconurl

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value


    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value


    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, value):
        self.__icon = value


class Footer:

    def __init__(self, text, icon=Embed.Empty):
        self.__text = text
        self.__icon = icon

    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, value):
        self.__icon = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value


class Printer:

    def __init__(self, author, footer):
        self.__author = author
        self.__footer = footer


    def key2word(self, key):
        return re.sub('([A-Z][A-Za-z0-9])', r' \1', key).title()


    def gen_embed(self, title=Embed.Empty, description=Embed.Empty, color=0x78387b):
        embed = Embed(title=title, description=description, color=color, timestamp=datetime.utcnow())
        embed.set_author(name=self.__author.name, url=self.__author.url, icon_url=self.__author.icon)
        embed.set_footer(text=self.__footer.text, icon_url=self.__footer.icon)
        return embed


    def query_embed(self, dict_data):
        embed = self.gen_embed(title='Query Result',
                description=f"**{dict_data['count']}** productions found")
        if len(dict_data['products']) != 0:
            for prod in dict_data['products']:
                embed.add_field(name=prod['title'], value=str(prod['id']), inline=False)

        return embed


    def detail_embed(self, dict_data):
        desc = self.links_parse(dict_data)
        embed = self.gen_embed(dict_data['title'], desc)

        embed = self.generic_field(embed, dict_data,
                    ['inDevelopment',
                        'averageRating',
                        'inDevelopment',
                        'isAvailableForSale',
                        'isPreorder',
                        'productType',
                        'id',
                        'globalReleaseDate'])
        embed = self.list_field(embed, dict_data,
                    ['tags',
                        'features',
                        'developers',
                        'publishers',
                        'supportedOS'])
        embed = self.image_field(embed, dict_data)
        embed = self.thumb_field(embed, dict_data)

        return embed


    def price_embed(self, price_dict):
        embed = self.gen_embed(price_dict['title'], 'Base Price')

        for p in price_dict['baseprice']:
            embed.add_field(name=p['country'], value=f"{p['price']} {p['currency']}")
        return embed


    def language_embed(self, dict_data):
        embed = self.gen_embed(dict_data['title'], 'Language Support')
        embed = self.thumb_field(embed, dict_data)

        name_dict = dict()
        value_dict = dict()

        for lan in dict_data['localizations']:
            if lan['code'] not in name_dict:
                name_dict[lan['code']] = lan['name']
                value_dict[lan['code']] = f"[{lan['type']}] "
            else:
                value_dict[lan['code']] += f"[{lan['type']}] "

        for key in name_dict:
            embed.add_field(name=name_dict[key], value=value_dict[key])

        return embed


    def generic_field(self, embed, dict_data, only=[], exclude=[]):
        if len(only) != 0:
            for key in dict_data:
                if key in only:
                    embed.add_field(name=self.key2word(key), value=str(dict_data[key]))
        elif len(exclude) != 0:
            for key in dict_data:
                if key not in exclude:
                    embed.add_field(name=self.key2word(key), value=str(dict_data[key]))
        else:
            for key in dict_data:
                embed.add_field(name=self.key2word(key), value=str(dict_data[key]))

        return embed


    def list_field(self, embed, dict_data, list_key=[]):
        if len(list_key) != 0:
            for key in dict_data:
                if key in list_key and isinstance(dict_data[key], list) and len(dict_data[key]) != 0:
                    mdstr = ' | '.join(dict_data[key])
                    embed.add_field(name=self.key2word(key), value=mdstr)

        return embed


    def image_field(self, embed, dict_data):
        img = dict_data.get('image', None)

        if img != None:
            url = img['href']
            formatter = img['formatters']
            img = url.replace('{formatter}', formatter[len(formatter)-1].replace('_2x', ''))
            embed.set_image(url=img)

        return embed


    def thumb_field(self, embed, dict_data):
        boxartimg = dict_data['links'].get('boxArtImage', None)

        if boxartimg != None:
            embed.set_thumbnail(url=boxartimg)

        return embed


    def links_parse(self, dict_data):
        links = dict_data['links']
        store = links.get('store', None)
        forum = links.get('forum', None)
        support = links.get('support', None)

        md_string = ''

        if store != None:
            md_string += f'[[Store]({store})] '
        if forum != None:
            md_string += f'[[Forum]({forum})] '
        if support != None:
            md_string += f'[[Support]({support})] '

        return md_string
