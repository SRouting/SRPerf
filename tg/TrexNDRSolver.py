
from TrexDriver import *
from TrexPerf import *
from Experiment import *
from NoDropRateSolver import *

if __name__ == '__main__':
        
        # The factory used for creating the TrexExperiment with fixed parameters.
        # Parameters are:
        # 
        # 127.0.0.1 is the Trex server address
        # 0, 1 are tx and rx ports
        # 'pcap/raw-pcap-files/plain-ipv6-64.pcap' is the pcap
        # 5 is the number of runs (or trials) to perform in the experiment
        # 10 is how long a run should last (is expressed in seconds)
        factory = TrexExperimentFactory('127.0.0.1', 0, 1, 
                                    'pcap/raw-pcap-files/plain-ipv6-64.pcap', 
                                    2, 10)
        # NoDropDelivey ratio
        # Parameters are:
        #
        # 800000.0 starting tx rate
        # 1000.0 (in pps) width of NDR searching window (used in the log search and linear phase)
        # 0.995 is the NDR
        ndr = NoDropRateSolver(800000.0, 500.0, 0.995, factory)
        ndr.solve()