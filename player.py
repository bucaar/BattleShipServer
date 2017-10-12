from board import Board
from constants import *
import time
import json

class Player:
  def __init__(self, sock_info, identity):
    self.board = Board()
    self.identity = identity
    self.opponent = None
    
    self.connection, self.client_address = sock_info if sock_info else (None, None)
    
    self.name = self.client_address
  
  # --------------------------------------------------
  
  def get_name(self):
    data = self.listen(Protocol.NAME)
    return data
    
  # --------------------------------------------------
  
  def get_ship_placements(self):
    data = self.listen(Protocol.PLACE)
    return json.loads(data)
  
  # --------------------------------------------------
  
  def get_shot(self):
    data = self.listen(Protocol.SHOOT)
    return json.loads(data)
  
  # --------------------------------------------------
      
  def notify(self, msg):
    self.connection.sendall((msg+"\r\n").encode("utf-8"))
  
  # --------------------------------------------------
      
  def listen(self, msg):
    self.notify(msg)
    self.connection.settimeout(SOCKET_TIMEOUT)
    data = self.connection.recv(4096).decode("utf-8").strip()
    self.connection.settimeout(None)
    return data
  
  # --------------------------------------------------
    
  def close(self):
    self.connection.close()
    self.connection = None
