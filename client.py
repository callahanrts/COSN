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


# Commands
register = ["REGISTER", HOST, PORT, USERNAME] # Response => ACK
query    = ["QUERY", "1"]                     # Response => LOCATION
logout   = ["LOGOUT", USERNAME]               # Response => none  
ping     = ["PING", "hello"]                  # Response => PONG
pong     = ["PONG", "hello"]                  # Response => none

initial_load = True

##
# Client-Server Commands
##
def register_user(): 
  client_socket.sendto(pickle.dumps(register), SERVER_ADDR)

def query_user(): 
  query[1] = str(input("username: "))
  client_socket.sendto(pickle.dumps(query), SERVER_ADDR)

def logout_user(): 
  client_socket.sendto(pickle.dumps(logout), SERVER_ADDR)

def list_commands(): 
  print("REGISTER")
  print("QUERY")
  print("LOGOUT")

##
# P2P Commands
##
def ping_user():
  pong[MESSAGE] = "User available"
  return pong

def pong_response(): 

def chat_manager(): 
  query()

  recv_data, addr = client_socket.recvfrom(1024)
  data = pickle.loads(recv_data) 

  s = socket(AF_INET, SOCK_STREAM)
  s.connect((data[2], int(data[3])))
  s.send(pickle.dumps(ping)

  recv_data, addr = s.recvfrom(1024)

  data = pickle.loads(recv_data) 
  print(data)
  s.close()

def peer_communication_thread(): 
  tcp_socket.bind((HOST, PORT))
  tcp_socket.listen(1024)

  while True:
    client_socket, addr = tcp_socket.accept()

    recv_data, addr = client_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    
    if data[STATUS] == "PING":
      reply = ping_user()

    else:
      print("received data:", data[MESSAGE])
      reply = ["OK", str(input("reply: "))]

    return_message = pickle.dumps(reply)
    client_socket.send(return_message)

    client_socket.close()

def server_communication_thread(): 
  client_socket.bind((HOST, PORT))
  while True:
    command = input("Enter a command: ").upper()
    if command == "REGISTER":
      register_user()

    elif command == "QUERY":
      query_user()

    elif command == "LIST":
      list_commands()

    elif command == "LOGOUT":
      logout_user()

    elif command == "CHAT":
      chat_manager()
      break

    else:
      print("ERROR: command not recognized")
      continue

    recv_data, addr = client_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    print(data)

  client_socket.close()

server_comm = threading.Thread(target = server_communication_thread)
peer_comm = threading.Thread(target = peer_communication_thread)

server_comm.start()
peer_comm.start()
