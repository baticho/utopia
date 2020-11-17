import scrapy

from scrapy.loader import ItemLoader
from login.items import LoginItem
from scrapy.linkextractors import LinkExtractor



class login(scrapy.Spider):
    name = 'login'
    start_urls = ['https://utopia-game.com/shared/']

    def parse(self, response):
        return scrapy.FormRequest.from_response(response, formdata = {'username': 'lamus', 'password': 'rali'}, callback = self.after_login)  

    def after_login(self, response):

        age = response.xpath("//div[@class='lobby-panel']/h1/a[@href='/wol/chooser/']/text()").get()
        print(age.strip())
        enter = LinkExtractor(restrict_xpaths="//h1/a[@href='/wol/chooser/']")

        pagination_links = enter.extract_links(response)
        yield from response.follow_all(pagination_links, self.after_enter)

    def after_enter(self, response):

        create = response.xpath("//h1/a[@href='/wol/game/throne']/text()").get()
        print(create)

        ranodm_kingdom_page = LinkExtractor(restrict_xpaths="//h1/a[@href='/wol/game/throne']")

        pagination_links = ranodm_kingdom_page.extract_links(response)
        yield from response.follow_all(pagination_links, self.after_ranodm)

    def after_ranodm(self, response):
        item = ItemLoader(item=LoginItem(), response=response)
        item.add_xpath('date', "//div[@class='current-date']/text()")

        item.add_xpath('race', '(//table[@class="two-column-stats"]/tbody/tr/td)[1]/text()')
        item.add_xpath('ruler', '(//table[@class="two-column-stats"]/tbody/tr/td)[3]/text()')
        item.add_xpath('land', '(//table[@class="two-column-stats"]/tbody/tr/td)[5]/text()')
        item.add_xpath('peasants', '(//table[@class="two-column-stats"]/tbody/tr/td)[7]/text()')
        item.add_xpath('building_eff', '(//table[@class="two-column-stats"]/tbody/tr/td)[9]/text()')
        item.add_xpath('money', '(//table[@class="two-column-stats"]/tbody/tr/td)[11]/text()')
        item.add_xpath('food', '(//table[@class="two-column-stats"]/tbody/tr/td)[13]/text()')
        item.add_xpath('runes', '(//table[@class="two-column-stats"]/tbody/tr/td)[15]/text()')
        item.add_xpath('trade_balance', '(//table[@class="two-column-stats"]/tbody/tr/td)[17]/text()')
        item.add_xpath('networth', '(//table[@class="two-column-stats"]/tbody/tr/td)[19]/text()')

        item.add_xpath('soldiers', '(//table[@class="two-column-stats"]/tbody/tr/td)[2]/text()')
        item.add_xpath('off_spec', '(//table[@class="two-column-stats"]/tbody/tr/td)[4]/text()')
        item.add_xpath('def_spec', '(//table[@class="two-column-stats"]/tbody/tr/td)[6]/text()')
        item.add_xpath('elit', '(//table[@class="two-column-stats"]/tbody/tr/td)[8]/text()')
        item.add_xpath('thieves', '(//table[@class="two-column-stats"]/tbody/tr/td)[10]/text()')
        item.add_xpath('wizards', '(//table[@class="two-column-stats"]/tbody/tr/td)[12]/text()')
        item.add_xpath('war_horses', '(//table[@class="two-column-stats"]/tbody/tr/td)[14]/text()')
        item.add_xpath('prisoners', '(//table[@class="two-column-stats"]/tbody/tr/td)[16]/text()')
        item.add_xpath('off_points', '(//table[@class="two-column-stats"]/tbody/tr/td)[18]/text()')
        item.add_xpath('def_points', '(//table[@class="two-column-stats"]/tbody/tr/td)[20]/text()')

        print("Intel")

        return item.load_item()



        

