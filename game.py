#!/usr/bin/python3

from constants import *
from board import Board
from player import Player
import random
import socket
import sys
import json

LOG_FILE = "output.log"

# --------------------------------------------------

def main(args):
  global LOG_FILE
  
  running = True
  winner = None
  
  #setup the server
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_address = ("0.0.0.0", args["p"] )
  sock.bind(server_address)
  
  sock.listen()
  
  players = [Player(sock.accept(), i) for i in range(2)]
  
  players[0].opponent = players[1]
  players[1].opponent = players[0]
  
  #get the ship placements
  ship_placements = [p.get_ship_placements() for p in players]
  
  #set up the logging file
  LOG_FILE = "{}VS{}.log".format(players[0].name, players[1].name)
  open(LOG_FILE, "w").close()
  
  log("START {}:{}".format(*server_address))
  
  for i in range(2):
    log("NAME {}: {}".format(i, players[i].name))
    
  for i in range(2):
    log("PLACE {}: {}".format(i, json.dumps(ship_placements[i])))
    
  #place the ships
  for i, p in enumerate(players):
    try:
      placements = ship_placements[i]
      for ship, placement in placements.items():
        p.board.place_ship(placement[0], placement[1], ship, placement[2])
    except Exception as e:
      log("ERROR {}: {}".format(i, e.args[0]))
      p.notify(Protocol.ERROR.format(e.args[0]))
      winner = (i+1)%2
      running = False
      break
  
  while running:
    winner = do_turn(players)
    if winner is not None:
      players[winner].notify(Protocol.WIN)
      players[winner].opponent.notify(Protocol.LOSE)
      running = False

  log("WIN {}".format(winner))
  
  #finally close the server
  sock.close()
  
# --------------------------------------------------
  
def do_turn(players):
  try:
    for i, p in enumerate(players):
      #have the player make their shots until they miss
      while True:
        shot = p.get_shot()
        
        result = p.opponent.board.shoot(shot[0], shot[1])
        p.notify(result)
        p.opponent.notify(Protocol.SHOT.format(shot[0], shot[1], result))
        log("SHOOT {}: {}".format(i, json.dumps(shot)))
        
        #see if we have a winner from this turn
        if len(p.opponent.board.ships_remaining()) == 0:
          return i
        
        if result == MISS:
          break
      
  except Exception as e:
    log("ERROR {}: {}".format(i, e.args[0]))
    p.notify(Protocol.ERROR.format(e.args[0]))
    return (i+1)%2
    
  return None
  
# --------------------------------------------------

def log(msg):
  print(msg)
  print(msg, file=open(LOG_FILE, "a"))
  
# --------------------------------------------------

def get_args():
  args = {"p": 4949}
  for i in range(len(sys.argv)):
    if sys.argv[i][0] == "-":
      arg = sys.argv[i+1] if i+1 < len(sys.argv) else ""
      try:
        arg = int(arg)
      except:
        pass
      args[sys.argv[i][1]] = arg
  return args

# --------------------------------------------------

if __name__ == "__main__":
  args = get_args()
  main(args)
