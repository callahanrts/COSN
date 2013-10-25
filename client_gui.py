from tkinter import * 
from socket import *
from gui_builder import * 
import pickle

class ChatWindow:
  def __init__(self):
    self.gb = GuiBuilder()
    self.chat_message = StringVar()
    self.chatbox = None
    self.win = None
    self.chat_socket = socket(AF_INET, SOCK_STREAM)

  def initChatMenu(self, user_data, my_username):
    self.win = Toplevel()

    self.gb.setGeometry("300x425", self.win)
    self.gb.setTitle(my_username + " > " + user_data[4], self.win)
    self.gb.createLabel("Chat Log Messages", self.win)
    self.chatbox = self.gb.createLogBox(self.win)

    self.gb.createLabel("Chat Message: ", self.win)
    self.gb.createLabel("TERMINATE to quit chat", self.win)

    self.gb.createInput(self.chat_message, self.win)
    frame = self.gb.createFrame(self.win)
    frame.pack()
    self.gb.createButton("Terminate", None, frame).pack(side=LEFT)
    self.gb.createButton("Send", lambda: self.send_chat(self.chat_message.get()), frame).pack(side=RIGHT)

  def send_chat(self, message, chat_socket):
    return_message = pickle.dumps(message)
    chat_socket.send(return_message)
    print(message)
    print(chat_socket)

  def openChatWindow(self):
    self.initChatMenu()

  def log_message(self, message):
    self.chatbox.insert(END, message)

class MainWindow:
  def __init__(self, server_command, peer_command, title):
    self.gb = GuiBuilder()
    self.root = Tk()
    self.listbox = None

    self.initMainWindow(server_command, peer_command, title)

  # Create the main window
  def initMainWindow(self, server_command, peer_command, title):
    self.gb.setTitle(title, self.root)
    self.gb.setGeometry("300x300", self.root)

    self.gb.createLabel("Command", self.root)
    self.servecmd = StringVar()
    self.servecmd.set("Register")
    self.peercmd = StringVar()
    self.peercmd.set("Friend")

    frame = self.gb.createFrame(self.root)
    frame.pack()
    
    self.gb.createMenuButton(self.servecmd, ["Register", "Query", "Logout"], frame).grid(row=0, column=0)
    self.gb.createButton("Send (server)", lambda: server_command(self.servecmd.get().upper(), self.username.get()), frame).grid(row=0, column=1)
    self.gb.createMenuButton(self.peercmd, ["Friend", "Chat", "Request", "Get"], frame).grid(row=1, column=0)
    self.gb.createButton("Send (client)", lambda: peer_command(self.peercmd.get().upper(), self.username.get()), frame).grid(row=1, column=1)    

    self.gb.createLabel("Username, if neccessary", self.root)

    self.username = StringVar()
    self.gb.createInput(self.username, self.root)

    self.gb.createLabel("Client Log Messages", self.root)
    self.listbox = self.gb.createLogBox(self.root)

  # Functions to control GUI Elements
  def log(self, message):
    self.listbox.insert(END, message)

  # Start the GUI event loop
  def start(self):
    self.root.mainloop()
