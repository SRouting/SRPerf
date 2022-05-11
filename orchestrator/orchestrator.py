#!/usr/bin/python

import sys
import json
import yaml
import os

from optparse import OptionParser

# We need to add tg modules
sys.path.insert(0, "../tg")

from config_parser import ConfigParser
from pdr import PDR
from mrr import MRR
from ssh_node import SshNode

# Constants

# Sut configurator
SUT_CONFIGURATOR = "forwarding-behaviour.cfg"
# Config file
CONFIG_FILE = "config.yaml"
# Testbed file
TESTBED_FILE = "testbed.yaml"
# key used in the testbed file
SUT_KEY = "sut"
SUT_HOME_KEY = "sut_home"
SUT_USER_KEY = "sut_user"
SUT_NAME_KEY = "sut_name"
FWD_ENGINE_KEY = "fwd"
# Results files
RESULTS_FILES = {
    'linux' :   'Linux.txt',
    'vpp'   :   'VPP.txt'
}

# Global variables

# Sut node
SUT = ""
# Sut home
SUT_HOME = ""
# Sut user
SUT_USER = ""
# Sut name
SUT_NAME = ""
# FWD ending
FWD_ENGINE = ""

# If the testbed file does not exist - we do not continue
if os.path.exists(TESTBED_FILE) == False:
  print("Error Testbed File %s Not Found" % TESTBED_FILE)
  sys.exit(-2)

# Parse function, load global variables from testbed file
with open(TESTBED_FILE) as f:
  configs = yaml.load(f)
SUT = configs[SUT_KEY]
SUT_HOME = configs[SUT_HOME_KEY]
SUT_USER = configs[SUT_USER_KEY]
SUT_NAME = configs[SUT_NAME_KEY]
FWD_ENGINE = configs[FWD_ENGINE_KEY]

# Check proper setup of the global variables
if SUT == "" or SUT_HOME == "" or SUT_USER == "" or SUT_NAME == "" or FWD_ENGINE == "":
  print("Check proper setup of the global variables")
  sys.exit(0)

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
    cfg_manager.run_command("cd %s/%s" %(SUT_HOME, FWD_ENGINE))
    # Let's parse the test plan
    parser = ConfigParser(CONFIG_FILE)
    # Run the experiments according to the test plan:
    for config in parser.get_configs():
      # Get the rate class
      rate_to_evaluate = Orchestrator.factory(config.rate)
      # Enforce the configuration
      experiment_name = config.name if config.name is not None else config.experiment
      cfg_manager.run_command("sudo bash %s %s" %(SUT_CONFIGURATOR, experiment_name))
      # Run the experiments
      values, outputs = rate_to_evaluate.run(config)
      # Collect the results
      results['%s-%s' %(experiment_name, config.rate)] = values
      results['%s-%s' %(experiment_name, config.rate)]['details'] = outputs
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
      print("Rate %s Not Supported Yet" % rate)
      sys.exit(-1)

  # Dump the results on a file
  @staticmethod
  def dump(results):
    with open(RESULTS_FILES[FWD_ENGINE], 'w') as file:
     file.write(json.dumps(results))

if __name__ == '__main__':
  results = Orchestrator.run()
  print(results)
