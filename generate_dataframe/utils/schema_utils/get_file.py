import os

def get_yaml_file(config_file):
    yaml_file = os.path.abspath(config_file)
    return yaml_file