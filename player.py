from board import Board
import time
import json

class Player:
  def __init__(self, sock_info, identity):
    self.board = Board()
    self.identity = identity
    self.opponent = None
    
    self.connection, self.client_address = sock_info if sock_info else (None, None)
    
    self.name = self.client_address
    self.name = self.listen("NAME")
    
  def get_ship_placements(self):
    data = self.listen("SHIP PLACEMENT")
    return json.loads(data)
  
  def get_shot(self):
    data = self.listen("SHOT LOCATION")
    return json.loads(data)
      
  def notify(self, msg):
    self.connection.sendall((msg+"\r\n").encode("utf-8"))
    time.sleep(.02)
      
  def listen(self, msg):
    self.notify(msg)
    data = self.connection.recv(4096).decode("utf-8").strip()
    
    
    return data
    
  def close(self):
    self.connection.close()
    self.connection = None
