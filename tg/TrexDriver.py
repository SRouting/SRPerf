#!/usr/bin/python

import sys
import argparse
import json
import math
from warnings import catch_warnings
from time import sleep

# get TRex APIs.
sys.path.insert(0, "/opt/trex-core-2.41/scripts/automation/trex_control_plane/stl/")
from trex_stl_lib.api import *


class TrexDriver():
    
    # Builds an instance of TrexDriver
    def __init__(self, server, txPort, rxPort, pcap, rate, duration):
        self.server = server
        self.txPort = txPort
        self.rxPort = rxPort
        self.pcap = pcap
        self.rate = rate;
        self.duration = duration
    
    # It creates a stream by leveraging the 'pcap' file which has been set 
    # during the driver creation.
    def __buildStreamsFromPcap(self):
            return [STLStream(packet=STLPktBuilder(pkt=self.pcap),
                              mode=STLTXCont())]
        
    # We create and return a dictionary used to store results of the run.
    # The dictionary is composed by:
    # 
    # dictionary 
    #     |
    #     +--tx
    #     |   +--port
    #     |   +--total_packets
    #     |
    #     +--rx
    #     |   +--port
    #     |   +--total_packets
    #     |
    #     +--warnings
    #
    def run(self):
        output = {}
        output['tx'] = {}
        output['rx'] = {}
        output['tx']['port'] = self.txPort
        output['tx']['total_packets'] = 0
        output['rx']['port'] = self.rxPort
        output['rx']['total_packets'] = 0
        output['warnings'] = None
        
        # We create the client
        client = STLClient(server=self.server)
        
        try:
            profile = None
            stream = None
            txStats = None
            rxStats = None
            allPorts = [self.txPort, self.rxPort]
            
            client.connect()
            
            # For safety reasons we reset any counter.
            client.reset(ports=allPorts)
            
            # We retrieve the streams
            # NOTE: we have as many streams as captured packets within 
            # the .pcap file.
            streams = self.__buildStreamsFromPcap()
            
            # We use only one port to multiplex altogether streams.
            client.add_streams(streams, ports=[self.txPort])
            
            # Even if we create a new client it is better to reset also
            # ports and streams, because between client creation and
            # start of the experiment some packets may be received on ports.
            client.clear_stats()
            
            client.start(ports=[self.txPort], mult=self.rate,
                         duration=self.duration)
            
            # Now we block until all packets have been send/received. To
            # for be sure operations had been completed we wait for both
            # txPort and rxPort.
            client.wait_on_traffic(ports=allPorts)
            
            # We store warnings inside the dictionary in order to allow them
            # to be accessed afterwards
            if client.get_warnings():
                output['warnings'] = client.get_warnings()
            
            # We wait for a bit in order to let the counters be stable
            sleep(1)
            
            # We retrieve statistics from Tx and Rx ports.
            txStats = client.get_xstats(self.txPort)
            rxStats = client.get_xstats(self.rxPort)
            
            output['tx']['total_packets'] = txStats['tx_total_packets']
            output['rx']['total_packets'] = rxStats['rx_total_packets']
          
        except STLError as e:
            print(e)
            sys.exit(1)
        
        finally:
            client.disconnect()
        
        return output

    
# Entry point used for testing
if __name__ == '__main__':
    
    driver = TrexDriver('127.0.0.1', 0, 1, 'pcap/raw-pcap-files/plain-ipv6-64.pcap', '5kpps', 10)
    output = driver.run()
    print(output) 
    
