from __future__ import with_statement
from socket import *
from threading import * 
from shutil import * 
import select
import sys
import pickle
import logging
import Queue
import json
import os
from io import open

# Append paths
sys.path.append(u'../extras')
sys.path.append(u'../server')
sys.path.append(u'../client')

# User Defined
from client_gui import * 
from constants import *
from servercmd import *
from clientcmd import *
from my_dropbox import * 

class Client(object):
  def __init__(self, host, port, username):
    # Initialize user variables
    self.username = username
    self.host = host
    self.port = int(port)
    self.server_addr = (u"", 9000)
    self.stop_thread = False

    # Initialize Command Classes
    self.cmd = Command(host, port, self.username)
    self.servecmd = ServerCommands(self.cmd)
    self.clientcmd = ClientCommands(self.cmd)

    # Chat variables
    self.chat_counter = 1

    # Friends list
    self.friends = [ 
      {
        "username": "test",
        "host": "''", 
        "port": 9000
      } 
    ]

    # Create directories if they don't exist
    self.setup_client_directories()

    # Create user profile from template if it doesn't exist
    self.location = self.load_user_file("location.json")
    self.user = self.load_user_file("profile.json")
    self.content = self.load_user_file("content.json")
    self.location["address"]["ID"] = self.username  
    self.location["address"]["IP"] = self.host
    self.location["address"]["port"] = self.port


    self.conn = sqlite3.connect(u'../server/cosn.db')
    cursor = self.conn.execute(u"SELECT friend FROM friend WHERE username = ?", [self.username])
    f_list = []
    for row in cursor:
      if row[0]:
        f_list.append(row[0])

    # Create GUI
    self.view = MainWindow(self.username, self.shutdown)
    self.view.add_command_elements(self.peer_command_handler, f_list)
    self.view.add_file_elements(self.get_file)
    self.view.add_chat_elements(self.chat_command)
    self.view.add_log_box()
    self.view.add_drive_elements(self.link_dropbox)
    self.view.add_request_elements(self.request_friend)
    self.view.add_accept_friend_elements(self.accept_friend)
    self.view.add_upload_elements(self.upload_profile)

    # Dropbox Object
    self.dropbox = Dropbox(username, self.user, self.location, self.content, self.view)

    for friend in f_list:
      if friend == "test": continue
      self.friends.append(self.dropbox.get_friend(friend))

    # Listen for incoming peer connections
    listener = Thread(target = self.peer_listener)
    listener.start()

    self.view.start()

  def get_file(self, filename, username):
    # Create socket to connect with a user
    self.chat_conn = socket(AF_INET, SOCK_STREAM)
    send_message = self.clientcmd.request_file(filename)

    try:
      for friend in self.friends:
        if friend["username"] == username:
          self.chat_conn.connect((friend["host"], friend["port"]))
      self.chat_conn.send(pickle.dumps(send_message)) 
      response = self.retrieve_data()
      self.save_file(response)

    except: # log errors
      logging.exception("hm")

    self.chat_conn.close()

    return

  def save_file(self, data):
    # Set directory or create if needed
    directory = "../users/"+self.username+"/friends/files/"
    self.create_dir_if_not_exists(directory)

    if data[1] != 0:  # Create File
      f = open(directory+data[1], "wb")
      f.write(data[3])
      f.close()
    else: 
      self.view.log(data)

  def setup_client_directories(self):
    # Create Directories if they don't exist
    self.user_directory = u"../users/" + self.username + u"/" 
    self.create_dir_if_not_exists(self.user_directory)

    self.friends_directory = self.user_directory + u"friends/"
    self.create_dir_if_not_exists(self.friends_directory)

  def load_user_file(self, filename):
    filepath = self.user_directory + filename
    try:
      user_file = open(filepath) # Attempt to retrieve user profile
    except IOError: # Generate template user profile or blank
      copyfile(u"../extras/" + filename, filepath)
      user_file = open(filepath)
    return json.load(user_file)

  def save_user_file(self, filename, json_obj):
    filepath = self.user_directory + filename
    with open(filepath, 'wb') as outfile:
      json.dump(json_obj, outfile, indent=2, sort_keys=True)

  def create_dir_if_not_exists(self, path):
    if not os.path.exists(path): os.makedirs(path)

  def peer_command_handler(self, command, user):
    # Respond to commands
    if command == u"FRIEND":
      self.chat_conn = socket(AF_INET, SOCK_STREAM)
      try:
        self.chat_conn.connect(user)
        self.chat_conn.send(pickle.dumps([command, self.dropbox.share_url()])) 
        self.view.log(self.retrieve_data())
      except: # log errors
        logging.exception(u"hm")
      self.chat_conn.close()

    elif command == u"PROFILE": 
      if self.dropbox.get_friend_files(user) == False: self.view.log("Profile not found")

  def retrieve_data(self):
    self.chat_conn.settimeout(2)
    data = bytearray()
    while 1:
      try:
        recv_data = self.chat_conn.recv(1024)
        data.extend(recv_data)
        self.chat_conn.settimeout(0.25)
      except timeout:
        self.chat_conn.settimeout(2)
        break
    return pickle.loads(data)

  # Current, single window chat
  def chat_command(self, message, user): 
    loc = self.dropbox.get_location(user)
    if loc["address"]["port"] != 0 and loc["address"]["IP"] != '0.0.0.0':
      # Open connection and get user
      self.chat_conn = socket(AF_INET, SOCK_STREAM)
      self.view.log_message(self.username+u": "+message)
      try:
        self.chat_conn.connect((loc["address"]["IP"], int(loc["address"]["port"])))
        chat_message = self.clientcmd.chat_message(message, self.username, self.chat_counter)
        self.chat_conn.send(pickle.dumps(chat_message))
        self.chat_counter += 1

        response = self.retrieve_data() # Get message
        self.view.log(response) 
      except:
        logging.exception(u"hm")

    else: 
      self.view.log(u"Your friend is not available")

  def respond_to(self, message):
    # Switch on the different types of messages or return original if not recognized
    if message[0] == u"FRIEND":
      self.dropbox.accept_friend(message[1], sqlite3.connect(u'../server/cosn.db'))
      return pickle.dumps(self.cmd.confirm) # Queue message to be returned

    elif message[0] == u"CHAT": 
      self.view.username.set(message[2])            
      self.view.log_message(message[2]+u": "+message[1])
      return pickle.dumps(self.clientcmd.delivered_message(message[3])) # Send message

    elif message[0] == u"REQUEST":
      send_message = self.clientcmd.profile_message(message[1], message[2], json.dumps(self.user)) 
      return pickle.dumps(send_message)  # Send message

    elif message[0] == u"RELAY": 
      profile_file = self.friends_directory + message[1] + u"/" + message[1] + u".json"
      try:
        self.user = json.load(open(profile_file)) # Read in user profile
        send_message = self.clientcmd.profile_message(message[1], message[2], json.dumps(self.user))
      except: 
        send_message = u"I don't have the requested profile."
      return pickle.dumps(send_message) # Send profile

    elif message[0] == u"GET": 
      try: 
        size = os.path.getsize(self.user_directory + message[1])
        f = open(self.user_directory+message[1], u"rb")
        str = f.read()
        send_message = self.clientcmd.send_file(message[1], size, str)
      except:
        send_message = ["File does not exist", 0]
      return pickle.dumps(send_message) # Send requested file

    elif message[0] == u"PING":
      send_message = self.clientcmd.pong_server(self.username, self.host, self.port)
      return pickle.dumps(send_message) # Send pong back to server

    else:
      print u"Command " + unicode(message[0]) + u" not recognized"
      return data

  def handle_inputs(self, readable, inputs, outputs, message_queues, tcp_socket):
    for s in readable:
      if s is tcp_socket:
        connection, client_address = s.accept()    # Accept connection
        connection.setblocking(0)                  # Don't allow socket blocking
        inputs.append(connection)                  # add connection to inputs arr
        message_queues[connection] = Queue.Queue() # Create message queue

      else:
        data = s.recv(1024)
        if data: 
          message = pickle.loads(data)                    # Parse message using pickle
          self.view.log(message)                          # Log message to gui
          message_queues[s].put(self.respond_to(message)) # Add response to queue

          if s not in outputs:
            outputs.append(s) # Add output channel for response

        else: # Interpret empty result as closed connection
          print u"Peer dropped out, closing connection"
          # Stop listening for input on the connection
          if s in outputs:
            outputs.remove(s)
          inputs.remove(s)
          s.close()

          del message_queues[s] # Remove message queue

  def handle_outputs(self, writable, outputs, message_queues):
    for s in writable:
      try:
        next_msg = message_queues[s].get_nowait()
      except Queue.Empty:
        outputs.remove(s) # No messages waiting so stop checking for writability.
      else:
        s.sendall(next_msg)

  def handle_exceptionals(self, exceptional, inputs, outputs, message_queues):
    for s in exceptional:
      inputs.remove(s)
      if s in outputs:
        outputs.remove(s)
      s.close()
      del message_queues[s] # Remove message queue

  def peer_listener(self):
    # Set up main, non-blocking, server socket to listen for tcp connections
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.setblocking(0)
    tcp_socket.bind((self.host, self.port))
    tcp_socket.listen(1024)

    inputs = [ tcp_socket ]  # Sockets from which we expect to read
    outputs = [ ]            # Sockets to which we expect to write
    message_queues = {}      # Outgoing message queues (socket:Queue)

    while not self.stop_thread:
      # Wait for at least one of the sockets to be ready for processing
      readable, writable, exceptional = select.select(inputs, outputs, inputs, 3)
      if len(readable) + len(writable) + len(exceptional) is 0: 
        continue
      # Handle, inputs, outputs and exceptionals
      self.handle_inputs(readable, inputs, outputs, message_queues, tcp_socket)
      self.handle_outputs(writable, outputs, message_queues)
      self.handle_exceptionals(exceptional, inputs, outputs, message_queues)

    tcp_socket.close() # Close tcp connection when server exits

  def shutdown(self, window):
    window.destroy()
    self.stop_thread = True
    self.location = self.load_user_file("location.json")
    self.location["address"]["IP"] = "0.0.0.0"
    self.location["address"]["port"] = 0
    self.save_user_file("location.json", self.location)
    self.dropbox.upload_file("location.json")

  def link_dropbox(self, auth_code):
    if not auth_code:
      self.dropbox.auth_url()
    else:
      if self.dropbox.get_token(auth_code): self.view.log("Dropbox linked successfully") 

  def upload_profile(self):
    self.dropbox.upload_file("profile.json")

  def request_friend(self, email):
    t = Thread(target = self.dropbox.send_friend_request(email))
    t.start()

  def accept_friend(self, url):
    friend = self.dropbox.accept_friend(url, None)
    self.peer_command_handler("FRIEND", friend)


if __name__ == u'__main__':
  client = Client(sys.argv[1], sys.argv[2], sys.argv[3])

