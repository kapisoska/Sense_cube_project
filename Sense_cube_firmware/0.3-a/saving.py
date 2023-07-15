import json

def save_sens_dock(value):
    with open('config.json', 'r') as jsonfile:
        config_file = json.load(jsonfile)
        config_file["dock_sense"] = value
        
def save_sens_nodock(value):
    with open('config.json', 'r') as jsonfile:
        config_file = json.load(jsonfile)
        config_file["nodock_sense"] = value