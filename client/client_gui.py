from Tkinter import * 
from socket import *
import pickle

# Append paths
sys.path.append(u'../extras')

from gui_builder import * 

class MainWindow(object):
  def __init__(self, title, shutdown):
    self.gb = GuiBuilder()
    self.root = Tk()
    self.initMainWindow(title, shutdown)

  # Create the main window
  def initMainWindow(self, title, shutdown):
    # Configure window settings
    self.gb.setTitle(title, self.root)
    self.gb.setGeometry(u"400x575", self.root)

    # Command label
    self.gb.createLabel(u"Command", self.root).pack()

    # Create needed gui variables 
    self.servecmd     = StringVar()
    self.peercmd      = StringVar()
    self.username     = StringVar()
    self.username2    = StringVar()
    self.chat_message = StringVar()
    self.auth_code    = StringVar()
    self.email        = StringVar()
    self.friend_url   = StringVar()

    # Set initial command values
    self.servecmd.set(u"Register")
    self.peercmd.set(u"Friend")

    # Shutdown method
    self.root.protocol("WM_DELETE_WINDOW", lambda: shutdown(self.root))

  def add_command_elements(self, server_command, peer_command):
    # Create frame for command menu buttons
    frame = self.gb.createFrame(self.root)
    frame.pack()
    
    # Server command drop down and send button
    self.gb.createMenuButton(self.servecmd, [u"Register", u"Query", u"Logout"], frame).grid(row=0, column=0)
    self.gb.createButton(u"Send (server)", lambda: server_command(self.servecmd.get().upper(), self.username.get()), frame).grid(row=0, column=1)
    
    # Client command drop down and send button
    self.gb.createMenuButton(self.peercmd, [u"Friend", u"Request", u"Relay", u"Get"], frame).grid(row=1, column=0)# Took Chat command out
    self.gb.createButton(u"Send (client)", lambda: peer_command(self.peercmd.get().upper(), self.username.get(), self.username2.get()), frame).grid(row=1, column=1)    

  def add_input_elements(self):
    # Create frame for chat input and send button
    frame = self.gb.createFrame(self.root)
    frame.pack()

    # First username label 
    user1 = self.gb.createLabel(u"Username 1", frame)
    user1.grid(row=0, column=0)
    user1.config(width=10)
    
    # Create input for first username
    self.gb.createInput(self.username, frame).grid(row=0, column=1)

    # Second username label
    user2 = self.gb.createLabel(u"Username 2", frame)
    user2.grid(row=1, column=0)
    user2.config(width=10)

    # Create input for second username
    self.gb.createInput(self.username2, frame).grid(row=1, column=1)

  def add_chat_elements(self, chat_command):
    # Chat message label
    self.gb.createLabel(u"Chat Message, if neccessary (requires username)", self.root).pack()

    # Create frame for chat messaging input and label
    frame = self.gb.createFrame(self.root)
    frame.pack()

    # Chat input and send button
    self.gb.createInput(self.chat_message, frame).pack(side=LEFT)
    self.gb.createButton(u"Send Message", lambda: chat_command(self.chat_message.get(), self.username.get()), frame).pack(side=RIGHT)    

    # Chat messages log box
    self.gb.createLabel(u"Chat Messages", self.root).pack()
    self.chatbox = self.gb.createLogBox(self.root)

  def add_log_box(self):
    # General event log box
    self.gb.createLabel(u"Client Log Messages", self.root).pack()
    self.listbox = self.gb.createLogBox(self.root)

  def add_drive_elements(self, link_dropbox):
    # Dropbox frame
    frame = self.gb.createFrame(self.root)
    frame.pack()

    # Auth code label
    self.gb.createLabel(u"Google Drive Auth Code", frame).pack()

    # Google Drive auth code input
    self.gb.createInput(self.auth_code, frame).pack(side = LEFT)

    # Link google drive button
    self.gb.createButton(u"Link Account", lambda: link_dropbox(self.auth_code.get()), frame).pack(side = RIGHT)

  def add_request_elements(self, request_friend):
    # Dropbox frame
    frame = self.gb.createFrame(self.root)
    frame.pack()

    # Auth code label
    self.gb.createLabel(u"Friends email address", frame).pack()

    # Dropbox auth code input
    self.gb.createInput(self.email, frame).pack(side = LEFT)

    # Link dropbox button
    self.gb.createButton(u"Give Permission", lambda: request_friend(self.email.get()), frame).pack(side = RIGHT)

  def add_upload_elements(self, upload_profile):
    self.gb.createButton(u"Update Profile", lambda: upload_profile(), self.root).pack()

  def add_accept_friend_elements(self, accept_friend):
    frame = self.gb.createFrame(self.root)
    frame.pack()
    self.gb.createLabel(u"Link sent to you from a friend", frame).pack()    # Auth code label
    self.gb.createInput(self.friend_url, frame).pack(side = LEFT)           # Dropbox auth code input
    self.gb.createButton(u"Accept", lambda: accept_friend(self.friend_url.get()), frame).pack(side = RIGHT)    # Link dropbox button

  # Log messages when events happen
  def log(self, message):
    self.listbox.insert(END, message)
    self.listbox.see(END)

  # Log chat messages 
  def log_message(self, message): 
    self.chatbox.insert(END, message)
    self.chatbox.see(END)

  # Start the GUI event loop
  def start(self):
    self.root.mainloop()
