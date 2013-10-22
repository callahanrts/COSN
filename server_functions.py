import sqlite3

def remove_user_from_table(username, conn): 
  conn.execute("DELETE FROM online_users WHERE username = ?", [username])
  conn.commit()

def logout_user(username, conn): 
  remove_user_from_table(username)
  return ["User was logged out successully"]

def query_user(request, conn):
  cursor = conn.execute("SELECT * FROM online_users WHERE username = ? LIMIT 1", [str(request[1])])
  exists = False
  for row in cursor:
    if row[0]:
      exists = True 
  if exists:
    return ["LOCATION", row[0], row[1], row[2], row[3]]
  else:
    return ["Error", "User was not found"]

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