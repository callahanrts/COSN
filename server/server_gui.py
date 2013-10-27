from tkinter import * 
from socket import *

class ServerGui:
  def __init__(self, ping_command):
    self.root = Tk()
    self.setTitle("Server")
    self.setGeometry("400x420")
    self.initServerLabel("Server Log Messages")
    self.initListBox()
    self.username = StringVar()

    frame = Frame(self.root)
    frame.pack()
    Entry(frame, textvariable = self.username, width=30).pack(side=LEFT)
    Button(frame, text= "Ping User", command = lambda: ping_command(self.username.get())).pack(side=RIGHT)

  def setTitle(self, title):
    self.root.title(title)

  def setGeometry(self, geo_str):
    self.root.geometry(geo_str)

  def initServerLabel(self, lbl_str):
    Label(self.root, text = lbl_str).pack()

  def initListBox(self):  
    scrollbar = Scrollbar(self.root)
    scrollbar.pack(side=RIGHT, fill=Y, pady=(0, 10), padx=(0, 10))

    self.listbox = Listbox(self.root)
    self.listbox.config(width=100, height=20)
    self.listbox.pack(padx=(10, 0), pady=(0, 10))

    # attach listbox to scrollbar
    self.listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=self.listbox.yview)

  def log(self, message):
    self.listbox.insert(END, message)

  def start(self):
    self.root.mainloop()
