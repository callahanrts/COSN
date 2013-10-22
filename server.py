from socket import *
import time
import pickle
import threading
import server_functions
import server_gui
import sqlite3

#Connect to server and print message 
server_socket = socket(AF_INET, SOCK_DGRAM)  
server_socket.bind(('', 9000))
print("(9000) UDP Server Waiting for client...")

def probe_server():
  # Connect to sqlite database and print success message
  conn = sqlite3.connect('cosn.db')
  print("Opened database successfully")

  # Delete records of online users
  conn.execute("DELETE FROM online_users")
  conn.commit()

  # Retrieve data from request
  while 1:
    data, address = server_socket.recvfrom(1024)
    request = pickle.loads(data)
    command = request[0]

    if command == "REGISTER":
      return_message = pickle.dumps(register_user(request, conn))

    elif command == "QUERY":
      return_message = pickle.dumps(query_user(request, conn))

    elif command == "LOGOUT":
      return_message = pickle.dumps(logout_user(request[1]))

    elif command == "DOWN": 
      return_message = pickle.dumps(down_user(request[1]))

    else:
      log("Invalid data from client ( " ,address[0], " " , address[1] , " ): ")
      log(command)

    server_socket.sendto(return_message, address)


if __name__ == '__main__':
  view = server_gui.ServerGui()
  listener = threading.Thread(target = probe_server)
  listener.start()

  view.start()