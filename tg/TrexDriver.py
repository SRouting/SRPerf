#!/usr/bin/python

import sys
import argparse
import json
import math
from warnings import catch_warnings
from time import sleep

import sys
sys.path.append('/proj/superfluidity-PG0/carmine/srv6pm-delay-measurement/srv6_delay_measurement/commons/protos/srv6pm/gen_py')
import grpc
import stamp_sender_pb2
import stamp_sender_pb2_grpc

# get TRex APIs.
sys.path.insert(0, "/opt/trex-core-2.92/scripts/automation/trex_control_plane/interactive/")

from trex.stl.api import *

class TrexOutput():
    
    def __init__(self):
        # We use a dictionary to represent (internally) the TrexOutput 'class'. 
        self.output = {}
        
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
        self.output['tx'] = {}
        self.output['rx'] = {}
        self.output['tx']['port'] = -1
        self.output['tx']['total_packets'] = -1
        self.output['tx']['duration'] = -1
        self.output['tx']['requested_tx_rate'] = -1
        
        self.output['rx']['port'] = -1
        self.output['rx']['total_packets'] = -1

        self.output['warnings'] = None
        
    def setTxPort(self, txPort):
        self.output['tx']['port'] = txPort
    
    def setRxPort(self, rxPort):
        self.output['rx']['port'] = rxPort

    def setTxTotalPackets(self, tPackets):
        self.output['tx']['total_packets'] = tPackets
        
    def setRxTotalPackets(self, tPackets):
        self.output['rx']['total_packets'] = tPackets
        
    def setTxDuration(self, duration):
        self.output['tx']['duration'] = duration
        
    def setRequestedTxRate(self, rate):   
        self.output['tx']['requested_tx_rate'] = rate
        
    def setWarnings(self, warn):
        self.output['warnings'] = warn
        
    def getTxPort(self):
        return self.output['tx']['port']
    
    def getRxPort(self, rxPort):
        return self.output['rx']['port']

    def getTxTotalPackets(self):
        return self.output['tx']['total_packets']
        
    def getRxTotalPackets(self):
        return self.output['rx']['total_packets']
    
    def getTxDuration(self):
        return self.output['tx']['duration']
    
    def getRequestedTxRate(self):
        return self.output['tx']['requested_tx_rate'] 
    
    def getWarnings(self):
        return self.output['warnings']
    
    def toDictionary(self):
        return self.output
    
    def toString(self):
        return str(self.output)

class TrexDriver():
    
    # Builds an instance of TrexDriver
    def __init__(self, server, txPort, rxPort, pcap, rate, duration):
        self.server = server
        self.txPort = txPort
        self.rxPort = rxPort
        self.pcap = pcap
        self.rate = rate
        self.duration = duration
    
    # It creates a stream by leveraging the 'pcap' file which has been set 
    # during the driver creation.
    def __buildStreamsFromPcap(self, mult=None):
        mult = float(mult)
        if mult is None:
            mult = 1.0
        if isinstance(self.pcap, list):
            streams = []
            for idx, pcap_info in enumerate(self.pcap):
                streams.append(
                    STLStream(
                        packet=STLPktBuilder(pkt=pcap_info['pcap']),
                        mode=STLTXCont(pps=pcap_info['percentage']/100)
                    )
                )
            return streams
        else:
            return [STLStream(packet=STLPktBuilder(pkt=self.pcap),
                              mode=STLTXCont())]
    
    def run(self):
        tOutput = TrexOutput()
        tOutput.setTxPort(self.txPort)
        tOutput.setRxPort(self.rxPort)
        tOutput.setRequestedTxRate(self.rate)
        tOutput.setTxDuration(self.duration)
        
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
            streams = self.__buildStreamsFromPcap(mult=self.rate)
            
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
            warn = client.get_warnings()
            if warn:
                tOutput.setWarnings(warn)
            
            # We wait for a bit in order to let the counters be stable
            sleep(1)

            try:
                channel = grpc.insecure_channel('c220g1-030805.wisc.cloudlab.us:12345')
                stub = stamp_sender_pb2_grpc.STAMPSessionSenderServiceStub(channel)
                stamp_results = stub.GetResultsCounter(stamp_sender_pb2.StampResultsCountersRequest(ssid=0))
                num_pkts_counter = stamp_results.num_results
            except grpc.RpcError as err:
                if err.code() == grpc.StatusCode.UNAVAILABLE:
                    num_pkts_counter = 0
                else:
                    raise err
            
            # We retrieve statistics from Tx and Rx ports.
            txStats = client.get_xstats(self.txPort)
            rxStats = client.get_xstats(self.rxPort)
            
            tOutput.setTxTotalPackets(txStats['tx_total_packets'])
            tOutput.setRxTotalPackets(rxStats['rx_total_packets'] + num_pkts_counter)

        except STLError as e:
            print(e)
            sys.exit(1)
        
        finally:
            client.disconnect()
        
        return tOutput

    
# Entry point used for testing
if __name__ == '__main__':

    driver = TrexDriver('127.0.0.1', 0, 1, 'pcap/trex-pcap-files/plain-ipv6-64.pcap', '100%', 10)
    output = driver.run()
    print(output.toString())
