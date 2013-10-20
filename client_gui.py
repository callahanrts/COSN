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
tcp_socket = socket(AF_INET, SOCK_STREAM)
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
chat      = ["CHAT", 'msg']                    # Response => DELIVERED
delivered = ["DELIVERED", "delivered"]         # Response => none

initial_load = True
chat_flag = False # chatting flag


###########################
## Event Listeners
###########################

def execute_command():
  command = var.get().upper()
  if command == "REGISTER":
    send_message = register_user()

  elif command == "QUERY":
    log(query_user(username.get()))
    return

  elif command == "LOGOUT":
    send_message = logout_user()

  elif command == "CHAT":
    chat_manager()

  client_socket.sendto(pickle.dumps(send_message), SERVER_ADDR)

  recv_data, addr = client_socket.recvfrom(1024)
  data = pickle.loads(recv_data) 
  log(data)


####################
## GUI SETUP 
####################


root = Tk()

root.title("Server")
root.geometry("600x400")

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

# # attach listbox to scrollbar
# listbox.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=listbox.yview)


###########################
## Functions
###########################

def chatting(val):
  chat_flat = val

def is_chatting():
  if chat_flag: return True
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
  data = query_user(user[4])
  if data[0] == "LOCATION": 
    friend[MESSAGE] = data[4]
    return friend
  else: 
    return False

def log(message):
  listbox.insert(END, message)


#######################################
##              MAIN                 ##
#######################################

if __name__ == '__main__':
  root.mainloop()
