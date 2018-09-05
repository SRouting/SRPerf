#!/usr/bin/python

import sys
import json

# We need to add tg modules
sys.path.insert(0, "../tg")

from config_parser import ConfigParser
from pdr import PDR
from mrr import MRR
from ssh_node import SshNode

# Sut node
SUT = "c220g1-031126.wisc.cloudlab.us"
# Sut home
SUT_HOME = "/proj/superfluidity-PG0/linux-srv6-perf/sut"
# Sut configurator
SUT_CONFIGURATOR = "forwarding-behaviour.cfg"
# Sut user
SUT_USER = "pier"
# Sut name
SUT_NAME = "sut"
# Config file
CONFIG_FILE = "config.yaml"
# Results file
RESULTS_FILE = "results.txt"

# Manages the orchestration of the experiments
class Orchestrator(object):

  # Run a defined experiment using the config provided as input
  @staticmethod
  def run():
    # Init steps
    results = {}
    # Establish the connection with the sut
    cfg_manager = SshNode(host=SUT, name=SUT_NAME, username=SUT_USER)
    # Move to the sut home
    cfg_manager.run_command("cd %s" %(SUT_HOME))
    # Let's parse the test plan
    parser = ConfigParser(CONFIG_FILE)
    # Run the experiments according to the test plan:
    for config in parser.get_configs():
      # Get the rate class
      rate_to_evaluate = Orchestrator.factory(config.rate)
      # Enforce the configuration
      cfg_manager.run_command("sudo bash %s %s" %(SUT_CONFIGURATOR, config.experiment))
      # Run the experiments
      values = rate_to_evaluate.run(config)
      # Collect the results
      results[config.experiment] = values
    # Finally dump the results on a file and return them
    Orchestrator.dump(results)
    return results

  # Factory method to return the proper rate
  @staticmethod
  def factory(rate):
    if rate == "pdr":
      return PDR
    elif rate == "mrr":
      return MRR
    else:
      print "Rate %s Not Supported Yet" % rate
      sys.exit(-1)

  # Dump the results on a file
  @staticmethod
  def dump(results):
    with open(RESULTS_FILE, 'w') as file:
     file.write(json.dumps(results))

if __name__ == '__main__':
  results = Orchestrator.run()
  print results