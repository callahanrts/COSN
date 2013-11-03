from socket import *
import time
import pickle
import threading
import sqlite3
import logging

import server_gui
from server_functions import *


class Server(object):
  def __init__(self):
    #Connect to server and print message 
    self.server_socket = socket(AF_INET, SOCK_DGRAM)  
    self.server_socket.bind((u'', 9000))
    print u"(9000) UDP Server Waiting for client..."

    # Connect to sqlite database and print success message
    self.conn = sqlite3.connect(u'server/cosn.db')
    print u"Opened database successfully"

    # Delete records of online users
    self.conn.execute(u"DELETE FROM online_users")
    self.conn.commit()

    # Start UDP listener thread
    listener = threading.Thread(target = self.probe_server)
    listener.start()

    # Create view for server 
    self.view = server_gui.ServerGui(self.ping_user)

    # Start gui mainloop (must be called last)
    self.view.start()

  def probe_server(self):
    while 1:
      # Retrieve data from request
      data, address = self.server_socket.recvfrom(1024)
      request = pickle.loads(data)
      command = request[0]

      # Log request in server message log
      self.view.log(request)

      # Get message to return to user
      return_message = self.reply_to_command(command, request)

      # If a return message was created, reply to it
      if return_message != None:
        self.view.log(return_message)
        self.server_socket.sendto(pickle.dumps(return_message), address)

  def reply_to_command(self, command, request):
    # Connect to sqlite database (must be done in each thread)
    self.conn = sqlite3.connect(u'server/cosn.db')

    if command == u"REGISTER":
      return register_user(request, self.conn)

    elif command == u"QUERY":
      return query_user(request, self.conn)

    elif command == u"LOGOUT":
      return logout_user(request[1], self.conn)

    elif command == u"DOWN": 
      if not self.ping_user(request[1]):
        return down_user(request[1], self.conn)
      else:
        return u"User is busy"

    else:
      self.view.log(u"Invalid data from client: " + command)

  # Ping user upon another users request
  def ping_user(self, username):
    # Get user data and the command to send to user
    user_data = query_user([u"", username], self.conn)
    send_message = ping_command(user_data)

    # Create tcp socket to send ping to client
    chat_conn = socket(AF_INET, SOCK_STREAM)

    try:
      # Connect to client and send message
      chat_conn.connect((user_data[2], int(user_data[3])))
      chat_conn.send(pickle.dumps(send_message)) 

      # Receive reply from client. If no response, send to except block
      recv_data, addr = chat_conn.recvfrom(1024)
      response = pickle.loads(recv_data) 
      self.view.log(response)
      return True
    except: 
      # Remove user from online table if no repsonse is received and log message
      down_user(username, self.conn)
      self.view.log(u"User is offline")
      return False

if __name__ == u'__main__':
  server = Server()
