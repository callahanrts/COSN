from tkinter import * 
from socket import *
from gui_builder import * 

class ChatWindow:
  def __init__(self, event_listener):
    self.gb = GuiBuilder()
    self.chat_message = StringVar()
    self.chatbox = None
    self.win = None

  def initChatMenu(self):
    self.win = Toplevel()

    self.gb.setGeometry("300x425", self.win)
    self.gb.createLabel("Chat Log Messages", self.win)
    self.chatbox = self.gb.createLogBox(self.win)

    self.gb.createLabel("Chat Message: ", self.win)
    self.gb.createLabel("TERMINATE to quit chat", self.win)

    self.gb.createInput(self.chat_message, self.win)
    frame = self.gb.createFrame(self.win)
    frame.pack()
    self.gb.createButton("Terminate", None, frame).pack(side=LEFT)
    self.gb.createButton("Send", None, frame).pack(side=RIGHT)

  def log_message(self, message):
    self.chatbox.insert(END, message)

class MainWindow:
  def __init__(self, server_command, peer_command):
    self.gb = GuiBuilder()
    self.root = Tk()
    self.listbox = None

    self.initMainWindow(server_command, peer_command)

  # Create the main window
  def initMainWindow(self, server_command, peer_command):
    self.gb.setTitle("username", self.root)
    self.gb.setGeometry("300x300", self.root)

    self.gb.createLabel("Command", self.root)
    self.servecmd = StringVar()
    self.servecmd.set("Register")
    self.peercmd = StringVar()
    self.peercmd.set("Friend")

    frame = self.gb.createFrame(self.root)
    frame.pack()
    
    self.gb.createMenuButton(self.servecmd, ["Register", "Query", "Logout"], frame).pack(side=LEFT)
    self.gb.createMenuButton(self.peercmd, ["Friend", "Chat", "Request", "Get"], frame).pack(side=RIGHT)

    self.gb.createLabel("Username, if neccessary", self.root)

    self.username = StringVar()
    self.gb.createInput(self.username, self.root)

    self.gb.createButton("Send", lambda: server_command(self.command.get().upper(), self.username.get()), self.root).pack()

    self.gb.createLabel("Client Log Messages", self.root)
    self.listbox = self.gb.createLogBox(self.root)

  # Functions to control GUI Elements
  def log(self, message):
    self.listbox.insert(END, message)

  # Start the GUI event loop
  def start(self):
    self.root.mainloop()
