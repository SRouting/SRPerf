#!/usr/bin/python

import sys

# We need to add tg modules
sys.path.insert(0, "../tg")

from NoDropRateSolver import NoDropRateSolver
from TrexPerf import TrexExperimentFactory
from config_parser import ConfigParser

# Trex server
TREX_SERVER = "127.0.0.1"
# TX port
TX_PORT = 0
# RX port
RX_PORT = 1
# Duration of a single RUN (time to get a sample)
DURATION = 10
# pcap location
PCAP_HOME = "../pcap/trex-pcap-files"
# Define the namber of samples for a given PDR
SAMPLES = 1
# Starting tx rate
STARTING_TX_RATE = 100000.0
# NDR window
NDR_WINDOW = 500.0
# Lower bound for delivery ratio
LB_DLR = 0.995

# Realizes a PDR experiment
class PDR(object):

  # Run a PDR experiment using the config provided as input
  @staticmethod
  def run(config):
    results = []
    print "Running PDR"
    # We collect run PDR values and we return them
    for iteration in range(0, config.run):
      print "Run", iteration
      # At first we create the experiment factory with the right parameters
      factory = TrexExperimentFactory(TREX_SERVER, TX_PORT, RX_PORT, "%s/%s.pcap" %(PCAP_HOME, ConfigParser.get_packet(config)),
                                      SAMPLES, DURATION)
      # Then we instantiate the NDR solver with the above defined parameters
      ndr = NoDropRateSolver(STARTING_TX_RATE, NDR_WINDOW, LB_DLR, factory)
      ndr.solve()
      # Once finished let's collect the results
      results.append(ndr.getSW()[0])
    return results
