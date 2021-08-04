import json
import requests
import time
import sys

import subprocess
from uci_puci import UciPuci

user_moves = dict()

class uci_bot:

    params = {}
    headers = {'Content-Type':'application/json'}
    token = "XXX"
    url = "https://api.telegram.org/bot"+token+'/'
    last_id = 0

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

foo = uci_bot()

while(True):
    try:
        cur_id, user_id = foo.get_last_id()

        if int(cur_id) > int(foo.last_id):
            for i in range(foo.last_id+1,cur_id+1):
                msg = foo.get_msg_i(i)
                if '/start' in msg:
                    foo.send_text("Ok, chess. Let's play some")
                    foo.send_text("If you play Black - give me White's move ( like that: /move a2a3)")
                    foo.send_text("If you play White - give me your move and Black's move ( like that: /move d2d3 a7a6 )")
                    user_moves[foo.user_id] = UciPuci()

                if '/log' in msg:
                    foo.send_text("Your moves: " + user_moves.get(foo.user_id).moves)

                if '/move' in msg:
                    accum_moves = ""
                    answer = ""
                    for _ in range(1,len(msg.split(' '))):
                        accum_moves+=msg.split(' ')[_]+" "
                    user_moves[foo.user_id].move(accum_moves)
                    print("USER moves -> ",user_moves[foo.user_id].moves)
                    answer = user_moves[foo.user_id].process()
                    user_moves[foo.user_id].move(answer + " ")
                    foo.send_text("Your move is: " + answer )
                foo.last_id+=1
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        pass
