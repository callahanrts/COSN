from socket import *
from threading import * 
from shutil import * 
import select
import sys
import pickle
import logging
import queue
import json
import os

# Append paths
sys.path.append('../extras')
sys.path.append('../server')
sys.path.append('../client')

# User Defined
from client_gui import * 
from constants import *
from servercmd import *
from clientcmd import *

class Client:
  def __init__(self, host, port, username):
    self.username = username
    self.host = host
    self.port = int(port)
    self.server_addr = ("", 9000)

    # Initialize Commands Class
    self.cmd = Command(host, port, self.username)
    self.servecmd = ServerCommands(self.cmd)
    self.clientcmd = ClientCommands(self.cmd)

    # Chat variables
    self.chat_counter = 1

    # Chat socket
    self.chat_conn = None

    # Friends list
    self.friends = [ ]

    # Create Directories if they don't exist
    self.user_directory = "../users/" + self.username + "/" 
    self.create_dir_if_not_exists(self.user_directory)

    self.friends_directory = self.user_directory + "friends/"
    self.create_dir_if_not_exists(self.friends_directory)

    # Profile data
    try:
      self.profile = open(self.user_directory + self.username + ".json")
    except IOError:
      copyfile("../extras/profile.json", "../users/" + self.username + "/" + self.username + ".json")
    
    self.profile = open(self.user_directory + self.username + ".json")
    self.profile = json.load(self.profile)
    self.profile_version = 1

    # Listen for incoming peer connections
    listener = Thread(target = self.peer_listener)
    listener.start()

    # Create GUI
    self.view = MainWindow(self.server_command_handler, self.peer_command_handler, self.chat_command, self.username)
    self.view.start()

  def create_dir_if_not_exists(self, path):
    if not os.path.exists(path): os.makedirs(path)

  def server_command_handler(self, command, user):
    if command == "REGISTER":
      send_message = self.servecmd.register_user()

    elif command == "QUERY":
      send_message = self.servecmd.query_user(user)

    elif command == "LOGOUT":
      send_message = self.servecmd.logout_user()

    self.view.log(self.send_udp(send_message))

  def send_udp(self, send_message):
    # UDP Socket to connect with server
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.settimeout(2)
    print(send_message)
    try: 
      udp_socket.sendto(pickle.dumps(send_message), self.server_addr)
      recv_data, addr = udp_socket.recvfrom(1024)
      return pickle.loads(recv_data) 
    except timeout:
      self.view.log("Server timed out")


  def peer_command_handler(self, command, user, alt_data):
    request_for_profile = False
    request_for_file = False

    # Create socket to connect with a user
    self.chat_conn = socket(AF_INET, SOCK_STREAM)

    user_data = self.send_udp(self.servecmd.query_user(user))

    if command == "FRIEND":
      self.friends.append(user)
      send_message = self.clientcmd.befriend_user(self.username)

    elif command == "REQUEST": 
      send_message = self.clientcmd.request_profile(user, self.profile_version) # version but not needed yet
      request_for_profile = True

    elif command == "RELAY": 
      send_message = self.clientcmd.request_profile_relay(alt_data, self.profile_version) # version but not needed yet
      request_for_profile = True

    elif command == "GET": 
      send_message = self.clientcmd.request_file(alt_data)
      request_for_file = True

    try:
      print(user_data)
      self.chat_conn.connect((user_data[2], int(user_data[3])))
      self.chat_conn.send(pickle.dumps(send_message)) 
      recv_data, addr = self.chat_conn.recvfrom(1024)
      response = pickle.loads(recv_data) 

      if request_for_profile:
        self.save_profile(response)
      elif request_for_file:
        self.save_file(response)
      else:
        self.view.log(response) 
    except:
      logging.exception("hm")
      self.view.log(self.send_udp(self.clientcmd.user_offline(user_data[4])))

    self.chat_conn.close()

  def save_file(self, data):
    recv_data, addr = self.chat_conn.recvfrom(data + 1024)
    resp_file = pickle.loads(recv_data) 

    directory = "../users/"+self.username+"/friends/files/"
    if not os.path.exists(directory):
      os.makedirs(directory)

    if data > 0:
      # create file
      f = open(directory+resp_file[1], "wb")
      f.write(resp_file[3])
      f.close()
    else: 
      self.view.log(resp_file)

  def save_profile(self, data):
    recv_data, addr = self.chat_conn.recvfrom(data + 1024)
    resp_file = pickle.loads(recv_data)
    if data > 0:
      directory = "../users/"+self.username+"/friends/"+resp_file[1]+"/"
      json_profile = json.loads(resp_file[3])
      if not os.path.exists(directory):
        os.makedirs(directory)

      with open(directory + resp_file[1] + ".json", "w") as outfile:
        json.dump(json_profile, outfile, indent=2)
    else:
      self.view.log(resp_file)

  # Current, single window chat
  def chat_command(self, message, user): 
    if user in self.friends:
      self.chat_conn = socket(AF_INET, SOCK_STREAM)
      user_data = self.send_udp(self.servecmd.query_user(user))
      self.view.log_message(self.username+": "+message)
      try:
        self.chat_conn.connect((user_data[2], int(user_data[3])))
        self.chat_conn.send(pickle.dumps(self.clientcmd.chat_message(message, self.username, self.chat_counter))) 
        self.chat_counter += 1

        # Get size of message
        recv_data, addr = self.chat_conn.recvfrom(1024)
        response = pickle.loads(recv_data) 

        # Get rest of message
        recv_data, addr = self.chat_conn.recvfrom(response + 1024)
        response = pickle.loads(recv_data) 

        self.view.log(response) 
      except:
        logging.exception("hm")
        self.view.log(self.send_udp(self.clientcmd.user_offline(user_data[4])))
    else:
      self.view.log("You must be friends with this user before chatting with them")

  def peer_listener(self):
    # Set up main, non-blocking, server socket to listen for tcp connections
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.setblocking(0)
    tcp_socket.bind((self.host, self.port))
    tcp_socket.listen(1024)

    # Sockets from which we expect to read
    inputs = [ tcp_socket ]

    # Sockets to which we expect to write
    outputs = [ ]

    # Outgoing message queues (socket:Queue)
    message_queues = {}

    while inputs:
      print("===========================================================================")
      # Wait for at least one of the sockets to be ready for processing
      readable, writable, exceptional = select.select(inputs, outputs, inputs)

      # Handle inputs
      for s in readable:
        if s is tcp_socket:
          connection, client_address = s.accept()
          connection.setblocking(0)
          inputs.append(connection)

          # Give the connection a queue for data we want to send
          message_queues[connection] = queue.Queue()
          print("Inputs:")
          print(inputs)

        else:
          data = s.recv(1024)
          if data: # A readable client socket has data
            # Parse message using pickle
            message = pickle.loads(data)
            self.view.log(message)
  
            # Print to console for debugging
            print("Readable client socket has data")
            print(message)

            # Switch on the different types of messages or return original if not recognized
            if message[0] == "FRIEND":
              self.friends.append(message[1])
              message_queues[s].put(pickle.dumps(self.cmd.confirm))
  
            elif message[0] == "CHAT": 
              chat_message = message[3]
              self.view.username.set(message[2])            
              self.view.log_message(message[2]+": "+message[1])
  
              # Send Size of the message
              message_queues[s].put(pickle.dumps(sys.getsizeof(chat_message)))

              # Send message
              message_queues[s].put(pickle.dumps(self.clientcmd.delivered_message(chat_message)))

            elif message[0] == "REQUEST":
              size = os.path.getsize(self.user_directory + self.username + ".json")
              send_message = self.clientcmd.profile_message(message[1], message[2], json.dumps(self.profile))
              message_queues[s].put(pickle.dumps(size))
              message_queues[s].put(pickle.dumps(send_message))

            elif message[0] == "RELAY": 
              profile_file = self.friends_directory + message[1] + "/" + message[1] + ".json"
              try:
                size = os.path.getsize(profile_file)
                self.profile = open(profile_file)
                self.profile = json.load(self.profile)              
                send_message = self.clientcmd.profile_message(message[1], message[2], json.dumps(self.profile))
              except: 
                size = 0
                send_message = "I don't have the requested profile."
              message_queues[s].put(pickle.dumps(size))
              message_queues[s].put(pickle.dumps(send_message))

            elif message[0] == "GET": 
              try: 
                size = os.path.getsize(self.user_directory + message[1])
                f = open(self.user_directory+message[1], "rb")
                bytes = f.read()
                send_message = self.clientcmd.send_file(message[1], size, bytes)
              except:
                size = 0
                send_message = "File does not exist"
              message_queues[s].put(pickle.dumps(size))
              message_queues[s].put(pickle.dumps(send_message))

            elif message[0] == "PING":
              send_message = self.clientcmd.pong_server(self.username, host, port)
              message_queues[s].put(pickle.dumps(send_message))            

            else:
              print("Command " + str(message[0]) + " not recognized")
              message_queues[s].put(data)

            # Add output channel for response
            if s not in outputs:
              outputs.append(s)

          else: # Interpret empty result as closed connection
            print("Peer dropped out, closing connection")
            # Stop listening for input on the connection
            if s in outputs:
              outputs.remove(s)
            inputs.remove(s)
            s.close()

            # Remove message queue
            del message_queues[s]
  
      # Handle outputs
      for s in writable:
        try:
          next_msg = message_queues[s].get_nowait()
        except queue.Empty:
          # No messages waiting so stop checking for writability.
          print(sys.stderr)
          print('output queue for')
          print(s.getpeername())
          print('is empty')
          outputs.remove(s)
        else:
          print(sys.stderr)
          print('sending "%s" to %s' % (next_msg, s.getpeername()))
          s.send(next_msg)

      # Handle "exceptional conditions"
      for s in exceptional:
        print ('handling exceptional condition for')
        print(s.getpeername())
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
          outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]
  
    # Close tcp connection when server exits
    tcp_socket.close()

if __name__ == '__main__':
  client = Client(sys.argv[1], sys.argv[2], sys.argv[3])