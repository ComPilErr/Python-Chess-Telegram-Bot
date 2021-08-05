import json
import requests
import time
import sys

import subprocess
from uci_puci import UciPuci
from uci_api import UciApi as TelegramApi


def main():

    foo = TelegramApi()

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
                        foo.user_moves[foo.user_id] = UciPuci()

                    if '/log' in msg:
                        foo.send_text("Your moves: " + foo.user_moves.get(foo.user_id).moves)

                    if '/move' in msg:
                        accum_moves = ""
                        answer = ""
                        for _ in range(1,len(msg.split(' '))):
                            accum_moves+=msg.split(' ')[_]+" "
                        foo.user_moves[foo.user_id].move(accum_moves)
                        print("USER moves -> ",foo.user_moves[foo.user_id].moves)
                        answer = foo.user_moves[foo.user_id].process()
                        foo.user_moves[foo.user_id].move(answer + " ")
                        foo.send_text("Your move is: " + answer )
                    foo.last_id+=1
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass


if __name__ == "__main__":
    main()
