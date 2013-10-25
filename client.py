from socket import *
from threading import * 
import sys
import pickle
import logging

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
  # UDP Socket to connect with server
  udp_socket = socket(AF_INET, SOCK_DGRAM)
  udp_socket.sendto(pickle.dumps(send_message), SERVER_ADDR)
  recv_data, addr = udp_socket.recvfrom(1024)
  return pickle.loads(recv_data) 

def send_chat(message):
  view.log(messag)

def peer_command_handler(command, user):
  # Create socket to connect with a user
  chat_conn = socket(AF_INET, SOCK_STREAM)

  user_data = send_udp(servecmd.query_user(user))

  if command == "FRIEND":
    send_message = clientcmd.befriend_user(user)

  elif command == "CHAT":
      # Create Chat GUI
    chat_window = ChatWindow()
    chat_window.initChatMenu(user_data, username, chat_conn)
    #chat_conn.close()
    return

  try:
    chat_conn.connect((user_data[2], int(user_data[3])))
    chat_conn.send(pickle.dumps(send_message)) 
    recv_data, addr = chat_conn.recvfrom(1024)
    response = pickle.loads(recv_data) 
    view.log(response) 
  except:
    logging.exception("hm")
    view.log("User is offline")
    #down_user(username.get())

  chat_conn.close()

def peer_listener():
  tcp_socket = socket(AF_INET, SOCK_STREAM)
  tcp_socket.bind((host, port))
  while 1:
    tcp_socket.listen(1024)

    peer_socket, addr = tcp_socket.accept()
    recv_data, addr = peer_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    view.log(data)

    if data[0] == "FRIEND":
      reply = cmd.confirm

    if data[0] == "CHAT": 
      reply = cmd.delivered

    if reply != None:
      return_message = pickle.dumps(reply)
      peer_socket.send(return_message)

    peer_socket.close()
  
  tcp_socket.close()

if __name__ == '__main__':
  # Listen for incoming peer connections
  listener = Thread(target = peer_listener)
  listener.start()

  # Create GUI
  view = MainWindow(server_command_handler, peer_command_handler, username)
  view.start()