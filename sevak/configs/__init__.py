from configparser import ConfigParser
import os

# Returns this folder path : /users/jalotra/XYZ
def get_abs_path():
    return os.path.dirname(os.path.abspath(__file__))

# Returns config file path : /users/jalotra/XYZ/config.ini
def get_config_file_path(): 
    return os.path.join(get_abs_path(), "config.ini")

# Return ConfigParser object
def get_config_parser():
    config = ConfigParser()
    with open(get_config_file_path(), "r") as f:
        config.read_file(f)
    return config