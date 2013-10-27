import sqlite3
################################################################
# These functions are used by the server to interact with the 
# database and give the server commands to return to the user
################################################################
def remove_user_from_table(username, conn): 
  conn.execute("DELETE FROM online_users WHERE username = ?", [username])
  conn.commit()

def logout_user(username, conn): 
  remove_user_from_table(username, conn)
  return [username + " was logged out successully"]

# Return user location or a message that explains the user is probably offline
def query_user(request, conn):
  cursor = conn.execute("SELECT * FROM online_users WHERE username = ? LIMIT 1", [str(request[1])])
  exists = False
  for row in cursor:
    if row[0]:
      exists = True 
  if exists:
    return ["LOCATION", row[0], row[1], row[2], row[3]]
  else:
    return ["Error", "User was not found--probably offline"]

# Insert a user into the online_users table
def register_user(request, conn):
  cursor = conn.execute("SELECT * FROM online_users WHERE username = ? LIMIT 1", [request[3]] )
  exists = False
  for row in cursor:
    if row[0]:
      exists = True 
  if exists:
    return ["ACK", row[0], row[1], row[2], row[3], "User already registered"]
  else:
    conn.execute("INSERT INTO online_users(id, ip_address, port, username) VALUES(NULL, ?, ?, ?)", [request[1], request[2], request[3]])
    conn.commit()
    return ["ACK", request[1], request[2], request[3], "Registered successfully"]

def down_user(username, conn):
  remove_user_from_table(username, conn)
  return ["User was taken offline for inactivity"]

def ping_command(user_data):
 return ["PING", user_data[4], user_data[2], user_data[3]] 