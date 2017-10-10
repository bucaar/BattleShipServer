import pygame, sys
from pygame.locals import *

NUM_ROWS = 10
NUM_COLS = 10

TILE_SIZE = 48
SHIP_WIDTH = TILE_SIZE//2
SHIP_PADDING = (TILE_SIZE-SHIP_WIDTH)//2

SCREEN_WIDTH   = TILE_SIZE*3+TILE_SIZE*NUM_ROWS*2
SCREEN_HEIGHT  = TILE_SIZE*2+TILE_SIZE*NUM_COLS
SCREEN_CAPTION = "Battleship!"

HIT  = "HIT"
SUNK = "SUNK"
MISS = "MISS"

HIT_MARK_RADIUS = 6

VERTICAL   = "v"
HORIZONTAL = "h"

ANIMATION_FPS = 30
SHOOT_FPS     = 5
PLACE_FPS     = 2

class Color:
  WHITE      = (255, 255, 255)
  BLACK      = (  0,   0,   0)
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

class ShipState:
  UNPLACED  = 0
  PLACED    = 1

class Tile:
  OCEAN      = " "
  CARRIER    = "C"
  BATTLESHIP = "B"
  SUBMARINE  = "S"
  DESTORYER  = "D"
  PATROL     = "P"
  
  DATA = {" ": {"length": 0, "name": "Ocean",            "color": Color.OCEAN},
          "C": {"length": 5, "name": "Aircraft Carrier", "color": Color.CARRIER},
          "B": {"length": 4, "name": "Battleship",       "color": Color.BATTLESHIP},
          "S": {"length": 3, "name": "Submarine",        "color": Color.SUBMARINE},
          "D": {"length": 3, "name": "Destroyer",        "color": Color.DESTORYER},
          "P": {"length": 2, "name": "Patrol Boat",      "color": Color.PATROL}}

pygame.init()
pygame.display.set_caption(SCREEN_CAPTION)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK  = pygame.time.Clock()

FONT = pygame.font.SysFont(None, TILE_SIZE)
PLAYER_1 = None
PLAYER_2 = None
PLAYER_1_RECT = None
PLAYER_2_RECT = None

