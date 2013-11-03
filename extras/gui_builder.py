from Tkinter import *

class GuiBuilder(object):
  def __init__(self):
    tmp = None

  # Set window attributes
  def setTitle(self, title, window):
    window.title(title)

  def setGeometry(self, geo_str, window):
    window.geometry(geo_str)

  # Create widgets
  def createLabel(self, lbl_str, window):
    return Label(window, text = lbl_str, anchor=W, width=40)

  def createMenuButton(self, cmd_var, options, window):
    option = OptionMenu(window, cmd_var, *options)
    option.config(width=10)
    return option

  def createInput(self, textVar, window):
    return Entry(window, textvariable = textVar, width=30)

  def createButton(self, lbl, cmd, window):
    return Button(window, text= lbl, command = cmd)

  def createFrame(self, window):
    return Frame(window)

  def createLogBox(self, window):
    frame = self.createFrame(window)
    frame.config(width=65, height=4)
    frame.pack()
    sb = Scrollbar(frame)
    sb.pack(side=RIGHT, fill=Y, pady=(0, 10), padx=(0, 10))

    log_box = Listbox(frame)
    log_box.config(width=65, height=4)
    log_box.pack(padx=(10, 0), pady=(0, 10))
    return log_box