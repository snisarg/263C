import yaml
import os

config_file = open(os.path.dirname(__file__)+('/config/simple.yaml'))
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


def get_generation_size():
    return int(config_map['clock']['generation_size'])


def predator_count():
    return int(config_map['animats']['count']['predator'])


def easy_prey_count():
    return int(config_map['animats']['count']['easy_prey'])


def hard_prey_count():
    return int(config_map['animats']['count']['hard_prey'])


def best_predator_count():
    return int(config_map['animats']['count']['best_predator'])


def grass_count():
    return int(config_map['grass'])


def easy_prey_range():
    return int(config_map['animats']['range']['easy_prey'])


def hard_prey_range():
    return int(config_map['animats']['range']['hard_prey'])


def predator_range():
    return int(config_map['animats']['range']['predator'])


def easy_prey_speed():
    return int(config_map['animats']['speed']['easy_prey'])


def hard_prey_speed():
    return int(config_map['animats']['speed']['hard_prey'])


def predator_speed():
    return int(config_map['animats']['speed']['predator'])

