from board import Board
from constants import *
import time
import json

class Player:
  def __init__(self, sock_info):
    self.board = Board()
    self.opponent = None

    self.connection, self.client_address = sock_info

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
    bytes = self.connection.sendall((msg+"\n").encode("utf-8"))

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
