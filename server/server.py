from socket import *
import time
import pickle
import threading
import sqlite3

import server_gui
from server_functions import *

#Connect to server and print message 
server_socket = socket(AF_INET, SOCK_DGRAM)  
server_socket.bind(('', 9000))
print("(9000) UDP Server Waiting for client...")

def probe_server():
  # Connect to sqlite database and print success message
  conn = sqlite3.connect('server/cosn.db')
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
      reply = register_user(request, conn)
      return_message = pickle.dumps(reply)

    elif command == "QUERY":
      reply = query_user(request, conn)
      return_message = pickle.dumps(reply)

    elif command == "LOGOUT":
      reply = logout_user(request[1], conn)
      return_message = pickle.dumps(reply)

    elif command == "DOWN": 
      reply = down_user(request[1], conn)
      return_message = pickle.dumps(reply)

    else:
      view.log("Invalid data from client ( " ,address[0], " " , address[1] , " ): ")
      view.log(command)

    view.log(reply)
    server_socket.sendto(return_message, address)


if __name__ == '__main__':
  view = server_gui.ServerGui()
  listener = threading.Thread(target = probe_server)
  listener.start()

  view.start()