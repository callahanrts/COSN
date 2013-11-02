from tkinter import * 
from socket import *
import pickle

# Append paths
sys.path.append('../extras')

from gui_builder import * 

class MainWindow:
  def __init__(self, server_command, peer_command, chat_command, title, link_dropbox):
    self.gb = GuiBuilder()
    self.root = Tk()
    self.initMainWindow(server_command, peer_command, chat_command, title, link_dropbox)

  # Create the main window
  def initMainWindow(self, server_command, peer_command, chat_command, title, link_dropbox):
    # Configure window settings
    self.gb.setTitle(title, self.root)
    self.gb.setGeometry("400x475", self.root)

    # Command label
    self.gb.createLabel("Command", self.root).pack()

    # Create needed gui variables 
    self.servecmd = StringVar()
    self.peercmd = StringVar()
    self.username = StringVar()
    self.username2 = StringVar()
    self.chat_message = StringVar()
    self.auth_code = StringVar()

    # Set initial command values
    self.servecmd.set("Register")
    self.peercmd.set("Friend")

    # Create frame for command menu buttons
    frame = self.gb.createFrame(self.root)
    frame.pack()
    
    # Server command drop down and send button
    self.gb.createMenuButton(self.servecmd, ["Register", "Query", "Logout"], frame).grid(row=0, column=0)
    self.gb.createButton("Send (server)", lambda: server_command(self.servecmd.get().upper(), self.username.get()), frame).grid(row=0, column=1)
    
    # Client command drop down and send button
    self.gb.createMenuButton(self.peercmd, ["Friend", "Request", "Relay", "Get"], frame).grid(row=1, column=0)# Took Chat command out
    self.gb.createButton("Send (client)", lambda: peer_command(self.peercmd.get().upper(), self.username.get(), self.username2.get()), frame).grid(row=1, column=1)    

    # Create frame for chat input and send button
    input_frame = self.gb.createFrame(self.root)
    input_frame.pack()

    # First username label 
    user1 = self.gb.createLabel("Username 1", input_frame)
    user1.grid(row=0, column=0)
    user1.config(width=10)
    
    # Create input for first username
    self.gb.createInput(self.username, input_frame).grid(row=0, column=1)

    # Second username label
    user2 = self.gb.createLabel("Username 2", input_frame)
    user2.grid(row=1, column=0)
    user2.config(width=10)

    # Create input for second username
    self.gb.createInput(self.username2, input_frame).grid(row=1, column=1)

    # Chat message label
    self.gb.createLabel("Chat Message, if neccessary (requires username)", self.root).pack()

    # Create frame for chat messaging input and label
    frame2 = self.gb.createFrame(self.root)
    frame2.pack()

    # Chat input and send button
    self.gb.createInput(self.chat_message, frame2).pack(side=LEFT)
    self.gb.createButton("Send Message", lambda: chat_command(self.chat_message.get(), self.username.get()), frame2).pack(side=RIGHT)    

    # Chat messages log box
    self.gb.createLabel("Chat Messages", self.root).pack()
    self.chatbox = self.gb.createLogBox(self.root)

    # General event log box
    self.gb.createLabel("Client Log Messages", self.root).pack()
    self.listbox = self.gb.createLogBox(self.root)

    # Dropbox frame
    frame3 = self.gb.createFrame(self.root)
    frame3.pack()

    # Auth code label
    self.gb.createLabel("Dropbox Auth Code", frame3).pack()

    # Dropbox auth code input
    self.gb.createInput(self.auth_code, frame3).pack(side = LEFT)

    # Link dropbox button
    self.gb.createButton("Link Dropbox", lambda: link_dropbox(self.auth_code.get()), frame3).pack(side = RIGHT)


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
