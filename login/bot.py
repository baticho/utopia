import requests, os, sqlite3 
from bottle import Bottle, response, request as bottle_request


class BotHandlerMixin:  
    BOT_URL = None

    def get_chat_id(self, data):
        """
        Method to extract chat id from telegram request.
        """
        chat_id = data['message']['chat']['id']

        return chat_id

    def get_message(self, data):
        """
        Method to extract message id from telegram request.
        """
        message_text = data['message']['text']

        return message_text

    def send_message(self, prepared_data):
        """
        Prepared data should be json which includes at least `chat_id` and `text`
        """       
        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)


class TelegramBot(BotHandlerMixin, Bottle):  
    _TOKEN_ = 'TOKEN'
    BOT_URL = f'https://api.telegram.org/bot{_TOKEN_}'

    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")

    def runSQL(self, command):
        conn = sqlite3.connect('utopia.db')
        cursor = conn.cursor()
        print(command)
        cursor.execute(f'''select {command} from utopia where id = (select max(id) from utopia)''')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def change_text_message(self, text):
        if 'вакс' in text:
            return 'Бил Гейтс ще ни чипира всички :scream: :scream: :scream:'
        elif 'covid' in text:
            return 'Всички ще умрем :scream: :scream: :scream:'
        elif '- ' in text:
            return 'Хаха'
        elif 'http' in text:
            return 'Това го видях вече.'
        elif 'лекар' in text:
            return 'Ако имаш нужда от лекар, звънни ми.'
        elif 'utopia' in text:
            command = text.split()[1]
            os.system('python start_spider.py')
            try:
                data = self.runSQL(command)
                return f'You have {data[0][0]} {command}'
            except:
                return 'Wrong command'

    def prepare_data_for_answer(self, data):
        message = self.get_message(data)
        answer = self.change_text_message(message)
        chat_id = self.get_chat_id(data)
        json_data = {
            "chat_id": chat_id,
            "text": answer,
        }
        if answer:
            return json_data

    def post_handler(self):
        data = bottle_request.json
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)

        return response


if __name__ == '__main__':  
    app = TelegramBot()
    app.run(host='localhost', port=8080)