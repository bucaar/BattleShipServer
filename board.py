from constants import *

class Board:
  def __init__(self):
    self.tiles = [[Tile.OCEAN for c in range(NUM_COLS)] for r in range(NUM_ROWS)]
    self.shots = [[False      for c in range(NUM_COLS)] for r in range(NUM_ROWS)]
    self.ships = {Tile.CARRIER    : ShipState.UNPLACED,
                  Tile.BATTLESHIP : ShipState.UNPLACED,
                  Tile.SUBMARINE  : ShipState.UNPLACED,
                  Tile.DESTORYER  : ShipState.UNPLACED,
                  Tile.PATROL     : ShipState.UNPLACED}
  
  # --------------------------------------------------
  
  def place_ship(self, x, y, s, o):
    #validate params
    s = s.upper()
    o = o.lower()
    if s not in self.ships:
      raise Exception("{} is not a valid ship type".format(s))
    if o != VERTICAL and o != HORIZONTAL:
      raise Exception("{} is not a valid orientation".format(o))
      
    #ensure they didn't already place this ship
    if self.ships[s]:
      raise Exception("Ship {} has already been placed".format(Tile.DATA[s]["name"]))
    
    ship = Tile.DATA[s]
    
    #check bounds
    if x < 0 or x + (ship["length"] if o == HORIZONTAL else 0) > NUM_COLS \
        or y < 0 or y + (ship["length"] if o == VERTICAL else 0) > NUM_ROWS:
      raise Exception("({}, {}, {}) is not a valid placement for ship {}".format(x, y, o, ship["name"]))
    
    #keep track of the spaces we need to set so we don't have to recalc them again
    spaces = []
    
    for i in range(ship["length"]):
      #calculate coords
      if o == VERTICAL:
        coords = (x, y+i)
      else:
        coords = (x+i, y)
        
      spaces.append(coords)
        
      #is there something blocking our path?
      if self.tiles[coords[0]][coords[1]] != Tile.OCEAN:
        raise Exception("Cannot place ship ({}, {}, {}, {}), collision at ({}, {})".format(x, y, o, ship["name"], coords[0], coords[1]))
        
    #safe to place by now
    for space in spaces:
      self.tiles[space[0]][space[1]] = s
      
    #note that we placed this ship
    self.ships[s] = ShipState.PLACED
  
  # --------------------------------------------------
  
  def shoot(self, x, y):
    #validate params
    if x < 0 or x > NUM_COLS or y < 0 or y > NUM_ROWS:
      raise Exception("({}, {}) is not a valid location to shoot".format(x, y))
    
    #already shot here
    if self.shots[x][y]:
      raise Exception("({}, {}) has already been shot at".format(x, y))
    
    #count before shot
    remain_before = self.ships_remaining()
    
    #note that we shot here
    self.shots[x][y] = True
    
    #count after shot
    remain_after = self.ships_remaining()
    
    if remain_after != remain_before:
      return SUNK.format(" ".join(s for s in (remain_before - remain_after)))
    if self.tiles[x][y] != Tile.OCEAN:
      return HIT 
    else:
      return MISS
  
  # --------------------------------------------------
  
  def ships_remaining(self):
    #keep track of the unshot ships that we see
    left = set()
    
    for x, col in enumerate(self.tiles):
      for y, tile_value in enumerate(col):
        if tile_value != Tile.OCEAN \
            and tile_value not in left \
            and not self.shots[x][y]:
          left.add(tile_value)
          
    return left
