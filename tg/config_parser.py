#!/usr/bin/python

import os
import sys

from collections import namedtuple

# Config utilities
Config = namedtuple("Config", ["type", "experiment", "size", "rate"])
FILE = "config.txt"

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
      for line in f:
        chunks = line.split("\n")[0].split("\t")
        self.configs.append(Config(type=chunks[0], experiment=chunks[1],
          size=chunks[2], rate=chunks[3]))

  # Configs getter
  def get_configs(self):
    return self.configs

  # Test getter
  @staticmethod
  def get_test(config):
    return "%s-%s-%s" %(config.type, config.experiment,
      ConfigParser.MAPPINGS[config.size])

if __name__ == '__main__':
  parser = ConfigParser(FILE)
  for config in parser.get_configs():
    print config, ConfigParser.get_test(config), config.rate

    