from socket import *
import threading
import sys
import pickle

# User Defined
import client_gui
import constants

SERVER_ADDR = ("", 9000)
# Command Line Arguments
host = str(sys.argv[1])
port = int(sys.argv[2])
username = str(sys.argv[3])

# UDP Socket to connect with server
udp_socket = socket(AF_INET, SOCK_DGRAM)

def peer_listener():
  tcp_socket = socket(AF_INET, SOCK_STREAM)
  tcp_socket.bind((host, port))
  tcp_socket.listen(1024)
  while 1:
    peer_socket, addr = tcp_socket.accept()
    recv_data, addr = peer_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    log(data)


if __name__ == '__main__':

  # Listen for incoming peer connections
  listener = threading.Thread(target = peer_listener)
  listener.start()

  # Initialize Commands Class
  cmd = constants.Command(host, port, username)
  print(cmd.ping)
  # Create GUI
  view = client_gui.ClientGui()
  view.start()