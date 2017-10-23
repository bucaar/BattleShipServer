#!/usr/bin/python3

from constants import *
from board import Board
from player import Player
import threading
import datetime
import random
import socket
import sys
import json
import time
import queue

# --------------------------------------------------

def main(args):
  #setup the server
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_address = ("0.0.0.0", args["p"])
  sock.bind(server_address)

  sock.listen()

  player_queue = queue.Queue()

  pt = threading.Thread(target=accept_players, args=(player_queue,sock))
  pt.start()

  while True:
    #limit the number of threads
    while threading.active_count() > 7:
      time.sleep(.5)

    #if we have enough connections,
    if player_queue.qsize() >= 2:
      p1 = player_queue.get()
      p2 = player_queue.get()
      p1.opponent = p2
      p2.opponent = p1

      players = [p1, p2]

      print("Game with {}".format([p.name for p in players]))

      #play the game in a new thread
      gt = threading.Thread(target=game, args=(players,))
      gt.start()

  #finally close the server
  sock.close()

# --------------------------------------------------

def accept_players(player_queue, sock):
  while True:
    player = Player(sock.accept())
    player_queue.put(player)
    print("Connection from {}".format(player.name))

    log("{}: Connection from {}".format(datetime.datetime.now().strftime("%m/%d %I:%M:%S %p"), player.name), "logs/connections.log")

# --------------------------------------------------

def game(players):

  #get the names for the players
  for i, p in enumerate(players):
    try:
      new_name = p.get_name()
      log("{} -> {}".format(p.name, new_name), "logs/connections.log")
      p.name = new_name
    except Exception as e:
      log("ERROR {}: {}".format(p.name, e.args[0]), "logs/connections.log")
      p.notify(Protocol.ERROR.format(e.args[0]))
      return

  #set up the logging file
  log_file = "logs/{}VS{}.log".format(players[0].name, players[1].name)
  with open(log_file, "w"): pass
  log("Create log file {}".format(log_file), "logs/connections.log")

  #output the names of the players
  for i in range(2):
    log("NAME {}: {}".format(i, players[i].name), log_file)

  #start the game, return the winner
  winner = start(players, log_file)

  players[winner].notify(Protocol.WIN)
  players[winner].opponent.notify(Protocol.LOSE)

  log("WIN {}".format(winner), log_file)
  log("{} > {}".format(players[winner].name, players[winner].opponent.name), "logs/results.log")

# --------------------------------------------------

def start(players, log_file):
  #get the ship placements
  ship_placements = []
  for i, p in enumerate(players):
    try:
      ship_placements.append(p.get_ship_placements())
    except Exception as e:
      log("ERROR {}: {}".format(i, e.args[0]), log_file)
      p.notify(Protocol.ERROR.format(e.args[0]))
      return (i+1)%2

  #output the ship placements for the players
  for i in range(2):
    log("PLACE {}: {}".format(i, json.dumps(ship_placements[i])), log_file)

  #place the ships
  for i, p in enumerate(players):
    try:
      placements = ship_placements[i]
      if len(placements) == 0:
        raise Exception("You must place your ships on the board")

      for ship, placement in placements.items():
        p.board.place_ship(placement[0], placement[1], ship, placement[2])
    except Exception as e:
      log("ERROR {}: {}".format(i, e.args[0]), log_file)
      p.notify(Protocol.ERROR.format(e.args[0]))
      return (i+1)%2

  while True:
    winner = do_turn(players, log_file)
    if winner is not None:
      return winner

# --------------------------------------------------

def do_turn(players, log_file):
  try:
    for i, p in enumerate(players):
      #have the player make their shots until they miss
      while True:
        shot = p.get_shot()

        result = p.opponent.board.shoot(shot[0], shot[1])
        p.notify(result)
        p.opponent.notify(Protocol.SHOT.format(shot[0], shot[1], result))
        log("SHOOT {}: {}".format(i, json.dumps(shot)), log_file)

        #see if we have a winner from this turn
        if len(p.opponent.board.ships_remaining()) == 0:
          return i

        if not CONTINUE_AFTER_HIT or result == MISS:
          break

  except Exception as e:
    log("ERROR {}: {}".format(i, e.args[0]), log_file)
    p.notify(Protocol.ERROR.format(e.args[0]))
    return (i+1)%2

  return None

# --------------------------------------------------

def log(msg, log_file):
  print(msg, file=open(log_file, "a"))
  #print("write {} to {}".format(msg, log_file))
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
