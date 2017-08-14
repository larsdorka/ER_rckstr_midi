import json

# configuration parameters in config.json
# FULL_SCREEN = false   # set to false to display in 1024/768 window
# MIDI_DEVICE_ID = -1   # set to -1 to use default device
# SHOW_DEBUG = true     # set to true to render debug info on the screen
# CHORD = [1, 4, 9]     # chord as list of keys to verify midi data against

STD_CONFIG_DATA = {'FULL_SCREEN': False,
                   'MIDI_DEVICE_ID': -1,
                   'SHOW_DEBUG': True,
                   'CHORD': [1, 4, 9]}


class Configuration:
    """class for storing and persistence of application configuration"""

    def __init__(self, debug_log=dict()):
        """constructor
        :param debug_log: dictionary to write log entries into
        """
        self.debug_log = debug_log
        self.debug_log['config'] = ""
        self.debug_log['config_chord'] = ""
        self.config_data = None
        self.config_file_path = ""

    def load(self, config_file_path="config.json"):
        """loads the configuration file and decodes the json content
        :param config_file_path:
        """
        self.config_file_path = config_file_path
        self.config_data = {}
        file_data = {}
        try:
            with open(self.config_file_path) as file:
                file_data = json.load(file)
        except Exception as ex:
            self.debug_log['config'] = "error on reading config file: " + str(ex)
        try:
            for key in STD_CONFIG_DATA:
                self.config_data[key] = file_data[key]
        except KeyError:
            self.debug_log['config'] = "error on reading config data"
            self.config_data = {}
        if not self.config_data:
            self.create_std_config()
        self.debug_log['config_chord'] = "solution chord:"
        for key in self.config_data['CHORD']:
            self.debug_log['config_chord'] += " " + str(key)

    def get_config(self, key=""):
        """returns the value for the given key from the configuration data
        :param key: the key to the config property
        :return: the value of the config property
        """
        value = ""
        try:
            value = self.config_data[key]
        except KeyError:
            self.debug_log['config'] = "error on reading config data: key {} not found".format(key)
        return value

    def set_config(self, key, value):
        """sets a given key/value pair into the configuration data
        :param key: the key to the config property
        :param value: the value to the config property
        """
        if key != "":
            self.config_data[key] = value

    def save(self):
        """encodes the json content and saves the configuration file"""
        if self.config_file_path != "":
            json_config = json.dumps(self.config_data, indent=2)
            with open(self.config_file_path, 'w', encoding='utf-8') as file:
                try:
                    file.write(json_config)
                except Exception as ex:
                    self.debug_log['config'] = "error on writing config data: " + str(ex)

    def create_std_config(self):
        """creates the standard configuration and stores it to a file"""
        self.config_data = STD_CONFIG_DATA
        self.save()
