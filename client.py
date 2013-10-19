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
logout   = ["LOGOUT", USERNAME]
ping     = ["PING", ]                         # Response => PONG
pong     = ["PONG", ]

initial_load = True

while True:
  command = input("Enter a command: ").upper()
  if command == "REGISTER" or initial_load:
    client_socket.sendto(pickle.dumps(register), ("localhost",9000))
    initial_load = False

  elif command == "QUERY":
    query[1] = str(input("Enter a username: "))
    client_socket.sendto(pickle.dumps(query), ("localhost",9000))

  elif command == "LIST":
    print("REGISTER")
    print("QUERY")
    print("LOGOUT")

  elif command == "LOGOUT":
    client_socket.sendto(pickle.dumps(logout), ("localhost",9000))

  elif command == "CHAT":
    #listen_for_friends(input("CONNECT or WAIT: ").upper())
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind((HOST, PORT))
    tcp_socket.listen(1024)
 
    while 1:
      socket, addr = tcp_socket.accept()
      print('Connection address:', addr)

      recv_data, addr = socket.recvfrom(1024)
      data = pickle.loads(recv_data) 
      
      print("received data:", data)
      return_message = pickle.dumps("GOT IT")
      socket.send(return_message)

      socket.close()


  else:
    print("ERROR: command not recognized")
    continue

  print("Sending request")
  recv_data, addr = client_socket.recvfrom(1024)
  data = pickle.loads(recv_data) 
  print(data)

client_socket.close()
