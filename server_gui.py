from tkinter import * 
from socket import *
import time
import sqlite3
import pickle
import threading




#Connect to server and print message 
server_socket = socket(AF_INET, SOCK_DGRAM)  
server_socket.bind(('', 9000))
print("(9000) UDP Server Waiting for client...")

root = Tk()

root.title("Server")
root.geometry("300x500")

l = Label(root, text = "Server Log Messages")
l.pack()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y, pady=(0, 10), padx=(0, 10))

listbox = Listbox(root)
listbox.config(width=100, height=100)
listbox.pack(padx=(10, 0), pady=(0, 10))

# attach listbox to scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

def log(message):
  listbox.insert(END, message)

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
      log("Invalid data from client ( " ,address[0], " " , address[1] , " ): ", command)

    server_socket.sendto(return_message, address)

      #root.after(1000, probe_server)

##
# Server Commands
##
def register_user(request, conn):
  cursor = conn.execute("SELECT * FROM online_users WHERE username = ? LIMIT 1", [request[3]] )
  exists = False
  for row in cursor:
    if row[0]:
      exists = True 
  if exists:
    log("User ("+ request[3] +") is already online")
    return ["ACK", row[0], row[1], row[2], row[3]]
  else:
    conn.execute("INSERT INTO online_users(id, ip_address, port, username) VALUES(NULL, ?, ?, ?)", [request[1], request[2], request[3]])
    conn.commit()
    log("User ("+request[3]+") has been registered")
    return ["ACK", request[1], request[2], request[3]]

def query_user(request, conn):
  cursor = conn.execute("SELECT * FROM online_users WHERE username = ? LIMIT 1", [str(request[1])])
  exists = False
  for row in cursor:
    if row[0]:
      exists = True 
  if exists:
    print("Query for user " + row[1])
    return ["LOCATION", row[0], row[1], row[2], row[3]]
  else:
    print("User was not found")
    return ["Error", "User was not found"]

def remove_user_from_table(username): 
  conn.execute("DELETE FROM online_users WHERE username = ?", [username])
  conn.commit()

def logout_user(username): 
  remove_user_from_table(username)
  print("User logged out")
  return ["User was logged out successully"]

def down_user(username):
  remove_user_from_table(username)
  print(username + " was taken offline for inactivity")
  return ["User was taken offline for inactivity"]


if __name__ == '__main__':
  listener = threading.Thread(target = probe_server)
  listener.start()
  #  root.after(1000, probe_server)
  root.mainloop()
