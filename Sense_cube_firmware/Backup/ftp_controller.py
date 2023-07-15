import json

def enable_ftp():
    with open("config.json", "r") as config_file:
        data = json.load(config_file)

    if data["start_ftp"] == False:
        with open("config.json", "w") as config_file:
                data["start_ftp"] = True
                print("set to true")
                json.dump(data, config_file)


def disable_ftp():
    with open("config.json", "r") as config_file:
        data = json.load(config_file)

    if data["start_ftp"]:
        with open("config.json", "w") as config_file:
                data["start_ftp"] = False
                print("set to false")
                json.dump(data, config_file)



#enable_ftp()
#disable_ftp()
