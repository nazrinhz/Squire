import requests
import random
import time

from iotc.models import Command, Property
from iotc import IoTCClient, IOTCConnectType, IOTCEvents

iotc_sub_domain = "custom-2jfbg7ldg76"
scope_id = '0ne00ADFF24'
device_id = 'ev60wc1npj'
device_key = 'OExra/nYDMqhW1UrD6CKMk2Ruq+O6dX2RvUvcGn+rzM='

sender_id = 'znvog4j7bm'
api_key = "SharedAccessSignature sr=49c3d3e0-9e6b-4c2a-b6ca-7c0a9e1dffe5&sig=0%2B2sZFGkGRMvqgEDvFZq26%2F0%2BzeuzMVCP31fcG44%2FmY%3D&skn=Lab6&se=1727897016818"
current_command = "SendData" # change to feature

def _command_url():
    return f"https://{iotc_sub_domain}.azureiotcentral.com/api/devices/{sender_id}/commands/{current_command}?api-version=2022-05-31&"

def _headers():
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    return headers
    
def send_command(command, request):
    global current_command
    current_command = command
    # print(_command_url())
    resp = requests.post(
        _command_url(),
        json={"request": request},
        headers=_headers()
    )
    print(resp.json())

iotc = IoTCClient(
    device_id,
    scope_id,
        IOTCConnectType.IOTC_CONNECT_DEVICE_KEY,
        device_key)


iotc.connect()

iotc.send_property({
    "LastTurnedOn": time.time()
})

#if iotc.is_connected():
# send_command("roll", "1d6")
send_command("feature", {"filepath":"./5etools/data/spells/spells-phb.json", "featurename":"Magic Missile", "view":True})
send_command("feature", {"filepath":"5etools/MM/Aarakocra.png", "view":True})
# print (_command_url())
time.sleep(4)