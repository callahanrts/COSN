from array import *
from socket import *
import pickle

client_socket = socket(AF_INET, SOCK_DGRAM)  #This creates socket
client_socket.bind(('', 9001))
client_socket.settimeout(5)

user = "1" 

# Commands
register = ["REGISTER", user, "", "9001"] # Response => ACK
query    = ["QUERY", "1"]                # Response => LOCATION
logout   = ["LOGOUT", user]

while True:
  command = input("Enter a command: ").upper()
  if command == "REGISTER":
    message = register

  elif command == "QUERY":
    query[1] = str(input("Enter a user id: "))
    message = query

  elif command == "LIST":
    print("REGISTER")
    print("QUERY")
    print("LOGOUT")

  elif command == "LOGOUT":
    message = logout

  else:
    print("ERROR: command not recognized")
    continue

  print("Sending request...")
  count = 0
  while True:
    try:      
      client_socket.sendto(pickle.dumps(message), ("localhost",9000))
      recv_data, addr = client_socket.recvfrom(1024)
    except timeout:
      count += 1
      if count == 3:
        print("Server unavailable, please try again later.")
        break
      print("Connection timed out. Sending request again...")
      continue

    data = pickle.loads(recv_data) 
    print(data)
    break
client_socket.close()

