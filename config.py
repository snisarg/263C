import yaml

config_file = open('config/simple.yaml')
config_map = yaml.safe_load(config_file)
config_file.close()


def grid_width():
    return config_map['config']['grid']['width']


def grid_height():
    return config_map['config']['grid']['width']


def cell_pixel_width():
    return config_map['config']['grid']['cell']['width']


def cell_pixel_height():
    return config_map['config']['grid']['cell']['height']


def single_obstacle_count():
    return config_map['config']['obstacles']['single']

