#!/usr/bin/python

import os
import sys
import yaml

from collections import namedtuple

# Config utilities
Config = namedtuple("Config", ["type", "experiment", "size", "rate", "run"])

# Parser of the configuration
class ConfigParser(object):

  MAPPINGS = {"max":"1300", "min":"64"}

  # Init Function, load data from file configuration file
  def __init__(self, config_file):
    # We expect a collection of config lines
    self.configs = []
    # If the config file does not exist - we do not continue
    if os.path.exists(config_file) == False:
        print "Error Config File %s Not Found" % config_file
        sys.exit(-2)
    self.parse_data(config_file)

  # Parse Function, load lines from file and parses one by one
  def parse_data(self, config_file):
    with open(config_file) as f:
      configs = yaml.load(f)
    for config in configs:
      self.configs.append(Config(type=config['type'], experiment=config['experiment'],
                                  size=config['size'], rate=config['rate'], run=config['run']))

  # Configs getter
  def get_configs(self):
    return self.configs

  # Packet getter
  @staticmethod
  def get_packet(config):
    return "%s-%s-%s" %(config.type, config.experiment,
      ConfigParser.MAPPINGS[config.size])




    