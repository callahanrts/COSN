
Client-Server / P2P project for a networkin course

To start a client:
```
cd client
python client.py HOST PORT USERNAME
```

To start the server:
```
cd server
python server.py
```

UDP Commands:
```
- REGISTER select register and click "Send (server)"
  - ACK will be returned
- QUERY select query and give a username for "Username 1". Now click "Send (server)"
  - LOCATION will be returned
- LOGOUT select logout and click "Send (server)"
  - A success message will be returned
```
TCP Commands: 
```
- FRIEND select friend and give a username for "Username 1". Now click "Send (client)"
  - CONFIRM will be returned
- REQUEST select request and give a username for "Username 1". Now click "Send (client)"
  - No message will be sent in return, but the requested user's profile will now be stored in the friends/ directory
- RELAY select relay and give the username to request from in "Username 1". Then, put the user profile you are requesting in "Username 2" and click "Send (client)"
  - No message will be sent in return, but the requested user's profile will now be stored in the friends/ directory
- GET select get and give the username to request the file from in "Username 1". Then, put the file you are requesting in "Username 2" and click "Send (client)" The program will expect your file to be stored in the user's root directory "users/YOUR_USERNAME/"
  - No message will be sent in return, but the requested file will be stored in "users/YOUR_USERNAME/files/"
```