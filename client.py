from array import *
from socket import *
import pickle
import sys
import threading
import readline

HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
USERNAME = str(sys.argv[3])
SERVER_ADDR = ("", 9000)
STATUS = 0
MESSAGE = 1

client_socket = socket(AF_INET, SOCK_DGRAM)
tcp_socket = socket(AF_INET, SOCK_STREAM)


# Client-Server Command Strings
register = ["REGISTER", HOST, PORT, USERNAME] # Response => ACK
query    = ["QUERY", "1"]                     # Response => LOCATION
logout   = ["LOGOUT", USERNAME]               # Response => none  
down     = ["DOWN", USERNAME]

# P2P Command Strings
ping     = ["PING", "hello"]                  # Response => PONG
pong     = ["PONG", "hello"]                  # Response => none
friend   = ["FRIEND", ""]                     # Response => CONFIRM
confirm  = ["CONFIRM", ""]                    # Response => none

initial_load = True

##
# Client-Server Commands
##
def register_user(): 
  return register

def query_user(): 
  query[MESSAGE] = str(input("username: "))
  return query

def logout_user(): 
  return logout

def down_user(username): # User should not be able to call this manually
  down[MESSAGE] = username
  return down

def list_commands(): 
  print("REGISTER")
  print("QUERY")
  print("LOGOUT")

##
# P2P Commands
##
def ping_user(peer_connection, username):
  try:  
    peer_connection.send(pickle.dumps(ping))  
  except timeouterror: 
    down_user(username)

def pong_user():
  return pong

def befriend_user(peer_connection, username):
  try:  
    peer_connection.send(pickle.dumps(friend))  
  except timeouterror: 
    down_user(username)



def chat_manager(): 
  print("Opened chat manager choose friend: ") # if friends list friends then query for availability
  # else prompt for friend to be added
  query_user()
  recv_data, addr = client_socket.recvfrom(1024)
  data = pickle.loads(recv_data) 
  s = socket(AF_INET, SOCK_STREAM)  
  try: 
    s.connect((data[2], int(data[3])))
  except: 
    print("User is offline")
    down_user(query[MESSAGE])
    chat_manager()
    return

  while True:
    command = input("chat command: ").upper()

    if command == "PING":  
      send_message = ping_user(s, query[MESSAGE])

    elif command == "FRIEND": 
      befriend_user(s, query[MESSAGE])

    else:
      print("command not found")
      continue

    recv_data, addr = s.recvfrom(1024)
    data = pickle.loads(recv_data) 
    print("data")

  s.close()


##
# Connection Threads
##
def peer_communication_thread(): 
  tcp_socket.bind((HOST, PORT))
  tcp_socket.listen(1024)

  while True:
    client_socket, addr = tcp_socket.accept()

    recv_data, addr = client_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    
    if data[STATUS] == "PING":
      reply = pong_user()

    else:
      print("received data:", data[MESSAGE])
      reply = ["OK", str(input("reply: "))]

    return_message = pickle.dumps(reply)
    client_socket.send(return_message)
    client_socket.close()

  tcp_socket.close()

def server_communication_thread(): 
  client_socket.bind((HOST, PORT))
  while True:
    command = input("Enter a command: ").upper()
    if command == "REGISTER":
      send_message = register_user()

    elif command == "QUERY":
      send_message = query_user()

    elif command == "LIST":
      send_message = list_commands()

    elif command == "LOGOUT":
      send_message = logout_user()

    elif command == "CHAT":
      chat_manager()
      break

    else:
      print("ERROR: command not recognized")
      continue

    client_socket.sendto(pickle.dumps(send_message), SERVER_ADDR)

    recv_data, addr = client_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    print(data)

  client_socket.close()

server_comm = threading.Thread(target = server_communication_thread)
peer_comm = threading.Thread(target = peer_communication_thread)

server_comm.start()
peer_comm.start()
