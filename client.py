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
ping     = ["PING", "user", "ip", "port"]     # Response => PONG
pong     = ["PONG", "user", "ip", "port"]     # Response => none
friend   = ["FRIEND", ""]                     # Response => CONFIRM
confirm  = ["CONFIRM", USERNAME]              # Response => none
busy     = ["BUSY", USERNAME]                 # Response => none

initial_load = True

##
# Client-Server Commands
##
def register_user(): 
  return register

def query_user(username): 
  query[MESSAGE] = username
  client_socket.sendto(pickle.dumps(query), SERVER_ADDR)
  recv_data, addr = client_socket.recvfrom(1024)
  data = pickle.loads(recv_data) 
  return data

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
def ping_user(user):
  ping[MESSAGE] = user[MESSAGE]
  ping[2] = user[2]
  ping[3] = user[3]
  return ping

def pong_user():
  pong[MESSAGE] = USERNAME
  pong[2] = HOST
  pong[3] = PORT
  return pong

def befriend_user(user):
  data = query_user(user[4])
  if data[0] == "LOCATION": 
    friend[MESSAGE] = data[4]
    return friend
  else: 
    return False

def chat_manager(): 
  print("Opened chat manager choose friend: ") # if friends list friends then query for availability
  # else prompt for friend to be added
  data = query_user(input("username: "))

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
      send_message = ping_user(data)

    elif command == "FRIEND": 
      send_message = befriend_user(data)
      # if not send_message:
      #   down_user(query[MESSAGE])
      #   continue

    else:
      print("command not found")
      continue

    try:  
      s.send(pickle.dumps(send_message))  
    except timeout: 
      down_user(query[MESSAGE])

    recv_data, addr = s.recvfrom(1024)
    data = pickle.loads(recv_data) 
    print(data)

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

    if chatting: 
      client_socket.send(pickle.dumps(busy))
      continue
      
    if data[STATUS] == "PING":
      reply = pong_user()

    elif data[STATUS] == "FRIEND":
      reply = confirm

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
      print(query_user(str(input("username: "))))
      continue

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
