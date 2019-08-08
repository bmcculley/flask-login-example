
def parse_config():
    config = configparser.ConfigParser()

    conffile = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "default.cfg")

    try:
        config.read(conffile)
    except:
        # need to setup logging
        print("Config file not found")

    for i in config["Default Configuration"]:
        CONFIG_OPTIONS[i.upper()] = config["Default Configuration"][i.upper()]
