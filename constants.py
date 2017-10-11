import pygame, sys
from pygame.locals import *

NUM_ROWS = 10
NUM_COLS = 10

HIT  = "HIT"
SUNK = "SUNK"
MISS = "MISS"

VERTICAL   = "v"
HORIZONTAL = "h"

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




