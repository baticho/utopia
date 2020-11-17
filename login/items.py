# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LoginItem(scrapy.Item):
    date = scrapy.Field()

    race = scrapy.Field()
    ruler = scrapy.Field()
    land = scrapy.Field()
    peasants = scrapy.Field()
    building_eff = scrapy.Field()
    money = scrapy.Field()
    food = scrapy.Field()
    runes = scrapy.Field()
    trade_balance = scrapy.Field()
    networth = scrapy.Field()

    soldiers = scrapy.Field()
    off_spec = scrapy.Field()
    def_spec = scrapy.Field()
    elit = scrapy.Field()
    thieves = scrapy.Field()
    wizards = scrapy.Field()
    war_horses = scrapy.Field()
    prisoners = scrapy.Field()
    off_points = scrapy.Field()
    def_points = scrapy.Field()
    