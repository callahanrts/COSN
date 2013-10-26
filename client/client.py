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

SERVER_ADDR = ("", 9000)

# Command Line Arguments
host = str(sys.argv[1])
port = int(sys.argv[2])
username = str(sys.argv[3])

# Create GUI Variable
view = None

# Initialize Commands Class
cmd = Command(host, port, username)
servecmd = ServerCommands(cmd)
clientcmd = ClientCommands(cmd)

# Chat variables
chatting_friend = None
chat_counter = 1

# Chat socket
chat_conn = None

# Create Directories if they don't exist
user_directory = "../users/" + username + "/" 
if not os.path.exists(user_directory):
  os.makedirs(user_directory)

friends_directory = user_directory + "friends/"
if not os.path.exists(friends_directory):
  os.makedirs(friends_directory)

# Profile data
try:
  profile = open(user_directory + username + ".json")
except IOError:
  copyfile("../extras/profile.json", "../users/" + username + "/" + username + ".json")
  profile = open(user_directory + username + ".json")
profile = json.load(profile)
profile_version = 1

def server_command_handler(command, user):
  global view
  print(user)
  if command == "REGISTER":
    send_message = servecmd.register_user()

  elif command == "QUERY":
    send_message = servecmd.query_user(user)

  elif command == "LOGOUT":
    send_message = servecmd.logout_user()

  view.log(send_udp(send_message))

def send_udp(send_message):
  # UDP Socket to connect with server
  udp_socket = socket(AF_INET, SOCK_DGRAM)
  print(send_message)
  udp_socket.sendto(pickle.dumps(send_message), SERVER_ADDR)
  recv_data, addr = udp_socket.recvfrom(1024)
  return pickle.loads(recv_data) 


def peer_command_handler(command, user, alt_data):
  global chat_conn
  request_for_profile = False
  request_for_file = False

  # Create socket to connect with a user
  chat_conn = socket(AF_INET, SOCK_STREAM)

  user_data = send_udp(servecmd.query_user(user))

  if command == "FRIEND":
    send_message = clientcmd.befriend_user(user)

  elif command == "REQUEST": 
    send_message = clientcmd.request_profile(user, profile_version) # version but not needed yet
    request_for_profile = True

  elif command == "RELAY": 
    send_message = clientcmd.request_profile_relay(alt_data, profile_version) # version but not needed yet
    request_for_profile = True

  elif command == "GET": 
    send_message = clientcmd.request_file(alt_data)
    request_for_file = True

  try:
    print(user_data)
    chat_conn.connect((user_data[2], int(user_data[3])))
    chat_conn.send(pickle.dumps(send_message)) 
    recv_data, addr = chat_conn.recvfrom(1024)
    response = pickle.loads(recv_data) 

    if request_for_profile:
      save_profile(response)
    elif request_for_file:
      save_file(response)
    else:
      view.log(response) 
  except:
    logging.exception("hm")
    view.log("User is offline")
    #down_user(username.get())

  chat_conn.close()

def save_file(data):
  recv_data, addr = chat_conn.recvfrom(data + 1024)
  resp_file = pickle.loads(recv_data) 

  directory = "../users/"+username+"/friends/files/"
  if not os.path.exists(directory):
    os.makedirs(directory)

  # create file
  f = open(directory+resp_file[1], "wb")
  f.write(resp_file[3])
  f.close()


def save_profile(data):
  directory = "../users/"+username+"/friends/"+data[1]+"/"
  json_profile = json.loads(data[3])
  if not os.path.exists(directory):
    os.makedirs(directory)

  with open(directory + data[1] + ".json", "w") as outfile:
    json.dump(json_profile, outfile, indent=2)


# Current, single window chat
def chat_command(message, user): 
  global chat_conn, chat_counter
  chat_conn = socket(AF_INET, SOCK_STREAM)
  user_data = send_udp(servecmd.query_user(user))
  view.log_message(username+": "+message)
  try:
    chat_conn.connect((user_data[2], int(user_data[3])))
    chat_conn.send(pickle.dumps(clientcmd.chat_message(message, username, chat_counter))) 
    chat_counter += 1
    recv_data, addr = chat_conn.recvfrom(1024)
    response = pickle.loads(recv_data) 
    view.log(response) 
  except:
    logging.exception("hm")
    view.log("User is offline")

def peer_listener():
  # Set up main, non-blocking, server socket to listen for tcp connections
  tcp_socket = socket(AF_INET, SOCK_STREAM)
  tcp_socket.setblocking(0)
  tcp_socket.bind((host, port))
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
          view.log(message)

          # Print to console for debugging
          print("Readable client socket has data")
          print(message)

          global profile

          # Switch on the different types of messages or return original if not recognized
          if message[0] == "FRIEND":
            message_queues[s].put(pickle.dumps(cmd.confirm))

          elif message[0] == "CHAT": 
            global chat_message
            chat_message = message[3]
            message_queues[s].put(pickle.dumps(clientcmd.delivered_message(chat_message)))
            view.username.set(message[2])
            view.log_message(message[2]+": "+message[1])

          elif message[0] == "REQUEST":
            send_message = clientcmd.profile_message(message[1], message[2], json.dumps(profile))
            message_queues[s].put(pickle.dumps(send_message))

          elif message[0] == "RELAY": 
            profile = open(friends_directory + message[1] + "/" + message[1] + ".json")

            profile = json.load(profile)
            send_message = clientcmd.profile_message(message[1], message[2], json.dumps(profile))
            message_queues[s].put(pickle.dumps(send_message))

          elif message[0] == "GET": 
            size = os.path.getsize(user_directory + message[1])
            f = open(user_directory+message[1], "rb")
            bytes = f.read()
            send_message = clientcmd.send_file(message[1], size, bytes)
            message_queues[s].put(pickle.dumps(size))
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
  # Listen for incoming peer connections
  listener = Thread(target = peer_listener)
  listener.start()

  # Create GUI
  view = MainWindow(server_command_handler, peer_command_handler, chat_command, username)
  view.start()