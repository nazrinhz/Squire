import random
import time
import json
from iotc.models import Command, Property
from iotc import IoTCClient, IOTCConnectType, IOTCEvents
from pprint import pprint

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
      feature(command.value["filepath"], command.value["feature name"], command.value["view"])
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
    print(filejson[0])
    type(filejson[0])
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



iotc = IoTCClient(device_id, scope_id, IOTCConnectType.IOTC_CONNECT_DEVICE_KEY,device_key)

iotc.connect()

iotc.on(IOTCEvents.IOTC_COMMAND, on_commands)

iotc.send_property({"LastTurnedOn": time.time()})

while iotc.is_connected():
  time.sleep(60)
