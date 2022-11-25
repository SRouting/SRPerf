#!/usr/bin/python

import os
import sys
import yaml

from collections import namedtuple

#Line rate mapping - WARNING Some values are random
LINE_RATES = {
  'ipv6':12253000,
  'ipv4':12253000,
  't_encaps_v6':12253000,
  't_encaps_v4':12253000,
  't_encaps_l2':12253000,
  't_insert_v6':12253000,
  'end':6868000,
  'end_x':6868000,
  'end_t':6868000,
  'end_b6':6868000,
  'end_b6_encaps':6868000,
  'end_dx6':6868000,
  'end_dx4':6868000,
  'end_dx2':6377000,
  'end_dt6':6868000,
  'end_ad6':6868000,
  'end_ad4':6868000,
  'end_am':6377000,
  'stamp_reflector_test': 8389262,
  'stamp_sender_test': 8389262,
}

# Config utilities
Config = namedtuple("Config", ["type", "experiment", "size", "rate", "run", "line_rate", "streams", "name"])

# Parser of the configuration
class ConfigParser(object):

  MAPPINGS = {"max":"1300", "min":"64"}

  # Init Function, load data from file configuration file
  def __init__(self, config_file):
    # We expect a collection of config lines
    self.configs = []
    # If the config file does not exist - we do not continue
    if os.path.exists(config_file) == False:
        print("Error Config File %s Not Found" % config_file)
        sys.exit(-2)
    self.parse_data(config_file)

  # Parse Function, load lines from file and parses one by one
  def parse_data(self, config_file):
    with open(config_file) as f:
      configs = yaml.safe_load(f)
    for config in configs:
      if config.get('streams') is not None:
        line_rate = 0
        for stream in config['streams']:
          line_rate += LINE_RATES[stream['experiment']] * stream['percentage'] / 100
      else:
        line_rate=LINE_RATES[config['experiment']]
      self.configs.append(Config(type=config['type'], experiment=config['experiment'],
                                  size=config['size'], rate=config['rate'], run=config['run'],
                                  line_rate=line_rate,
                                  streams=config['streams'] if 'streams' in config else None,
                                  name=config['name'] if 'name' in config else None))

  # Configs getter
  def get_configs(self):
    return self.configs

  # Packet getter
  @staticmethod
  def get_packet(config):
    return "%s-%s-%s" %(config.type, config.experiment,
      ConfigParser.MAPPINGS[config.size])

  # Streams getter
  @staticmethod
  def get_streams(config):
    return config.streams
