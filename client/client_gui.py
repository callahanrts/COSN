from tkinter import * 
from socket import *
import pickle

# Append paths
sys.path.append('../extras')
sys.path.append('../server')
sys.path.append('../client')

from gui_builder import * 

class MainWindow:
  def __init__(self, server_command, peer_command, chat_command, title):
    self.gb = GuiBuilder()
    self.root = Tk()
    self.listbox = None
    self.chatbox = None
    self.initMainWindow(server_command, peer_command, chat_command, title)

  # Create the main window
  def initMainWindow(self, server_command, peer_command, chat_command, title):
    self.gb.setTitle(title, self.root)
    self.gb.setGeometry("400x400", self.root)

    self.gb.createLabel("Command", self.root).pack()
    self.servecmd = StringVar()
    self.servecmd.set("Register")
    self.peercmd = StringVar()
    self.peercmd.set("Friend")

    frame = self.gb.createFrame(self.root)
    frame.pack()
    
    self.gb.createMenuButton(self.servecmd, ["Register", "Query", "Logout"], frame).grid(row=0, column=0)
    self.gb.createButton("Send (server)", lambda: server_command(self.servecmd.get().upper(), self.username.get()), frame).grid(row=0, column=1)
    self.gb.createMenuButton(self.peercmd, ["Friend", "Request", "Relay", "Get"], frame).grid(row=1, column=0)# Took Chat command out
    self.gb.createButton("Send (client)", lambda: peer_command(self.peercmd.get().upper(), self.username.get(), self.username2.get()), frame).grid(row=1, column=1)    

    input_frame = self.gb.createFrame(self.root)
    input_frame.pack()
    user1 = self.gb.createLabel("Username 1", input_frame)
    user1.grid(row=0, column=0)
    user1.config(width=10)
    self.username = StringVar()
    self.gb.createInput(self.username, input_frame).grid(row=0, column=1)

    user2 = self.gb.createLabel("Username 2", input_frame)
    user2.grid(row=1, column=0)
    user2.config(width=10)
    self.username2 = StringVar()
    self.gb.createInput(self.username2, input_frame).grid(row=1, column=1)

    self.gb.createLabel("Chat Message, if neccessary (requires username)", self.root).pack()
    frame2 = self.gb.createFrame(self.root)
    frame2.pack()

    self.chat_message = StringVar()
    self.gb.createInput(self.chat_message, frame2).pack(side=LEFT)
    self.gb.createButton("Send Message", lambda: chat_command(self.chat_message.get(), self.username.get()), frame2).pack(side=RIGHT)    

    self.gb.createLabel("Chat Messages", self.root).pack()
    self.chatbox = self.gb.createLogBox(self.root)

    self.gb.createLabel("Client Log Messages", self.root).pack()
    self.listbox = self.gb.createLogBox(self.root)

  # Functions to control GUI Elements
  def log(self, message):
    self.listbox.insert(END, message)
    self.listbox.see(END)

  def log_message(self, message): 
    self.chatbox.insert(END, message)
    self.chatbox.see(END)

  # Start the GUI event loop
  def start(self):
    self.root.mainloop()
