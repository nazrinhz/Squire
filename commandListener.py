import random
import time
import json
from iotc.models import Command, Property
from iotc import IoTCClient, IOTCConnectType, IOTCEvents
from pprint import pprint
import tkinter
import sys
import os
from PIL import ImageTk, Image

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
      roll(command.value["quantity"], command.value["numofsides"],command.value["modifier"], command.value["publicprivate"], command.value["showhide"])
    case "feature":
      print(command.value)
      # print(type(command.value))
      feature(command.value["filepath"], command.value["featurename"], command.value["view"])
    case "image":
      image(command.value["filepath"], command.value["view"])

  iotc.send_property({"LastCommandReceived": command.name})
  command.reply()

def roll(quantity,sides,mod,pub, view):
  sum = mod
  i = 0
  for i in quantity:
    sum += random.randint(1,sides)
  output = "The total roll of " + quantity + "d" + sides + "+" + mod + "is: " + sum 
  total = tkinter.Label(master, text=output)
  total.pack() 
  pass
  # return literals

def feature(filepath, name, view):
  print("here")
  with open(filepath) as file:
    filejson = json.load(file)
    obj_list = filejson["spell"]
    featurejson = next((x for x in obj_list if x["name"] == name), None)
    print(next((x for x in obj_list if x["name"] == name), None))
    feature_box = tkinter.Frame()
    name = tkinter.Label(feature_box, text=featurejson["name"])

    features = tkinter.Label(master, text=featurejson)
    features.pack()
    # type(filejson[0])
    # go from printing to putting on a widget
    # print(file.readline())
  pass

def image(filepath, view):
  print(filepath)
  # load from string
  image_ = Image.open(filepath)
  image_ = image_.resize((256, 256))
  img = ImageTk.PhotoImage(image_)
  img_label = tkinter.Label(master, image=img)
  img_label.image = img
  img_label.pack()
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

#create main window
master = tkinter.Tk()
master.title("tester")
master.geometry("1200x1200")


#make a label for the window
label1 = tkinter.Label(master, text='Features!!')
# Lay out label
label1.pack()

# feature("./5etools/data/spells/spells-phb.json","Magic Missile", True)
# image("5etools/MM/Aarakocra.png", True)

# Run forever!
master.mainloop()

while iotc.is_connected():
  time.sleep(60)
