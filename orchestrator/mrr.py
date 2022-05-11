#!/usr/bin/python

import sys
import numpy as np

# We need to add tg modules
sys.path.insert(0, "../tg")

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
# Rate
RATE = "100%"

# Realizes a MRR experiment
class MRR(object):

  # Run a MRR experiment using the config provided as input
  @staticmethod
  def run(config):
    # We create an array in order to store mrr of each run
    results = []
    # We collect run MRR values and we return them
    for iteration in range(0, config.run):
      print("MRR %s-%s Run %s" %(config.type, config.experiment, iteration))
      # At first we create the experiment factory with the right parameters
      factory = TrexExperimentFactory(TREX_SERVER, TX_PORT, RX_PORT, "%s/%s.pcap" %(PCAP_HOME, ConfigParser.get_packet(config)),
                                      SAMPLES, DURATION)
      # Build the experiment passing a given rate
      experiment = factory.build(RATE)
      # Run and collect the output of the experiment
      run = experiment.run().runs[0]
      # Calculate mrr and then store in the array
      mrr = run.getRxTotalPackets() / DURATION
      results.append(mrr)
    return results, None
