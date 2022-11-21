#!/usr/bin/python

import sys

# We need to add tg modules
sys.path.insert(0, "../tg")

from NoDropRateSolver import *
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
#STARTING_TX_RATE = 100.0
# NDR window
NDR_WINDOW = 50.0
# Lower bound for delivery ratio
LB_DLR = 0.995

# Realizes a PDR experiment
class PDR(object):

  @staticmethod
  def get_packet(config):
    ret = []
    streams = ConfigParser.get_streams(config)
    if streams is not None:
      for stream in streams:
        packet = "%s-%s-%s" % (stream["type"], stream["experiment"],
                               ConfigParser.MAPPINGS[stream["size"]])
        ret.append({
          "pcap": "%s/%s.pcap" % (PCAP_HOME, packet),
          "percentage": stream["percentage"]
        })
      return ret
    else:
      return "%s/%s.pcap" %(PCAP_HOME, ConfigParser.get_packet(config))

  # Run a PDR experiment using the config provided as input
  @staticmethod
  def run(config):
    results = []
    outputs = []
    # We collect run PDR values and we return them
    for iteration in range(0, config.run):
      print("PDR %s-%s Run %s" %(config.type, config.experiment, iteration))
      # At first we create the experiment factory with the right parameters
      factory = TrexExperimentFactory(TREX_SERVER, TX_PORT, RX_PORT,
                                      PDR.get_packet(config), SAMPLES, DURATION)
      # Then we instantiate the NDR solver with the above defined parameters
      ndr = NoDropRateSolver(STARTING_TX_RATE, config.line_rate, NDR_WINDOW, LB_DLR, 
                             RateType.PPS, factory)
      ndr.solve()
      # Once finished let's collect the results
      results.append(ndr.getSW()[0])
      outputs.append(ndr.getRawOutput())
    return results, outputs
