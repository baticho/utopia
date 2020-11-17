# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests, sqlite3

class LoginPipeline:


    def telegram_bot_sendtext(self, bot_message):

        bot_token = '155961489:AAHmt5R8zyoQnnoD-kKjY5ZB_9SyfPl8NGc'
        bot_chatID = '67310463' #Bat Icho
        #bot_chatID = '164076275' #Vankata
        #bot_chatID = '175377493' #Bratcgeda
        #bot_chatID = '-1001356679470' #BotId
        #bot_chatID = '955829215' #Petya
        #bot_chatID = '140393291' #Zdravka
        #bot_chatID = '298993355' #Muzzy
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        print(send_text)

        response = requests.get(send_text)
        return response.json()

    def process_item(self, item, spider):
        print(f'Race: {item.get("date")[0]}')

        #test = self.telegram_bot_sendtext(f'Date: {item.get("date")[0]}, Race: {item.get("race")[0]}, Ruler: {item.get("ruler")[0]}')
        #test = self.telegram_bot_sendtext(f'You have {item.get("soldiers")[0]} soldiers and {item.get("peasants")[0]} peasants')
        #print(test)

        return item

class UtopiaPipeline:
	conn = sqlite3.connect('utopia.db')
	cursor = conn.cursor()

	def open_spider(self, spider):
		try:
			self.cursor.execute('''select max(id) from utopia''')
			self.data = self.cursor.fetchall()
		except:
			self.data = [[0]]

	def process_item(self, item, spider):

		self.cursor.execute('''create table if not exists "utopia" (
			id INTEGER PRIMARY KEY,
			date text,
			race text,
			ruler text,
			land text,
			peasants text,
			building_eff text,
			money text,
			food text,
			runes text,
			trade_balance text,
			networth text,
			soldiers text,
			off_spec text,
			def_spec text,
			elit text,
			thieves text,
			wizards text,
			war_horses text,
			prisoners text,
			off_points text,
			def_points text
			) ''')

		date = item['date'][0]

		race = item['race'][0]
		ruler = item['ruler'][0]
		land = item['land'][0]
		peasants = item['peasants'][0]
		building_eff = item['building_eff'][0]
		money = item['money'][0]
		food = item['food'][0]
		runes = item['runes'][0]
		trade_balance = item['trade_balance'][0]
		networth = item['networth'][0]

		soldiers = item['soldiers'][0]
		off_spec = item['off_spec'][0]
		def_spec = item['def_spec'][0]
		elit = item['elit'][0]
		thieves = item['thieves'][0].strip()
		wizards = item['wizards'][0].strip()
		war_horses = item['war_horses'][0]
		prisoners = item['prisoners'][0]
		off_points = item['off_points'][0]
		def_points = item['def_points'][0]

		idd = self.data[0][0]+1

		self.cursor.execute(f"""insert into utopia values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (idd, date, race, ruler, land, peasants, building_eff, money, food, runes, 
			trade_balance, networth, soldiers, off_spec, def_spec, elit, thieves, wizards, war_horses, prisoners, off_points, def_points))

		return item

	def close_spider(self, spider):
		self.conn.commit()
		self.cursor.close()
		self.conn.close()