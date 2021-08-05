import json
import requests

class UciApi:

    user_moves = dict()
    params = {}
    headers = {'Content-Type':'application/json'}
    token = "XXX"
    url = "https://api.telegram.org/bot"+token+'/'

    def __init__(self):
        self.last_id, self.user_id = self.get_last_id()
        params = {'chat_id':self.user_id}

    def go(self):
        response = requests.get(self.url+'getMe',headers=self.headers)
        return response.json()

    def webhook_get(self):
        response = requests.get(self.url+'getWebhookInfo',headers=self.headers)
        return response.json()


    def send_poll(self,question):
        self.params['chat_id']=self.user_id
        self.params['question']=question
        self.params['options']={'a':'b','c':'d'}
        response = requests.post(self.url+'sendPoll',headers=self.headers,params=self.params)
        return response.json()


    def send_text(self, msg):
        self.params['chat_id']=self.user_id
        self.params['text']=msg
        #print(self.params)
        response = requests.post(self.url+'sendMessage',headers=self.headers,params=self.params)
        return response.json()

    def send_loc(self, la, lo):
        self.params['latitude'] = la
        self.params['longitude'] = lo
        response = requests.post(self.url+'sendLocation',headers=self.headers,params=self.params)

    def get_last_id(self):
        response = requests.get(self.url+'getUpdates',headers=self.headers)
        return (response.json()['result'][-1]['update_id'], response.json()['result'][-1]['message']['chat']['id'])

    def get_msg_i(self, i):
        self.params['offset'] = i
        response = requests.get(self.url+'getUpdates',headers=self.headers,params=self.params)
        for item in response.json()['result']:
            try:
                text = item['message']['text']
                id = item['message']['chat']['id']
                self.user_id = id
                print(text)
                index = item['update_id']
                if int(i) == int(index):
                    return text
            except:
                return "Smile detected!"

    def get_msg(self):
        response = requests.get(self.url+'getUpdates',headers=self.headers,params=self.params)
        for item in response.json()['result']:
            print(json.dumps(item, sort_keys=True, indent=4, separators=(',',': ')))
            try:
                text = item['message']['text']
                index = item['message']['message_id']
                self.moves.append([index,text])
                print(index, text)
            except:
                pass

        return self.moves
