from socket import *
from threading import * 
import select
import sys
import pickle
import logging
import queue

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

def server_command_handler(command, user):
  global view
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
  udp_socket.sendto(pickle.dumps(send_message), SERVER_ADDR)
  recv_data, addr = udp_socket.recvfrom(1024)
  return pickle.loads(recv_data) 

def send_chat(message):
  view.log(messag)

def peer_command_handler(command, user):
  # Create socket to connect with a user
  chat_conn = socket(AF_INET, SOCK_STREAM)

  user_data = send_udp(servecmd.query_user(user))

  if command == "FRIEND":
    send_message = clientcmd.befriend_user(user)

  elif command == "CHAT":
      # Create Chat GUI
    chat_window = ChatWindow()
    chat_window.initChatMenu(user_data, username, chat_conn)
    #chat_conn.close()
    return

  try:
    chat_conn.connect((user_data[2], int(user_data[3])))
    chat_conn.send(pickle.dumps(send_message)) 
    recv_data, addr = chat_conn.recvfrom(1024)
    response = pickle.loads(recv_data) 
    view.log(response) 
  except:
    logging.exception("hm")
    view.log("User is offline")
    #down_user(username.get())

  chat_conn.close()

def peer_listener():
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

          # Switch on the different types of messages or return original if not recognized
          if message[0] == "FRIEND":
            message_queues[s].put(pickle.dumps(cmd.confirm))
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


  # while 1:

  #   peer_socket, addr = tcp_socket.accept()
  #   recv_data, addr = peer_socket.recvfrom(1024)
  #   data = pickle.loads(recv_data) 
  #   view.log(data)

  #   if data[0] == "FRIEND":
  #     reply = cmd.confirm

  #   if data[0] == "CHAT": 
  #     reply = cmd.delivered

  #   if reply != None:
  #     return_message = pickle.dumps(reply)
  #     peer_socket.send(return_message)

  #   peer_socket.close()
  
  tcp_socket.close()

if __name__ == '__main__':
  # Listen for incoming peer connections
  listener = Thread(target = peer_listener)
  listener.start()

  # Create GUI
  view = MainWindow(server_command_handler, peer_command_handler, username)
  view.start()