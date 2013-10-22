from tkinter import * 
from socket import *


class ClientGui:
  ############################################
  # Initialize gui class with main window
  ############################################
  def __init__(self):
    self.root = Tk()
    self.chat_message = StringVar()
    self.messaging = IntVar()
    self.listbox = None
    self.chatbox = None
    self.win = None

    self.setTitle("username", self.root)
    self.setGeometry("300x300", self.root)

    self.createLabel("Command", self.root)
    self.command = StringVar()
    self.command.set("Register")
    self.createMenuButton(self.command, self.root)

    self.createLabel("Username, if neccessary", self.root)

    self.username = StringVar()
    self.createInput(self.username, self.root)

    self.createButton("Send", self.openChatMenu, self.root).pack()

    self.createLabel("Client Log Messages", self.root)
    self.createLogBox(self.listbox, self.root)
  ############################################
  # Set configurations for windows
  ############################################

  def setTitle(self, title, window):
    window.title(title)

  def setGeometry(self, geo_str, window):
    window.geometry(geo_str)

  ############################################
  # Create different types of widgets most of 
  # which return the widget created
  ############################################
  def createLabel(self, lbl_str, window):
    return Label(window, text = lbl_str, anchor=W, width=30).pack()

  def createMenuButton(self, cmd_var, window):
    option = OptionMenu(window, cmd_var, "Register", "Query", "Logout", "Ping", "Friend", "Chat", "Request", "Get")
    option.config(width=10)
    option.pack()
    return option

  def createInput(self, textVar, window):
    return Entry(window, textvariable = textVar, width=30).pack()

  def createButton(self, lbl, cmd, window):
    return Button(window, text= lbl, command = cmd)

  def createFrame(self, window):
    return Frame(window)

  def createLogBox(self, log_box, window):
    sb = Scrollbar(window)
    sb.pack(side=RIGHT, fill=Y, pady=(0, 10), padx=(0, 10))

    log_box = Listbox(window)
    log_box.config(width=65, height=15)
    log_box.pack(padx=(10, 0), pady=(0, 10))


  ############################################
  # Create different windows that will pop up
  ############################################
  def openChatMenu(self):
    self.win = Toplevel()

    self.setGeometry("300x425", self.win)
    self.createLabel("Chat Log Messages", self.win)
    self.createLogBox(self.chatbox, self.win)

    self.createLabel("Chat Message: ", self.win)
    self.createLabel("TERMINATE to quit chat", self.win)

    self.createInput(self.chat_message, self.win)
    frame = self.createFrame(self.win)
    frame.pack()
    self.createButton("Terminate", None, frame).pack(side=LEFT)
    self.createButton("Send", None, frame).pack(side=RIGHT)


  ############################################
  # Start the GUI event loop
  ############################################
  def start(self):
    self.root.mainloop()