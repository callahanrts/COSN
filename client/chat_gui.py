from Tkinter import * 
from socket import *
import pickle

# Append paths
sys.path.append(u'../extras')

from gui_builder import * 

class ChatWindow(object):
  def __init__(self, title, shutdown):
    self.gb = GuiBuilder()
    self.root = Tk()
