import random
import time
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
      spl_pl = command.value.split(" ")
      feature(spl_pl[0], spl_pl[1]) # change to read object
    case "image":
      spl_pl = command.value.split(" ")
      image(spl_pl[0], spl_pl[1])

  iotc.send_property({"LastCommandReceived": command.name})
  command.reply()

def roll(die_string, view):
  literals = die_string.split(" ")
  print(literals)

def feature(filepath, view):
  with open(filepath) as file:
    print(file.readline)
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
