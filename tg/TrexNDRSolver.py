
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
                                    'pcap/trex-pcap-files/plain-ipv6-64.pcap', 
                                    1, 5)
        # NoDropDelivey ratio
        # Parameters are:
        #
        # 100000.0 starting tx rate
        # 500.0 (in pps) width of NDR searching window (used in the log search and linear phase)
        # 0.995 is the NDR
        ndr = NoDropRateSolver(100000.0, 500.0, 0.995, 12253800, factory)
        ndr.solve()
        
        # If no SW has been found, it returns None; otherwise it returns a tuple,
        # whose values are:
        #    position 0: SW's lower bound
        #    position 1: SW's delivery ratio for lower bound
        #    position 2: SW's upper bound
        #    position 3: SW's delivery ratio for upper bound
        #    position 4,5,6: ancillary data. For further information please look at
        #                    function expSearch() and logSearch().
        sw = ndr.getSW()
        
        print '---------- Result ------------'
        print sw
        print '---------- Result ------------'