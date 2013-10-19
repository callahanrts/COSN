from array import *
from socket import *
import pickle
import sys

UDP_HOST = sys.argv[1]
UDP_PORT = int(sys.argv[2])
USERNAME = str(sys.argv[3])
print(UDP_HOST)
print(UDP_PORT)
print(USERNAME)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.bind((UDP_HOST, UDP_PORT))


# Commands
register = ["REGISTER", "", "9002", USERNAME] # Response => ACK
query    = ["QUERY", "1"]                # Response => LOCATION
logout   = ["LOGOUT", USERNAME]

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

  else:
    print("ERROR: command not recognized")
    continue

  print("Sending request")
  recv_data, addr = client_socket.recvfrom(1024)
  data = pickle.loads(recv_data) 
  print(data)

client_socket.close()

