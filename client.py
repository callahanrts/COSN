from socket import *
from threading import * 
import sys
import pickle

# User Defined
from client_gui import * 
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

def server_command_handler(command, user):
  global view
  if command == "REGISTER":
    send_message = servecmd.register_user()

  elif command == "QUERY":
    send_message = servecmd.query_user(user)

  elif command == "LOGOUT":
    send_message = servecmd.logout_user()

  view.log(send_udp(send_message))

def send_udp(send_message):
  udp_socket.sendto(pickle.dumps(send_message), SERVER_ADDR)
  recv_data, addr = udp_socket.recvfrom(1024)
  return pickle.loads(recv_data) 

def peer_command_handler(command, user):
  # Create socket to connect with a user
  chat_conn = socket(AF_INET, SOCK_STREAM)  

  if command == "FRIEND":
    send_message = clientcmd.befriend_user(user)

  # if command == "CHAT":
  #   chat_window()
  #   peer = True
  #   return

  # elif command == "PING":
  #   data = query_user(user)
  #   send_message = ping_user(data)
  #   peer = True

  # elif command == "FRIEND":
  #   data = query_user(user)
  #   send_message = befriend_user(data)
  #   peer = True

  # elif command == "REQUEST":
  #   data = query_user(user)
  #   send_message = request_profile(data, 1)
  #   peer = True

#  response = sendto_peer(data, send_message)
  
  # if response[STATUS] == "PROFILE":
  #   root = ET.fromstring(response[3])
  #   tree = ET.ElementTree(root)
  #   tree.write(USERNAME+"/friends/"+response[MESSAGE]+".xml")
  #   response[3] = "FILE"

  #   log(response)

  try: 
    user_data = send_udp(servecmd.query_user(user))
    print(user_data)
    chat_conn.connect((user_data[2], int(user_data[3])))
    chat_conn.send(pickle.dumps(send_message))  
  except: 
    view.log("User is offline")
    #down_user(user)
    return

  recv_data, addr = chat_conn.recvfrom(1024)
  response = pickle.loads(recv_data) 
  chat_conn.close()

def peer_listener():
  tcp_socket = socket(AF_INET, SOCK_STREAM)
  tcp_socket.bind((host, port))
  tcp_socket.listen(1024)
  while 1:
    peer_socket, addr = tcp_socket.accept()
    recv_data, addr = peer_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    view.log(data)
    if data[STATUS] == "FRIEND":
      reply = cmd.confirm

if __name__ == '__main__':
  # Listen for incoming peer connections
  listener = Thread(target = peer_listener)
  listener.start()

  # Create GUI
  view = MainWindow(server_command_handler, peer_command_handler, username)
  view.start()