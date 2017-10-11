pygame.init()
pygame.display.set_caption(SCREEN_CAPTION)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK  = pygame.time.Clock()

TILE_SIZE = 48
SHIP_WIDTH = TILE_SIZE//2
SHIP_PADDING = (TILE_SIZE-SHIP_WIDTH)//2

SCREEN_WIDTH   = TILE_SIZE*3+TILE_SIZE*NUM_ROWS*2
SCREEN_HEIGHT  = TILE_SIZE*2+TILE_SIZE*NUM_COLS
SCREEN_CAPTION = "Battleship!"

FONT = pygame.font.SysFont(None, TILE_SIZE)
  
PLAYER_1 = None
PLAYER_2 = None
PLAYER_1_RECT = None
PLAYER_2_RECT = None

ANIMATION_FPS = 30
SHOOT_FPS     = 2
PLACE_FPS     = 2

HIT_MARK_RADIUS = 6

def visualize_file():
  with open("output.log") as f:
    lines = f.readlines()
  
  #make sure we can quit whenever
  for event in pygame.event.get():
    if event.type == QUIT:
      pass
      
  #draw the bg
  bg(players)
  
  #TODO: place the ships
  
  #display the ships
  display(players, PLACE_FPS)
  
  #swap the boards
  swap_animation(players, ANIMATION_FPS)
  
  #play shoot animations
  shoot_animation(players, i, shot, ANIMATION_FPS)
  #draw the board
  display(players, SHOOT_FPS)
  
  #end the pygame screens
  pygame.quit()

if __name__ == "__main__":
  visualize_file()
