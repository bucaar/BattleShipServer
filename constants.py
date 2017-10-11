import pygame, sys
from pygame.locals import *

NUM_ROWS = 10
NUM_COLS = 10

HIT  = "HIT"
SUNK = "SUNK {}"
MISS = "MISS"

VERTICAL   = "v"
HORIZONTAL = "h"

NOTIFY_DELAY = .02

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
  
  DATA = {" ": {"length": 0, "name": "Ocean"},
          "C": {"length": 5, "name": "Aircraft Carrier"},
          "B": {"length": 4, "name": "Battleship"},
          "S": {"length": 3, "name": "Submarine"},
          "D": {"length": 3, "name": "Destroyer"},
          "P": {"length": 2, "name": "Patrol Boat"}}

class Protocol:
  NAME = "NAME"
  PLACE = "SHIP PLACEMENT"
  SHOOT = "SHOT LOCATION"
  SHOT = "OPPONENT SHOT {},{},{}"
  WIN = "WIN"
  LOSE = "LOSE"
  ERROR = "ERROR {}"
