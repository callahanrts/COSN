from array import *
from socket import *
import pickle
import sys
import threading

HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
USERNAME = str(sys.argv[3])

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.bind((HOST, PORT))

# Commands
register = ["REGISTER", HOST, PORT, USERNAME] # Response => ACK
query    = ["QUERY", "1"]                     # Response => LOCATION
logout   = ["LOGOUT", USERNAME]               # Response => none  
ping     = ["PING", ]                         # Response => PONG
pong     = ["PONG", ]                         # Response => none

initial_load = True

def register_user(): 
  client_socket.sendto(pickle.dumps(register), ("localhost",9000))

def query_user(): 
  query[1] = str(input("Enter a username: "))
  client_socket.sendto(pickle.dumps(query), ("localhost",9000))

def logout_user(): 
  client_socket.sendto(pickle.dumps(logout), ("localhost",9000))

def list_commands(): 
  print("REGISTER")
  print("QUERY")
  print("LOGOUT")

def chat(): 
  query[1] = str(input("username: "))
  client_socket.sendto(pickle.dumps(query), ("",9000))

  recv_data, addr = client_socket.recvfrom(1024)
  data = pickle.loads(recv_data) 

  MESSAGE = "Hello, World!"

  s = socket(AF_INET, SOCK_STREAM)
  s.connect((data[2], int(data[3])))
  s.send(pickle.dumps(MESSAGE))

  recv_data, addr = s.recvfrom(1024)

  data = pickle.loads(recv_data) 
  print(data)
  s.close()

def peer_communication_thread(): 
  tcp_socket = socket(AF_INET, SOCK_STREAM)
  tcp_socket.bind((HOST, PORT))
  tcp_socket.listen(1024)

  while 1:
    client_socket, addr = tcp_socket.accept()
    print('Connection address:', addr)

    recv_data, addr = client_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    
    print("received data:", data)
    reply = str(input("reply: "))
    return_message = pickle.dumps(reply)
    client_socket.send(return_message)

    client_socket.close()

def server_communication_thread(): 
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
      chat()
      chat_finished = True

    else:
      print("ERROR: command not recognized")
      continue

    if not chat_finished:
      recv_data, addr = client_socket.recvfrom(1024)
      data = pickle.loads(recv_data) 
      print(data)

  client_socket.close()

server_comm = threading.Thread(target=server_communication_thread)
peer_comm = threading.Thread(target=peer_communication_thread)

server_comm.start()
peer_comm.start()
