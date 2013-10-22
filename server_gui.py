from tkinter import * 

class ServerGui:
  def __init__(self):
    #Connect to server and print message 
    self.server_socket = socket(AF_INET, SOCK_DGRAM)  
    self.server_socket.bind(('', 9000))
    print("(9000) UDP Server Waiting for client...")

    self.root = Tk()
    self.root.setTitle("Server")

  def setTitle(self, title):
    self.root.title(title)

  def setGeometry(self, geo_str):
    root.geometry("300x350")

  def initServerLabel(self, geo_str):
    Label(self.root, text = "Server Log Messages").pack()

  def initListBox(self):  
    scrollbar = Scrollbar(self.root)
    scrollbar.pack(side=RIGHT, fill=Y, pady=(0, 10), padx=(0, 10))

    self.listbox = Listbox(self.root)
    self.listbox.config(width=100, height=100)
    self.listbox.pack(padx=(10, 0), pady=(0, 10))

    # attach listbox to scrollbar
    self.listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=self.listbox.yview)

  def log(self, message):
    self.listbox.insert(END, message)