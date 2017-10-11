#!/usr/bin/python3

import pygame
from pygame.locals import *
from constants import *
from board import Board
import json

TILE_SIZE = 32
SHIP_WIDTH = TILE_SIZE//2
SHIP_PADDING = (TILE_SIZE-SHIP_WIDTH)//2
HIT_MARK_RADIUS = 6

SCREEN_WIDTH   = TILE_SIZE*3+TILE_SIZE*NUM_ROWS*2
SCREEN_HEIGHT  = TILE_SIZE*2+TILE_SIZE*NUM_COLS
SCREEN_CAPTION = "Battleship!"

pygame.init()
pygame.display.set_caption(SCREEN_CAPTION)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK  = pygame.time.Clock()

FONT = pygame.font.SysFont(None, TILE_SIZE)


# --------------------------------------------------

class Color:
  WHITE      = (255, 255, 255)
  BLACK      = (  0,   0,   0)
  GRAY       = (160, 160, 160)
  RED        = (255,   0,   0)
  BLUE       = (  0,   0, 255)
  
  HIT        = RED
  MISS       = WHITE
  
  OCEAN      = ( 51,  51, 255)
  CARRIER    = (100, 100, 100)
  BATTLESHIP = (125, 125, 125)
  SUBMARINE  = (150, 150, 150)
  DESTORYER  = (175, 175, 175)
  PATROL     = (200, 200, 200)
  
Tile.DATA[" "]["color"] = Color.OCEAN
Tile.DATA["C"]["color"] = Color.CARRIER
Tile.DATA["B"]["color"] = Color.BATTLESHIP
Tile.DATA["S"]["color"] = Color.SUBMARINE
Tile.DATA["D"]["color"] = Color.DESTORYER
Tile.DATA["P"]["color"] = Color.PATROL
  
ANIMATION_FPS = 30
PLACE_FPS     = 2

# --------------------------------------------------

def visualize_file(args):
  with open(args["f"]) as f:
    lines = f.readlines()
    lines = [l.strip() for l in lines]
    
  players = ["" for _ in range(2)]
  boards = [Board() for _ in range(2)]
  
  bg(players)
  draw_boards(boards)
  pygame.display.flip()
  
  for line in lines:
    #make sure we can quit whenever
    for event in pygame.event.get():
      if event.type == QUIT:
        pass
    
    print(line)
    if line[:4] == "NAME":
      i = int(line[5])
      name = line[8:]
      players[i] = name
      bg(players)
      
    elif line[:5] == "PLACE":
      i = int(line[6])
      data = line[9:]
      ships = json.loads(data)
      for s, a in ships.items():
        boards[i].place_ship(a[0], a[1], s, a[2])
        draw_boards(boards)
        pygame.display.flip()
        CLOCK.tick(PLACE_FPS)
      pass
      
    elif line[:5] == "SHOOT":
      i = int(line[6])
      data = line[9:]
      shot = json.loads(data)
      shoot_animation(players, boards, i, shot)
      boards[(i+1)%2].shoot(shot[0], shot[1])
      draw_boards(boards)
      pygame.display.flip()
    elif line[:3] == "WIN":
      pass
  
  #end the pygame screens
  pygame.quit()
  
# --------------------------------------------------
  
def draw_boards(boards):
  #draw the newly placed ships
  for i, b in enumerate(boards):
    direction = 1 if i == 0 else -1
    draw_board(b,
           TILE_SIZE+(TILE_SIZE+TILE_SIZE*NUM_ROWS)*i, 
           TILE_SIZE)
    
# --------------------------------------------------

def draw_board(board, xpos, ypos):
  for x, col in enumerate(board.tiles):
    for y, tile_value in enumerate(col):
      tile_data = Tile.DATA[tile_value]
      
      #draw the empty ocean tile
      rect = (xpos+x*TILE_SIZE, ypos+y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
      pygame.draw.rect(SCREEN, Color.OCEAN, rect, 0)
      pygame.draw.rect(SCREEN, Color.BLACK, rect, 1)
      
      #we need to draw a ship tile here
      if tile_value != Tile.OCEAN:
        rect = [xpos+x*TILE_SIZE+(TILE_SIZE-SHIP_WIDTH)//2, 
                ypos+y*TILE_SIZE+(TILE_SIZE-SHIP_WIDTH)//2, 
                SHIP_WIDTH, 
                SHIP_WIDTH]
        
        #same ship tile to the west, reduce pos increase width
        if x-1 >= 0 and board.tiles[x-1][y] == tile_value:
          rect[0] -= SHIP_PADDING
          rect[2] += SHIP_PADDING
        #same ship tile to the north, reduce pos increase width
        if y-1 >= 0 and board.tiles[x][y-1] == tile_value:
          rect[1] -= SHIP_PADDING
          rect[3] += SHIP_PADDING
        #same ship tile to the east, increase width
        if x+1 < NUM_COLS and board.tiles[x+1][y] == tile_value:
          rect[2] += SHIP_PADDING
        #same ship tile to the south, increase width
        if y+1 < NUM_ROWS and board.tiles[x][y+1] == tile_value:
          rect[3] += SHIP_PADDING
          
        pygame.draw.rect(SCREEN, tile_data["color"], rect, 0)
        
      #has this tile been shot?
      if board.shots[x][y]:
        pos = (xpos+x*TILE_SIZE+TILE_SIZE//2, 
               ypos+y*TILE_SIZE+TILE_SIZE//2)
        #is it water?
        if tile_value == Tile.OCEAN:
          pygame.draw.circle(SCREEN, Color.MISS, pos, HIT_MARK_RADIUS)
        else:
          pygame.draw.circle(SCREEN, Color.HIT,  pos, HIT_MARK_RADIUS)

# --------------------------------------------------

def bg(players):
  #draw the background and ids
  SCREEN.fill(Color.GRAY)
  
  player_1 = FONT.render(players[0], True, Color.RED)
  player_1_rect = player_1.get_rect()
  player_1_rect.centerx = TILE_SIZE+(TILE_SIZE*NUM_ROWS)//2
  player_1_rect.centery = TILE_SIZE//2
  player_2 = FONT.render(players[1], True, Color.BLUE)
  player_2_rect = player_2.get_rect()
  player_2_rect.centerx = TILE_SIZE*2+(TILE_SIZE*NUM_ROWS)+(TILE_SIZE*NUM_ROWS)//2
  player_2_rect.centery = TILE_SIZE//2
  
  SCREEN.blit(player_1, player_1_rect)
  SCREEN.blit(player_2, player_2_rect)

# --------------------------------------------------

def shoot_animation(players, boards, i, shot):
  #get the boards x, y position
  xpos, ypos = TILE_SIZE+(TILE_SIZE+TILE_SIZE*NUM_ROWS)*((i+1)%2), TILE_SIZE

  #the cell were shooting
  x, y = shot

  #the coordinates of the target
  end = (xpos+x*TILE_SIZE+TILE_SIZE//2, 
         ypos+y*TILE_SIZE+TILE_SIZE//2)
  
  #This is where we are starting the shot from
  start = (-HIT_MARK_RADIUS, SCREEN_HEIGHT//2) if i == 0 else (SCREEN_WIDTH+HIT_MARK_RADIUS, SCREEN_HEIGHT//2)
  
  #our lovely animation
  for x in range(ANIMATION_FPS+1):
    percent = x/ANIMATION_FPS
    rad = (-16*percent**2+16*percent+1) * HIT_MARK_RADIUS
    pos = (int((end[0]-start[0])*percent+start[0]), int((end[1]-start[1])*percent+start[1]))
    
    bg(players)
    draw_boards(boards)
    pygame.draw.circle(SCREEN, Color.BLACK, pos, int(rad))
    pygame.display.flip()
    CLOCK.tick(ANIMATION_FPS)

# --------------------------------------------------

def get_args():
  args = {"f": "output.log"}
  for i in range(len(sys.argv)):
    if sys.argv[i][0] == "-":
      arg = sys.argv[i+1] if i+1 < len(sys.argv) else ""
      try:
        arg = int(arg)
      except:
        pass
      args[sys.argv[i][1]] = arg
  return args

if __name__ == "__main__":
  args = get_args()
  visualize_file(args)
