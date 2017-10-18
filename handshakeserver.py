#!/usr/bin/python3

import threading
import sys
import socket
import json

HANDSHAKE = "HELLO"

# --------------------------------------------------

def main(args):
  #setup the server
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_address = ("0.0.0.0", args["p"])
  sock.bind(server_address)

  sock.listen()

  while True:
    sock_info = sock.accept()
    connection, client_address = sock_info
    bytes = connection.sendall((HANDSHAKE+"\n").encode("utf-8"))
    connection.close()

  #finally close the server
  sock.close()

# --------------------------------------------------

def get_args():
  args = {"p": 4948}
  for i in range(len(sys.argv)):
    if sys.argv[i][0] == "-":
      arg = sys.argv[i+1] if i+1 < len(sys.argv) else ""
      try:
        arg = int(arg)
      except:
        pass
      args[sys.argv[i][1]] = arg
  return args

# --------------------------------------------------

if __name__ == "__main__":
  args = get_args()
  main(args)



