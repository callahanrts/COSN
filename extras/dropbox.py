#!/usr/local/bin/python2
import cmd
import locale
import os
import pprint
import shlex
import sys

from dropbox import client, rest


class Dropbox:
  def __init__(self):
    # Get your app key and secret from the Dropbox developer website
    self.app_key = '2ycmk3mndjuvija'
    self.app_secret = 'f6v4pvhsirmr5tw'



  def auth_url(self):
    return self.flow.start()

if __name__ == '__main__':
  db = Dropbox()
  #print(db.auth_url())
