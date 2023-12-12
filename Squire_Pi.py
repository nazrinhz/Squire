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

"""Command Callback Function
Description: This function is wired to the command reciever callback of the Azure Device. It reads the command name and value to interpret into one of the other functions contained.
returns:none, but essentially returns another function.
parameters: command:Command (an iotc value to interpret commands from Azure properly)"""
def on_commands(command: Command):
  try:
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
      case "combat":
        if "misc_value" in command.value:
          combat(command.value["action"], command.value["name"], command.value["misc_value"])
        else:
          combat(command.value["action"], command.value["name"], 0)
      case "exit":
        master.destroy()
        exit()
  except Exception as error:
    with open(file="./errors.txt", mode="a") as file:
      file.write(f'Error occurred:\n {str(error)}\nat {time.ctime(time.time())}.\n')
    exit()
    

  iotc.send_property({"LastCommandReceived": command.name})
  command.reply()

"""Roll Dice Function
Description: This function handles the rolling of dice and outputs them as a tkinter widget.
returns:none, but essentially returns a tkinter widget
parameters: quantity:str, sides:str, mod:str, pub:bool, view:bool"""
def roll(quantity,sides,mod,pub, view):
  sum = int(mod)
  for i in range(int(quantity)):
    addend = random.randint(1,int(sides))
    sum += addend
  output = f"The total roll of {quantity}d{sides} + {mod} is:"
  roll_frame = tkinter.Frame(master,height=20,width=20,highlightbackground="black",highlightthickness=2,highlightcolor="black")
  roll_text = tkinter.Label(roll_frame, text=output,font=("Arial", 20))
  roll_value = tkinter.Label(roll_frame, text=str(sum),font=("Arial", 56))
  widgets[0] = roll_frame
  output_window()
  pass
  # return literals

"""Show Feature Function
Description: This function handles the visualizing of features and outputs them as a tkinter widget. Many different features from many different files can be shown and handled.
returns:none, but essentially returns a tkinter widget
parameters: filepath:str, name:str, view:bool"""
def feature(filepath, name, view):
  print("here")
  with open(filepath) as file:
    filejson = json.load(file)
    feature_box = tkinter.Frame(master, height=10,width=50,highlightbackground="black",highlightthickness=2,highlightcolor="black")
    if "spell" in filejson:
      obj_list = filejson["spell"]
      featurejson = next((x for x in obj_list if x["name"] == name), None)
      print(featurejson)
      name = tkinter.Label(feature_box, text=featurejson["name"], font=("Arial", 20), justify='left',wraplength=500)
      where_in_book = f'{featurejson["source"]} {featurejson["page"]}'
      source = tkinter.Label(feature_box, text=where_in_book, justify='left',wraplength=500)
      if featurejson["level"] == 1:
        spell_info = f'1st-level {get_spell_type(featurejson["school"])}'
      elif featurejson["level"] == 2:
        spell_info = f'2nd-level {get_spell_type(featurejson["school"])}'
      elif featurejson["level"] == 3:
        spell_info = f'3rd-level {get_spell_type(featurejson["school"])}'
      else:
        spell_info = f'{featurejson["level"]}th-level {get_spell_type(featurejson["school"])}'
      level = tkinter.Label(feature_box, text=spell_info, justify='left',wraplength=500)
      casting_time = f'{featurejson["time"][0]["number"]} {featurejson["time"][0]["unit"]}'
      cast_time = tkinter.Label(feature_box, text=casting_time, justify='left',wraplength=500)
      if featurejson["range"]["distance"]["type"] == "self":
        spell_range = f'Range: Self'
      elif featurejson["range"]["distance"]["type"] == "touch":
        spell_range = f'Range: Touch'
      elif featurejson["range"]["distance"]["type"] == "feet":
        spell_range = f'Range: {featurejson["range"]["distance"]["amount"]} feet'
      else:
        spell_range = f'Range: Special'
      range_widget = tkinter.Label(feature_box,text=spell_range, justify='left',wraplength=500)
      comp_text = ''
      first = True
      if "v" in featurejson["components"]:
        comp_text = "Components: V"
        first = False
      if "s" in featurejson["components"]:
        if first:
          comp_text = "Components: S"
          first = False
        else:
          comp_text = comp_text + ", S"
      if "m" in featurejson["components"]:
        if first:
          comp_text = f"Components: M ({featurejson['components']['m']})"
          first = False
        else:
          comp_text = comp_text + f", M ({featurejson['components']['m']})"
      component_widget = tkinter.Label(feature_box,text=comp_text, justify="left", wraplength=500)
      if featurejson["duration"][0]["type"] == "timed":
        dur_text = f'Duration: {featurejson["duration"][0]["duration"]["amount"]} {featurejson["duration"][0]["duration"]["type"]}'
      elif featurejson["duration"][0]["type"] == "instant":
        dur_text = f'Duration: Instantaneous'
      if "concentration" in featurejson["duration"][0]:
        dur_text = dur_text + " (Requires Concentration)"
      dur_widget = tkinter.Label(feature_box,text=dur_text,justify='left',wraplength=500)

      for entry in featurejson["entries"]:
        paragraph = tkinter.Label(feature_box,text=entry, justify='left',wraplength=500)
    elif "classFeature" in filejson or "subclassFeature" in filejson:
      # determine obj_list based on whether the feature is in the mainclass or subclass list of features
      sub_feature = False
      if next((x for x in filejson["classFeature"] if x["name"] == name), None) != None:
        obj_list = filejson["classFeature"]
      else:
        obj_list = filejson["subclassFeature"]
        sub_feature = True
      featurejson = next((x for x in obj_list if x["name"] == name), None)
      print(featurejson)
      name = tkinter.Label(feature_box, text=featurejson["name"], font=("Arial", 20), justify='left',wraplength=500)
      where_in_book = f'{featurejson["source"]} {featurejson["page"]}'
      source = tkinter.Label(feature_box, text=where_in_book, justify='left',wraplength=500)
      if featurejson["level"] == 1:
        level_info = f'1st-level {featurejson["className"]}'
      elif featurejson["level"] == 2:
        level_info = f'2nd-level {featurejson["className"]}'
      elif featurejson["level"] == 3:
        level_info = f'3rd-level {featurejson["className"]}'
      else:
        level_info = f'{featurejson["level"]}th-level {featurejson["className"]}'
      if sub_feature:
        level_info = level_info + f' ({featurejson["subclassShortName"]}) Feature'
      else:
        level_info = level_info + ' Feature'
      level = tkinter.Label(feature_box, text=level_info, justify='left',wraplength=500)

      for entry in featurejson["entries"]:
        paragraph = tkinter.Label(feature_box,text=entry, justify='left',wraplength=500)
      print("class feature")

    elif "feat" in filejson:
      obj_list = filejson["feat"]
      featurejson = next((x for x in obj_list if x["name"] == name), None)
      print(featurejson)
      name = tkinter.Label(feature_box, text=featurejson["name"], font=("Arial", 20), justify='left',wraplength=500)
      where_in_book = f'{featurejson["source"]} {featurejson["page"]}'
      source = tkinter.Label(feature_box, text=where_in_book, justify='left',wraplength=500)
      for entry in featurejson["entries"]:
        if type(entry) == str:
          paragraph = tkinter.Label(feature_box,text=entry, justify='left',wraplength=500)
        elif type(entry) == dict:
          for bullet in entry["items"]:
            point = tkinter.Label(feature_box, text=bullet,justify='left',wraplength=350)
      print("class feature")
      print("fill in feat")
    elif "skill" in filejson:
      obj_list = filejson["skill"]
      featurejson = next((x for x in obj_list if x["name"] == name), None)
      print(featurejson)
      name = tkinter.Label(feature_box, text=featurejson["name"], font=("Arial", 20), justify='left',wraplength=500)
      where_in_book = f'{featurejson["source"]} {featurejson["page"]}'
      source = tkinter.Label(feature_box, text=where_in_book, justify='left',wraplength=500)
      for entry in featurejson["entries"]:
        if type(entry) == str:
          paragraph = tkinter.Label(feature_box,text=entry, justify='left',wraplength=500)
        elif type(entry) == dict:
          for bullet in entry["items"]:
            point = tkinter.Label(feature_box, text=bullet,justify='left',wraplength=350)
      print("fill in skill")
    elif "race" in filejson:
      obj_list = filejson["race"]
      featurejson = next((x for x in obj_list if x["name"] == name), None)
      print(featurejson)
      print("fill in racial")
    elif "something else" in filejson:
      print("fill in")
    
    widgets[1] = feature_box
    output_window()
    # type(filejson[0])
    # go from printing to putting on a widget
    # print(file.readline())
  pass

"""Get Spell Type Function
Description: This function makes the formatting for spells easier.
returns:string representing the full lowercase name of a spell school
parameters: school:str"""
def get_spell_type(school):
  if school == "A":
    return "abjuration"
  elif school == "C":
    return "conjuration"
  elif school == "D":
    return "divination"
  elif school == "E":
    return "enchantment"
  elif school == "V":
    return "evocation"
  elif school == "I":
    return "illusion"
  elif school == "N":
    return "necromancy"
  elif school == "T":
    return "transmutation"
  else:
    return "Unknown Spell Type"

"""Show Image Function
Description: This function handles the showing of an image and outputs it as a tkinter widget.
returns:none, but essentially returns a tkinter widget
parameters: filepath:str, view:bool"""
def image(filepath, view):
  print(filepath)
  # load from string
  image_ = Image.open(filepath)
  image_ = image_.resize((512, 512))
  img = ImageTk.PhotoImage(image_)
  widgets[2] = tkinter.Label(master, image=img)
  widgets[2].image = img
  output_window()

"""Combat Function
Description: This function handles the various combat actions and outputs them as a tkinter widget.
returns:none, but essentially returns a tkinter widget
parameters: action:str, name:str, misc_value:str"""
def combat(action, name, misc_value):
  initiative_list = widgets[3].winfo_children()
  initiative_frame = tkinter.Frame(master, height=50, width=10,highlightbackground="black",highlightthickness=2,highlightcolor="black")

  header_entry = tkinter.Frame(initiative_frame)
  header_text = tkinter.Label(header_entry,text="Initiative Count",wraplength=100,font=("Arial", 20))
  header_name = tkinter.Label(header_entry,text="Name",font=("Arial", 20))
  header_hp = tkinter.Label(header_entry,text="Hit Points",font=("Arial", 20))
  header_cond = tkinter.Label(header_entry,text="Conditions",font=("Arial", 20))

  match action:
    case "hp":
      # change HP value
      for widget in initiative_list:
        if widget.winfo_children()[1].cget("text") == name: # if a widget value somewhere is the same as the player's name, change the value and break
          new_entry = tkinter.Frame(initiative_frame)
          new_text = tkinter.Label(new_entry, text=widget.winfo_children()[0].cget("text"),font=("Arial", 18))
          new_name = tkinter.Label(new_entry,text=widget.winfo_children()[1].cget("text"),font=("Arial", 18))
          new_hp = tkinter.Label(new_entry,text=str(misc_value),font=("Arial", 18))
          new_cond = tkinter.Label(new_entry,text=widget.winfo_children()[3].cget("text"),font=("Arial", 18))
        elif widget.winfo_children()[1].cget("text") != "Name": # compare initiative values here
          new_entry = tkinter.Frame(initiative_frame)
          new_text = tkinter.Label(new_entry, text=widget.winfo_children()[0].cget("text"),font=("Arial", 18))
          new_name = tkinter.Label(new_entry,text=widget.winfo_children()[1].cget("text"),font=("Arial", 18))
          new_hp = tkinter.Label(new_entry,text=widget.winfo_children()[2].cget("text"),font=("Arial", 18))
          new_cond = tkinter.Label(new_entry,text=widget.winfo_children()[3].cget("text"),font=("Arial", 18))
      pass
    case "condition":
      # change conditions of thing
      for widget in initiative_list:
        if widget.winfo_children()[1].cget("text") == name: # if a widget value somewhere is the same as the player's name, change the value and break
          new_entry = tkinter.Frame(initiative_frame)
          new_text = tkinter.Label(new_entry, text=widget.winfo_children()[0].cget("text"),font=("Arial", 18))
          new_name = tkinter.Label(new_entry,text=widget.winfo_children()[1].cget("text"),font=("Arial", 18))
          new_hp = tkinter.Label(new_entry,text=widget.winfo_children()[2].cget("text"),font=("Arial", 18))
          new_cond = tkinter.Label(new_entry,text=str(misc_value),font=("Arial", 18))
        elif widget.winfo_children()[1].cget("text") != "Name": # compare initiative values here
          new_entry = tkinter.Frame(initiative_frame)
          new_text = tkinter.Label(new_entry, text=widget.winfo_children()[0].cget("text"),font=("Arial", 18))
          new_name = tkinter.Label(new_entry,text=widget.winfo_children()[1].cget("text"),font=("Arial", 18))
          new_hp = tkinter.Label(new_entry,text=widget.winfo_children()[2].cget("text"),font=("Arial", 18))
          new_cond = tkinter.Label(new_entry,text=widget.winfo_children()[3].cget("text"),font=("Arial", 18))
      pass
    case "remove conditions":
      # change conditions of thing
      for widget in initiative_list:
        if widget.winfo_children()[1].cget("text") == name: # if a widget value somewhere is the same as the player's name, change the value and break
          new_entry = tkinter.Frame(initiative_frame)
          new_text = tkinter.Label(new_entry, text=widget.winfo_children()[0].cget("text"),font=("Arial", 18))
          new_name = tkinter.Label(new_entry,text=widget.winfo_children()[1].cget("text"),font=("Arial", 18))
          new_hp = tkinter.Label(new_entry,text=widget.winfo_children()[2].cget("text"),font=("Arial", 18))
          new_cond = tkinter.Label(new_entry,text='---',font=("Arial", 18))
        elif widget.winfo_children()[1].cget("text") != "Name": # compare initiative values here
          new_entry = tkinter.Frame(initiative_frame)
          new_text = tkinter.Label(new_entry, text=widget.winfo_children()[0].cget("text"),font=("Arial", 18))
          new_name = tkinter.Label(new_entry,text=widget.winfo_children()[1].cget("text"),font=("Arial", 18))
          new_hp = tkinter.Label(new_entry,text=widget.winfo_children()[2].cget("text"),font=("Arial", 18))
          new_cond = tkinter.Label(new_entry,text=widget.winfo_children()[3].cget("text"),font=("Arial", 18))
      pass
    case "initiative":
      in_list = False
      # add or change someone's init
      # if widget with name does not exist, make one
      for widget in initiative_list:
        if widget.winfo_children()[1].cget("text") == name: # if a widget value somewhere is the same as the player's name, change the value and break
          new_entry = tkinter.Frame(initiative_frame)
          new_text = tkinter.Label(new_entry, text=str(misc_value),font=("Arial", 18))
          new_name = tkinter.Label(new_entry,text=widget.winfo_children()[1].cget("text"),font=("Arial", 18))
          new_hp = tkinter.Label(new_entry,text=widget.winfo_children()[2].cget("text"),font=("Arial", 18))
          new_cond = tkinter.Label(new_entry,text=widget.winfo_children()[3].cget("text"),font=("Arial", 18))
          in_list = True
        elif widget.winfo_children()[1].cget("text") != "Name": # compare initiative values here
          new_entry = tkinter.Frame(initiative_frame)
          new_text = tkinter.Label(new_entry, text=widget.winfo_children()[0].cget("text"),font=("Arial", 18))
          new_name = tkinter.Label(new_entry,text=widget.winfo_children()[1].cget("text"),font=("Arial", 18))
          new_hp = tkinter.Label(new_entry,text=widget.winfo_children()[2].cget("text"),font=("Arial", 18))
          new_cond = tkinter.Label(new_entry,text=widget.winfo_children()[3].cget("text"),font=("Arial", 18))
      if not in_list:
        initiative_entry = tkinter.Frame(initiative_frame)
        initiative_text = tkinter.Label(initiative_entry,text=str(misc_value),font=("Arial", 18))
        character_name = tkinter.Label(initiative_entry,text=name,font=("Arial", 18))
        character_hp = tkinter.Label(initiative_entry,text="---",font=("Arial", 18))
        character_cond = tkinter.Label(initiative_entry,text="---",font=("Arial", 18))

      # if it does, just change the value
      pass
    case "clear":
      # clears the widget
      pass
  widgets[3] = initiative_frame
  output_window()
  pass

iotc = IoTCClient(device_id, scope_id, IOTCConnectType.IOTC_CONNECT_DEVICE_KEY,device_key)
iotc.connect()
iotc.on(IOTCEvents.IOTC_COMMAND, on_commands)
iotc.send_property({"LastTurnedOn": time.time()})

#create main window
master = tkinter.Tk()
master.title("Squire")
master.geometry("2000x2000")

widgets = [tkinter.Label(master,text="widget 1", height=20,width=20), tkinter.Label(master,text="send a feature command to see it here!", height=20,width=20), tkinter.Label(master,text="widget 3", height=20,width=20), tkinter.Label(master,text="widget 4", height=20,width=20)]

"""Output Window Function
Description: This function properly takes the tkinter widgets and packs them into a constant shape.
returns:none, but essentially returns a tkinter widget
parameters:none"""
def output_window():
  for child in master.winfo_children():
    if child not in widgets:
      child.destroy()
  widgets[0].grid(column=0, row=0)
  for child in widgets[0].winfo_children():
    child.pack()
  widgets[1].grid(column=0,row=1, columnspan=2)
  for child in widgets[1].winfo_children():
    child.pack()
  widgets[2].grid(column=1,row=0)
  for child in widgets[2].winfo_children():
    child.pack()
  widgets[3].grid(column=2,row=0, rowspan=2)
  if len(widgets[3].winfo_children()) >0:
    widgets[3].winfo_children()[0].pack()
    for grandchild in widgets[3].winfo_children()[0].winfo_children():
        grandchild.pack(side="left")

  initiative_list = [(child, float(child.winfo_children()[0].cget("text"))) for child in widgets[3].winfo_children()[1:]]
  init_sorted = sorted(initiative_list, key=lambda x: x[1], reverse=True)
  for child in init_sorted:
    child[0].pack()
    for grandchild in child[0].winfo_children():
      grandchild.pack(side="left")
  pass

#make a label for the window
label1 = tkinter.Label(master, text='Features!!')
# Lay out label
label1.pack()

# feature("./5etools/data/spells/spells-phb.json","Magic Missile", True)
image("5etools/MM/Goblin.png", True)
roll(0,0,0,True,True)
combat("clear", "Fizzcrack", 13)
# combat("initiative", "Varuk", 10)
# feature("./5etools/data/feats.json","Athlete", True)

# Run forever!
master.mainloop()

# while iotc.is_connected():
#   time.sleep(60)
