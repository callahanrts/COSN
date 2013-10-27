from socket import *
import time
import pickle
import threading
import sqlite3
import logging

import server_gui
from server_functions import *

#Connect to server and print message 
server_socket = socket(AF_INET, SOCK_DGRAM)  
server_socket.bind(('', 9000))
print("(9000) UDP Server Waiting for client...")

# View
view = None

def probe_server():
  global view
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
    view.log(request)
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
      if not ping_user(request[1]):
        reply = down_user(request[1], conn)
        return_message = pickle.dumps(reply)
      else:
        return_message = pickle.dumps("User is busy")

    else:
      view.log("Invalid data from client ( " ,address[0], " " , address[1] , " ): ")
      view.log(command)

    view.log(reply)
    server_socket.sendto(return_message, address)

# Ping user upon another users request
def ping_user(username):
  global view
  conn = sqlite3.connect('server/cosn.db')
  user_data = query_user(["", username], conn)
  send_message = ping_command(user_data)
  chat_conn = socket(AF_INET, SOCK_STREAM)
  try:
    chat_conn.connect((user_data[2], int(user_data[3])))
    chat_conn.send(pickle.dumps(send_message)) 
    recv_data, addr = chat_conn.recvfrom(1024)
    response = pickle.loads(recv_data) 
    view.log(response)
    return True
  except: # Remove user from online table if no repsonse is received
    logging.exception("hm")
    view.log("User is offline")
    down_user(username, conn)
    return False

if __name__ == '__main__':
  view = server_gui.ServerGui(ping_user)
  listener = threading.Thread(target = probe_server)
  listener.start()

  view.start()