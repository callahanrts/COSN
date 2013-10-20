from socket import *
import time
import sqlite3
import pickle



##
# Server Commands
##
def register_user():
  cursor = conn.execute("SELECT * FROM online_users WHERE username = ? LIMIT 1", [request[3]] )
  exists = False
  for row in cursor:
    if row[0]:
      exists = True 
  if exists:
    print("User is already online")
    return ["ACK", row[0], row[1], row[2], row[3]]
  else:
    conn.execute("INSERT INTO online_users(id, ip_address, port, username) VALUES(NULL, ?, ?, ?)", [request[1], request[2], request[3]])
    conn.commit()
    print("User has been registered")
    return ["ACK", request[1], request[2], request[3]]

def query_user():
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

