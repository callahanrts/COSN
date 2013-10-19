from socket import *
import time
import sqlite3
import pickle


# Connect to sqlite database and print success message
conn = sqlite3.connect('cosn.db')
print("Opened database successfully")

# Delete records of online users
conn.execute("DELETE FROM online_users")
conn.commit()

#Connect to server and print message 
server_socket = socket(AF_INET, SOCK_DGRAM)  
server_socket.bind(('', 9000))
print("(9000) UDP Server Waiting for client...")

# Wait for connections from clients
while True:
  # Retrieve data from request
  data, address = server_socket.recvfrom(1024)
  request = pickle.loads(data)
  command = request[0]

  # Register Command
  if command == "REGISTER":
    cursor = conn.execute("SELECT * FROM online_users WHERE username = ? LIMIT 1", (request[3],) )
    exists = False
    for row in cursor:
      if row[0]:
        exists = True 
    if exists:
      print("User is already online")
      server_socket.sendto(pickle.dumps(["ACK", row[0], row[1], row[2], row[3]]), address)
    else:
      conn.execute("INSERT INTO online_users(id, ip_address, port, username) VALUES(NULL, ?, ?, ?)", (request[1], request[2], request[3]))
      conn.commit()
      print("User has been registered")
      server_socket.sendto(pickle.dumps(["ACK", request[1], request[2], request[3]]), address)
  
  # Query Command
  elif command == "QUERY":
    cursor = conn.execute("SELECT * FROM online_users WHERE username = ? LIMIT 1", (str(request[1]),))
    exists = False
    for row in cursor:
      if row[0]:
        exists = True 
    if exists:
      print("Query for user " + row[1])
      server_socket.sendto(pickle.dumps(["LOCATION", row[0], row[1], row[2], row[3]]), address)
    else:
      print("User was not found")
      server_socket.sendto(pickle.dumps(["Error", "User was not found"]), address)

  # Logout Command
  elif command == "LOGOUT":
    conn.execute("DELETE FROM online_users WHERE id = ?", request[1])
    server_socket.sendto(pickle.dumps(["User was logged out successully"]), address)
    conn.commit()
    print("User logged out")

  else:
    print("Invalid data from client ( " ,address[0], " " , address[1] , " ): ", command)
