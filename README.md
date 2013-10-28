Cody Callahan
View this readme here to view it with optimal formatting https://github.com/callahanrts/COSN

Client-Server / P2P project for a networkin course

To start a client:
```
cd client
python client.py HOST PORT USERNAME
```

To start the server:
```
python server/server.py
```

Changes I've made to the spec:
```
- Messages sent to client and server are not done so with a string. They placed into an array 
  and then pickled and sent over the connection. 
- I decided to use JSON as opposed to XML for its robustness and the answers on this SO 
  post: http://stackoverflow.com/questions/3536893/what-are-the-pros-and-cons-of-xml-and-json 
- Erros do not get logged to a file. They get logged in the gui
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
  - No message will be sent in return, but the requested user's profile will now be stored in the
    friends/ directory
- RELAY select relay and give the username to request from in "Username 1". Then, put the user 
  profile you are requesting in "Username 2" and click "Send (client)"
  - No message will be sent in return, but the requested user's profile will now be stored in the
    friends/ directory
- GET select get and give the username to request the file from in "Username 1". Then, put the file
  you are requesting in "Username 2" and click "Send (client)" The program will expect your file to 
  be stored in the user's root directory "users/YOUR_USERNAME/". 
  - The requested file will be stored in "users/YOUR_USERNAME/files/" unless the requested file 
    could not be found. If it could not be found a message will be returned telling the user the 
    file does not exist. 
- CHAT Given more time, I would like to implement chats that open in separate windows when initiated.
  Currently chat works like this:
  - UserA types UserB's username to start chat with in "Username 1" and fills out the chat message 
    input. UserA Presses send to chat.
  - UserB will get UserA's chat and automatically UserB's "Username 1" field will be set to UserA's 
    username. UserB can then fill out the message input and click send to reply. This can be done with
    multiple users at the same time, so long as the correct username is in the "Username 1" field. 
```

Description of Included files:

- client
  - client.py - The main client program. Interacts with the server and other instances of clients
  - client_gui.py - Creates a main window and widgets to be used by a client instance
  - clientcmd.py - A set of functions used to create commands to be sent to another client
- extras
  - constants.py - Templates for many of the commands that will be used by the client
  - gui_builder.py - A class to aid in the building and configuring of windows and widgets
  - profile.json - A template for user profiles. It gets automatically placed in a user's directory if they don't have it. 
  - text - a plaintext template that can be used to send from client to client. It is large enough to require more than a single packet when sending. 
- license
  - license - open source MIT license agreement
- server
  - cosn.db - The sqlite database used to store client information
  - server.py - The main server program. Interacts with clients and the database. 
  - server_functions.py - A list of functions used by the server to deal with the database and construct useful responses to the client.
  - server_gui.py - A class used to build and maintain the main window for the server. 
  - servercmd.py - These are commands for the client to construct and send to the server
- users (Structure generated and manipulated by the client program)
  - USER
    - files
    - friends
      - USER B
        - profile.json
      - USER C
        - profile.json


