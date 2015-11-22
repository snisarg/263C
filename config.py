import yaml

config_file = open('config/simple.yaml')
config_map = yaml.safe_load(config_file)
config_file.close()


def grid_width():
    return config_map['grid']['width']


def grid_height():
    return config_map['grid']['height']


def cell_pixel_width():
    return config_map['grid']['cell']['width']


def cell_pixel_height():
    return config_map['grid']['cell']['height']


def single_obstacle_count():
    return config_map['obstacles']['single']


def render_refresh_clock_ticks():
    return int(config_map['clock']['ticks'])

