import sys
import subprocess
from random import randint

class UciPuci:

    def __init__(self, moves = ""):
        self.moves = moves
        self.p = subprocess.Popen("../StockFish/src/stockfish",stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        self.p.stdin.write("uci\n")
        self.p.stdin.write("option name Hash type spin default 1 min 1 max 128\n")
        self.p.stdin.write("option name Nullmove type check default true\n")
        self.p.stdin.write("option name Style type combo default Normal var Solid var Normal var Risky\n")
        self.p.stdin.write("setoption name Hash value 32\n")
        self.p.stdin.write("isready\n")

    def __del__(self):
        self.p.terminate()

    def process(self):
        self.p.stdin.write("ucinewgame\n")

        if self.moves is not "":
            self.p.stdin.write("position startpos moves "+self.moves+"\n")
        else:
            self.p.stdin.write("position startpos moves\n")
        self.p.stdin.write("go movetime " + str( randint( 1000 , 3000 ) )+"\n")
        out = ""
        for _ in iter(self.p.stdout.readline,''):
            pass
            if 'bestmove' in _:
                out = _
                break
        return(out.split(' ')[1])

    def move(self, moves):
        self.moves += moves
