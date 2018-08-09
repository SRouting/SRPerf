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
    def __init__(self, server, txPort, rxPort, pcap, kpps, duration):
        self.server = server
        self.txPort = txPort
        self.rxPort = rxPort
        self.pcap = pcap
        self.rate = kpps;
        self.duration = duration
        
    # It transforms the rate expressed in kpps into the inter-packet gap
    # expressed in micro-seconds.
    def __fromKppsToIpgUsec(self, kpps):
        return 1000.0 / kpps;
    
    # It evaluates the number of times that a pcap file should be used to
    # generate a sufficient number of packets to fill the entire tx
    # window for completing the measurement test.
    def __packetLoopCounter(self, ipgUsec, duration):
        return long(math.ceil(2.0 * (1e6 / (ipgUsec))) * duration)
        
    def run(self):
        
        # We create a dictionary used to store results of the run.
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
            allPorts = [self.txPort, self.rxPort]
            ipgUsec = self.__fromKppsToIpgUsec(self.rate)
            loopCount = self.__packetLoopCounter(ipgUsec, self.duration)
            
            client.connect()
            
            # For safety reasons we reset any counter.
            client.reset(ports=allPorts)
            
            # We need to create a profile by reading the pcap and setting
            # the ipg_usec as well as the loop_count.
            profile = STLProfile.load_pcap(self.pcap, ipg_usec=ipgUsec,
                                           loop_count=loopCount)
            
            # We retrieve the streams
            # NOTE: we have as many streams as captured packets within 
            # the .pcap file.
            streams = profile.get_streams()
            
            # We use only one port to multiplex altogether streams.
            client.add_streams(streams, ports=[self.txPort])
            
            # Even if we create a new client it is better to reset also
            # ports and streams, because between client creation and
            # start of the experiment some packets may be received on ports.
            client.clear_stats()
            
            # NOTE: parameter 'mult' it does not seem to work properly when
            # pcap is used. Conversely, the ipg_usec is used to define
            # the packet rates.
            client.start(ports=[self.txPort], duration=self.duration)
            
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
            
            output['tx']['total_packets'] = client.get_xstats(self.txPort)['tx_total_packets']
            output['rx']['total_packets'] = client.get_xstats(self.rxPort)['rx_total_packets']
          
        except STLError as e:
            print(e)
            sys.exit(1)
        
        finally:
            client.disconnect()
        
        return output

    
# Entry point used for testing
if __name__ == '__main__':
    
    driver = TrexDriver('127.0.0.1', 0, 1, 'pcap/raw-pcap-files/plain-ipv6-64.pcap', 1100, 10)
    output = driver.run()
    print(output) 
    
