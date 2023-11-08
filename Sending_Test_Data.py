import requests
import random
import time
import pandas as pd
import numpy as np
import pickle

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
    
def send_command():
    resp = requests.post(
        _command_url(),
        json={"request": "goblin deez nuts"},
        headers=_headers()
    )
    print(resp.json())

iotc = IoTCClient(
    device_id,
    scope_id,
        IOTCConnectType.IOTC_CONNECT_DEVICE_KEY,
        device_key)


iotc.connect()

filename = 'X_test.csv'
testing_data = pd.read_csv(filename)

iotc.send_property({
    "LastTurnedOn": time.time()
})

while iotc.is_connected():
    # sample = testing_data.sample(1)
    # with open("iot_model", "rb") as model_file:
    #     model = pickle.load(model_file)
    # y_pred = model.predict(sample)
    # if y_pred[0] == 1:
        # send_command()
    # iotc.send_telemetry(sample.to_dict('records'))
    # iotc.send_telemetry({'RainTomorrow': str(y_pred[0])})
    # time.sleep(random.randint(5,60))
    send_command()
    # print (_command_url())
    time.sleep(4)