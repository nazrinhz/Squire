import random
import time
import json
from iotc.models import Command, Property
from iotc import IoTCClient, IOTCConnectType, IOTCEvents
from pprint import pprint
import tkinter
import sys
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

scope_id = '0ne00ADFF24'
device_id = 'znvog4j7bm'
device_key = '9QClbv6uFfoqr4uuIUe0rbz/ILe2tLu2hXO4NtB0HmI='


def on_commands(command: Command):
  print(f"{command.name} command was sent")
  match command.name:
    case "SendData":
      pprint(vars(command))
    case "roll":
      roll(command.value, True)
    case "feature":
      print(command.value)
      # print(type(command.value))
      feature(command.value["filepath"], command.value["featurename"], command.value["view"])
    case "image":
      spl_pl = command.value.split(" ")
      image(spl_pl[0], spl_pl[1])

  iotc.send_property({"LastCommandReceived": command.name})
  command.reply()

def roll(die_string, view):
  literals = die_string.split(" ")
  print(literals)
  for token in literals:
    if token.find("+") != -1:
      value = roll(token, view)
    pass
  # return literals

def feature(filepath, name, view):
  print("here")
  with open(filepath) as file:
    filejson = json.load(file)
    obj_list = filejson["spell"]
    featurejson = next((x for x in obj_list if x["name"] == name), None)
    print(next((x for x in obj_list if x["name"] == name), None))
    features = tkinter.Label(master, text=featurejson)
    features.pack()
    # type(filejson[0])
    # go from printing to putting on a widget
    # print(file.readline())
  pass

def image(filepath, view):
  # load from string
  pass

def database(action, filepath, view):
  # if add, do this

  # if remove, do this
  pass

def combat(action):
  # show/hide info
  pass

# feature("./5etools/data/spells/spells-phb.json","Magic Missile", True)

iotc = IoTCClient(device_id, scope_id, IOTCConnectType.IOTC_CONNECT_DEVICE_KEY,device_key)

iotc.connect()

iotc.on(IOTCEvents.IOTC_COMMAND, on_commands)

iotc.send_property({"LastTurnedOn": time.time()})

#create main window
master = tkinter.Tk()
master.title("tester")
master.geometry("300x100")


#make a label for the window
label1 = tkinter.Label(master, text='Features!!')
# Lay out label
label1.pack()

# Run forever!
master.mainloop()
while iotc.is_connected():
  time.sleep(60)
