import json
import requests
import time
import sys
import subprocess

user_moves = dict()

class uci_bot:
    p = 0
    moves = []
    user_id = 0
    params = {}
    headers = {'Content-Type':'application/json'}
    token = "XXX"
    url = "https://api.telegram.org/bot"+token+'/'
    last_id = 0

    def __init__(self):
        self.last_id, self.user_id = self.get_last_id()
        params = {'chat_id':self.user_id}
        self.p = subprocess.Popen("../StockFish/src/stockfish",stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        self.p.stdin.write("uci\n")
        self.p.stdin.write("option name Hash type spin default 1 min 1 max 128\n")
        self.p.stdin.write("option name Nullmove type check default true\n")
        self.p.stdin.write("option name Style type combo default Normal var Solid var Normal var Risky\n")
        self.p.stdin.write("setoption name Hash value 32\n")
        self.p.stdin.write("isready\n")


    def go(self):
        response = requests.get(self.url+'getMe',headers=self.headers)
        return response.json()

    def webhook_get(self):
        response = requests.get(self.url+'getWebhookInfo',headers=self.headers)
        return response.json()


    def send_poll(self,question):
        self.params['chat_id']=user_id
        self.params['question']=question
        self.params['options']={'a':'b','c':'d'}
        response = requests.post(self.url+'sendPoll',headers=self.headers,params=self.params)
        return response.json()


    def send_text(self, msg):
        self.params['chat_id']=user_id
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
        self.params['chat_id'] = user_id
        self.params['offset'] = i
        response = requests.get(self.url+'getUpdates',headers=self.headers,params=self.params)
        for item in response.json()['result']:
            try:
                text = item['message']['text']
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

def process(moves=""):

    foo.p.stdin.write("ucinewgame\n")

    if moves is not "":
        foo.p.stdin.write("position startpos moves "+moves+"\n")
    else:
        foo.p.stdin.write("position startpos moves\n")
    foo.p.stdin.write("go movetime 2000\n")
    out = ""
    for _ in iter(foo.p.stdout.readline,''):
        pass
        if 'bestmove' in _:
            out = _
            break
    return(out.split(' ')[1])

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
                    user_moves[foo.user_id] = ""

                if '/log' in msg:
                    foo.send_text("Your moves: " + user_moves.get(foo.user_id) )

                if '/move' in msg:
                    accum_moves = ""
                    answer = ""
                    for _ in range(1,len(msg.split(' '))):
                        accum_moves+=msg.split(' ')[_]+" "
                    user_moves[foo.user_id] = user_moves.get(foo.user_id) + accum_moves
                    answer = process(user_moves[foo.user_id])
                    user_moves[foo.user_id] = user_moves.get(foo.user_id) + answer + " "
                    foo.send_text("Your move is: " + answer )
                foo.last_id+=1
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        pass
