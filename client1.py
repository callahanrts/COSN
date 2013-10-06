from array import *
from socket import *
import pickle

client_socket = socket(AF_INET, SOCK_DGRAM)  #This creates socket
client_socket.bind(('', 9001))

user = "1" 

# Commands
register = ["REGISTER", user, "", "9001"] # Response => ACK
query    = ["QUERY", "1"]                # Response => LOCATION
logout   = ["LOGOUT", user]

while True:
  command = input("Enter a command: ").upper()
  if command == "REGISTER":
    client_socket.sendto(pickle.dumps(register), ("localhost",9000))

  elif command == "QUERY":
    query[1] = str(input("Enter a user id: "))
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

