from socket import *
import threading
import sys
import pickle

# User Defined
import client_gui
from constants import *
from servercmd import *
from clientcmd import *

SERVER_ADDR = ("", 9000)

# Command Line Arguments
host = str(sys.argv[1])
port = int(sys.argv[2])
username = str(sys.argv[3])

# UDP Socket to connect with server
udp_socket = socket(AF_INET, SOCK_DGRAM)

# Create GUI Variable
view = None

# Initialize Commands Class
cmd = Command(host, port, username)
servecmd = ServerCommands(cmd)
clientcmd = ClientCommands(cmd)

def event_listener(command, username):
  global view
  if command == "REGISTER":
    send_message = servecmd.register_user()
    server = True

  elif command == "QUERY":
    send_message = servecmd.query_user(username)
    server = True

  elif command == "LOGOUT":
    send_message = servecmd.logout_user()
    print(send_message)
    server = True

  # elif command == "CHAT":
  #   chat_window()
  #   peer = True
  #   return

  # elif command == "PING":
  #   data = query_user(username.get())
  #   send_message = ping_user(data)
  #   peer = True

  # elif command == "FRIEND":
  #   data = query_user(username.get())
  #   send_message = befriend_user(data)
  #   peer = True

  # elif command == "REQUEST":
  #   data = query_user(username.get())
  #   send_message = request_profile(data, 1)
  #   peer = True
  if server: 
    udp_socket.sendto(pickle.dumps(send_message), SERVER_ADDR)
    recv_data, addr = udp_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    view.log(data)

  # elif peer: 
  #   response = sendto_peer(data, send_message)
  #   if response[STATUS] == "PROFILE":
  #     root = ET.fromstring(response[3])
  #     tree = ET.ElementTree(root)
  #     tree.write(USERNAME+"/friends/"+response[MESSAGE]+".xml")
  #     response[3] = "FILE"

  #   log(response)


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

  # Create GUI
  view = client_gui.ClientGui(event_listener)
  view.start()