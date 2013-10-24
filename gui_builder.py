from tkinter import *

class GuiBuilder:
  def __init__(self):
    tmp = None

  # Set window attributes
  def setTitle(self, title, window):
    window.title(title)

  def setGeometry(self, geo_str, window):
    window.geometry(geo_str)

  # Create widgets
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

  def createLogBox(self, window):
    sb = Scrollbar(window)
    sb.pack(side=RIGHT, fill=Y, pady=(0, 10), padx=(0, 10))

    log_box = Listbox(window)
    log_box.config(width=65, height=15)
    log_box.pack(padx=(10, 0), pady=(0, 10))
    return log_box