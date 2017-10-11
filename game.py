#!/usr/bin/python3

import pygame
from pygame.locals import *
from constants import *
from board import Board
import random
import socket
import sys
import json
import time

# --------------------------------------------------

def main():
  running = True
  winner = None
  
  #set up the logging file
  open("output.log", "w").close()
  
  #setup the server
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_address = ("localhost", 4949 )
  log("START {}:{}".format(*server_address))
  sock.bind(server_address)
  
  sock.listen()
  
  players = [Player(sock.accept(), i) for i in range(2)]
  
  players[0].opponent = players[1]
  players[1].opponent = players[0]
  
  for i in range(2):
    log("NAME {}: {}".format(i, players[i].name))
  
  if VISUALIZE:
    #draw the bg
    bg(players)
  
  #get the ship placements
  ship_placements = [p.get_ship_placements() for p in players]
  
  #place the ships
  for i, p in enumerate(players):
    try:
      placements = ship_placements[i]
      for ship, placement in placements.items():
        p.board.place_ship(placement[0], placement[1], ship, placement[2])
        if VISUALIZE:
          display(players, PLACE_FPS)
    except Exception as e:
      log("ERROR {}: {}".format(i, e.args[0]))
      p.notify("ERROR {}".format(e.args[0]))
      winner = (i+1)%2
      running = False
      break
  
  #if someone hasn't lost yet
  if running:
    if VISUALIZE:
      #draw the newly placed ships
      display(players, PLACE_FPS)
    
      #swap the boards
      swap_animation(players, ANIMATION_FPS)
  
  while running:
    if VISUALIZE:
      for event in pygame.event.get():
        if event.type == QUIT:
          running = False

    winner = do_turn(players)
    if winner is not None:
      players[winner].notify("WIN")
      players[winner].opponent.notify("LOSE")
      running = False

  log("WIN {}".format(winner))
  
  if VISUALIZE:
    waiting = True
    while waiting:
      for event in pygame.event.get():
        if event.type == QUIT:
          waiting = False
      CLOCK.tick(15)
  
  if VISUALIZE:
    pygame.quit()
    sock.close()
  
def do_turn(players):
  try:
    for i, p in enumerate(players):
      #have the player make their shots until they miss
      while True:
        shot = p.get_shot()
        
        if VISUALIZE:
          shoot_animation(players, i, shot, ANIMATION_FPS)
        
        result = p.board.shoot(shot[0], shot[1])
        p.notify(result)
        p.opponent.notify("OPPONENT SHOT {},{},{}".format(shot[0], shot[1], result))
        
        if VISUALIZE:
          #draw the board
          display(players, SHOOT_FPS)
      
        #see if we have a winner from this turn
        if p.board.ships_remaining() == 0:
          return i
        
        if result == MISS:
          break
      
  except Exception as e:
    log("ERROR {}: {}".format(i, e.args[0]))
    p.notify("ERROR {}".format(e.args[0]))
    return (i+1)%2
    
  return None
  
def display(players, fps, offset=0):
  if not VISUALIZE:
    return
  #draw the newly placed ships
  for i, p in enumerate(players):
    direction = 1 if i == 0 else -1
    p.board.draw(TILE_SIZE+(TILE_SIZE+TILE_SIZE*NUM_ROWS)*i+(TILE_SIZE+TILE_SIZE*NUM_ROWS)*offset*direction, TILE_SIZE)
  if fps > 0:
    pygame.display.flip()
    CLOCK.tick(fps)
  
def bg(players):
  if not VISUALIZE:
    return
  global PLAYER_1, PLAYER_1_RECT, PLAYER_2, PLAYER_2_RECT
  
  #draw the background and ids
  SCREEN.fill(Color.WHITE)
  if PLAYER_1 is None:
    PLAYER_1 = FONT.render(players[0].name, True, Color.RED)
    PLAYER_1_RECT = PLAYER_1.get_rect()
    PLAYER_1_RECT.centerx = TILE_SIZE+(TILE_SIZE*NUM_ROWS)//2
    PLAYER_1_RECT.centery = TILE_SIZE//2
  if PLAYER_2 is None:
    PLAYER_2 = FONT.render(players[1].name, True, Color.BLUE)
    PLAYER_2_RECT = PLAYER_2.get_rect()
    PLAYER_2_RECT.centerx = TILE_SIZE*2+(TILE_SIZE*NUM_ROWS)+(TILE_SIZE*NUM_ROWS)//2
    PLAYER_2_RECT.centery = TILE_SIZE//2
  
  
  SCREEN.blit(PLAYER_1, PLAYER_1_RECT)
  SCREEN.blit(PLAYER_2, PLAYER_2_RECT)

def shoot_animation(players, i, shot, fps):
  if not VISUALIZE:
    return
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
    CLOCK.tick(15)

  #get the boards x, y position
  xpos, ypos = TILE_SIZE+(TILE_SIZE+TILE_SIZE*NUM_ROWS)*i, TILE_SIZE

  #the cell were shooting
  x, y = shot

  #the coordinates of the target
  end = (xpos+x*TILE_SIZE+TILE_SIZE//2, 
         ypos+y*TILE_SIZE+TILE_SIZE//2)
  
  #This is where we are starting the shot from
  start = (-HIT_MARK_RADIUS, SCREEN_HEIGHT//2) if i == 1 else (SCREEN_WIDTH+HIT_MARK_RADIUS, SCREEN_HEIGHT//2)
  
  #our lovely animation
  for x in range(fps+1):
    percent = x/fps
    rad = (-12*percent**2+12*percent+1) * HIT_MARK_RADIUS
    pos = (int((end[0]-start[0])*percent+start[0]), int((end[1]-start[1])*percent+start[1]))
    
    bg(players)
    display(players, 0)
    pygame.draw.circle(SCREEN, Color.BLACK, pos, int(rad))
    pygame.display.flip()
    CLOCK.tick(fps)
 
  #refresh the view now we are done   
  bg(players)
  display(players, fps)

def swap_animation(players, fps):
  if not VISUALIZE:
    return
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
    CLOCK.tick(15)
  #our beautiful animation
  for x in range(fps):
    bg(players)
    display(players, fps, offset=x/fps)
  
  #swap the boards
  players[0].board, players[1].board = players[1].board, players[0].board
  
  #refresh the view now we are done
  bg(players)
  display(players, fps)
      
# --------------------------------------------------

class Player:
  def __init__(self, sock_info, identity):
    self.board = Board()
    self.identity = identity
    self.opponent = None
    self.connection, self.client_address = sock_info
    self.name = self.client_address
    self.name = self.listen("NAME")
  
  def get_ship_placements(self):
    data = self.listen("SHIP PLACEMENT")
    return json.loads(data)
  
  def get_shot(self):
    data = self.listen("SHOT LOCATION")
    return json.loads(data)
      
  def notify(self, msg):
    log("SERVER {}: {}".format(self.identity, msg))
    self.connection.sendall((msg+"\r\n").encode("utf-8"))
    time.sleep(.02)
      
  def listen(self, msg):
    self.notify(msg)
    data = self.connection.recv(4096).decode("utf-8").strip()
    log("PLAYER {}: {}".format(self.identity, data))
    
    return data
    
  def close(self):
    self.connection.close()
  
# --------------------------------------------------

def log(msg):
  print(msg)
  print(msg, file=open("output.log", "a"))

if __name__ == "__main__":
  main()
