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
  def __init__(self, event_listener):
    self.gb = GuiBuilder()
    self.root = Tk()
    self.listbox = None

    self.initMainWindow(event_listener)

  # Create the main window
  def initMainWindow(self, event_listener):
    self.gb.setTitle("username", self.root)
    self.gb.setGeometry("300x300", self.root)

    self.gb.createLabel("Command", self.root)
    self.command = StringVar()
    self.command.set("Register")
    self.gb.createMenuButton(self.command, self.root)

    self.gb.createLabel("Username, if neccessary", self.root)

    self.username = StringVar()
    self.gb.createInput(self.username, self.root)

    self.gb.createButton("Send", lambda: event_listener(self.command.get().upper(), self.username.get()), self.root).pack()

    self.gb.createLabel("Client Log Messages", self.root)
    self.listbox = self.gb.createLogBox(self.root)

  # Functions to control GUI Elements
  def log(self, message):
    self.listbox.insert(END, message)

  # Start the GUI event loop
  def start(self):
    self.root.mainloop()
