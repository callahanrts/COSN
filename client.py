from array import *
from socket import *
import pickle
import sys
import threading
from tkinter import * 

#####################
## SOCKET SETUP
#####################

HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
USERNAME = str(sys.argv[3])
SERVER_ADDR = ("", 9000)
STATUS = 0
MESSAGE = 1

client_socket = socket(AF_INET, SOCK_DGRAM)
chat_conn = socket(AF_INET, SOCK_STREAM) 


# Client-Server Command Strings
register = ["REGISTER", HOST, PORT, USERNAME] # Response => ACK
query    = ["QUERY", "1"]                     # Response => LOCATION
logout   = ["LOGOUT", USERNAME]               # Response => none  
down     = ["DOWN", USERNAME]

# P2P Command Strings
ping      = ["PING", "user", "ip", "port"]     # Response => PONG
pong      = ["PONG", "user", "ip", "port"]     # Response => none
friend    = ["FRIEND", ""]                     # Response => CONFIRM
confirm   = ["CONFIRM", USERNAME]              # Response => none
busy      = ["BUSY", USERNAME]                 # Response => none
chat      = ["CHAT", 'msg', "username"]        # Response => DELIVERED
delivered = ["DELIVERED", "delivered"]         # Response => none

initial_load = True
chat_flag = False # chatting flag


def execute_command():
  server = False
  peer = False
  command = var.get().upper()
  if command == "REGISTER":
    send_message = register_user()
    server = True

  elif command == "QUERY":
    data = log(query_user(username.get()))
    return

  elif command == "LOGOUT":
    send_message = logout_user()
    server = True

  elif command == "CHAT":
    chat_window()
    peer = True
    return

  elif command == "PING":
    data = query_user(username.get())
    send_message = ping_user(data)
    peer = True

  elif command == "FRIEND":
    data = query_user(username.get())
    send_message = befriend_user(data)
    peer = True

  if server: 
    client_socket.sendto(pickle.dumps(send_message), SERVER_ADDR)
    recv_data, addr = client_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    log(data)

  elif peer: log(sendto_peer(data, send_message))

####################
## GUI SETUP 
####################


root = Tk()

root.title(USERNAME)
root.geometry("500x300")

# Command Label
c_label = Label(root, text = "Command", anchor=W)
c_label.pack()

# Command Menu Button
var = StringVar(root)
var.set("Register") # initial value

option = OptionMenu(root, var, "Register", "Query", "Logout", "Ping", "Friend", "Chat")
option.config(width=10)
option.pack()


# Username Label
i_label = Label(root, text = "Username, if neccessary", anchor=W, width=30)
i_label.pack()

# Uername input
username = StringVar()
text_field = Entry(root, textvariable = username, width=30)
text_field.pack()

# Send Button
button = Button(root, text="Send", command=execute_command)
button.pack()

# Client Log
m_label = Label(root, text = "Client Log Messages")
m_label.pack()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y, pady=(0, 10), padx=(0, 10))

listbox = Listbox(root)
listbox.config(width=65, height=15)
listbox.pack(padx=(10, 0), pady=(0, 10))

###################################
# Items for Chat Window
###################################
chat_message = StringVar()
messaging = IntVar()
chatbox = None

###########################
## Event Listeners
###########################

def sendto_peer(data, send_message):
  chat_conn = socket(AF_INET, SOCK_STREAM)  
  try: 
    chat_conn.connect((data[2], int(data[3])))
    chat_conn.send(pickle.dumps(send_message))  
  except: 
    log("User is offline")
    down_user(username.get())
    return

  recv_data, addr = chat_conn.recvfrom(1024)
  return pickle.loads(recv_data) 


def chat_window():
  # create child window
  win = Toplevel()

  # Chat Log
  Label(win, text = "Chat Log Messages").pack()

  Scrollbar(win).pack(side=RIGHT, fill=Y, pady=(0, 10), padx=(0, 10))

  global chatbox
  chatbox = Listbox(win)
  chatbox.config(width=65, height=15)
  chatbox.pack(padx=(10, 0), pady=(0, 10))

  # Username Label
  Label(win, text = "Chat Message: ", anchor=W, width=30).pack()

  # Chat input
  log("get friend data")
  friend_data = query_user(username.get())
  log(friend_data)

  global messaging
  messaging.set(1)

  e = Entry(win, textvariable = chat_message, width=30)
  e.pack()

  # Send Message
  Button(win, text="Send", command=lambda: reply_message(friend_data)).pack()


def log_message(message):
  global chatbox
  chatbox.insert(END, message)

def reply_message(friend_data):
  chat[MESSAGE] = chat_message.get()
  log_message(USERNAME+": "+chat[MESSAGE])
  chat[2] = USERNAME
  sendto_peer(friend_data, chat)
  return

###########################
## Functions
###########################

def chatting(val):
  chat_flat = val

def is_chatting():
  global messaging
  if messaging.get() == 1:
    return True
  return False

##
# Client-Server Commands
##
def register_user(): 
  return register

def query_user(username): 
  query[MESSAGE] = username
  client_socket.sendto(pickle.dumps(query), SERVER_ADDR)
  recv_data, addr = client_socket.recvfrom(1024)
  data = pickle.loads(recv_data) 
  return data

def logout_user(): 
  return logout

def down_user(username): # User should not be able to call this manually
  down[MESSAGE] = username
  return down

def list_commands(): 
  print("REGISTER")
  print("QUERY")
  print("LOGOUT")

##
# P2P Commands
##
def ping_user(user):
  ping[MESSAGE] = user[MESSAGE]
  ping[2] = user[2]
  ping[3] = user[3]
  return ping

def pong_user():
  pong[MESSAGE] = USERNAME
  pong[2] = HOST
  pong[3] = PORT
  return pong

def befriend_user(user):
  friend[MESSAGE] = user[MESSAGE]
  return friend

def log(message):
  listbox.insert(END, message)

def peer_listener():
  tcp_socket = socket(AF_INET, SOCK_STREAM)
  tcp_socket.bind((HOST, PORT))
  tcp_socket.listen(1024)
  while 1:
    peer_socket, addr = tcp_socket.accept()
    recv_data, addr = peer_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    log(data)
    if data[STATUS] == "PING":
      reply = pong_user()

    elif data[STATUS] == "FRIEND":
      reply = confirm

    elif data[STATUS] == "CHAT":
      username.set(data[2])
      if not is_chatting(): chat_window()
      log_message(data[2]+ ": "+data[MESSAGE])
      peer_socket.send(pickle.dumps(delivered))
      continue

    elif data[STATUS] == "DELIVERED": 
      log("Delivered")
      log(data[MESSAGE])
      peer_socket.close()
      continue

    return_message = pickle.dumps(reply)
    peer_socket.send(return_message)
    peer_socket.close()

  tcp_socket.close()

#######################################
##              MAIN                 ##
#######################################

if __name__ == '__main__':
  listener = threading.Thread(target = peer_listener)
  listener.start()

  root.mainloop()
