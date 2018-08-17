#!/usr/bin/python

import numpy as np

from TrexDriver import *

class TrexPerfOutput():
    
    def __init__(self, runs, mean, std):
        self.output = {}
        
        self.output['dl_mean'] = mean
        self.output['dl_std'] = std
        
        self.runs = runs
        
    def getTrexOutput(self):
        return self.runs
    
    def getAverageDL(self):
        return self.output['dl_mean']
    
    def getStdDL(self):
        return self.output['dl_std']
    
    def toDictionary(self):
        # We create a copy of the current dictionary in order to add the 'runs'
        # field without altering the original structure.
        s = self.output.copy()
        s['runs'] = []
        
        for run in self.runs:
            dict = run.toDictionary()
            s['runs'].append(dict.copy())
            
        return s
    
    def toString(self):
        s = self.toDictionary()
        return str(s)
        
        
        #return '{{0}, {1}}'.format(self.runs.toString(), str(self.output))

class TrexPerfDriver():
    
    # Caller must assure consistency of parameters before creating a new
    # instance of this class.
    def __init__(self, server, txPort, rxPort, pcap, rate, repetitions,
                 duration):
        self.server = server
        self.txPort = txPort
        self.rxPort = rxPort
        self.pcap = pcap
        self.rate = rate
        self.repetitions = repetitions
        self.duration = duration
        
    def doPerformanceTest(self):
        results = []
        
        # We initialize the TrexDriver used to drive multiple tests with the 
        # same traffic rate.
        driver = TrexDriver(self.server, self.txPort, self.rxPort, self.pcap,
                            self.rate, self.duration)
        
        # Here we consider an additional run, the warm-up one. It is used to
        # warm up caches for reaching better and more stable results.
        for i in range(1 + self.repetitions):
            output = driver.run()
            if output is None:
                print('Driver returns an invalid result. Please check your SUT configuration.')
                sys.exit(1)
            
            if i > 0:
                # We skip the warm-up run which is the first one (0).
                results.append(output)
            else:
                print('Warm-up run skipped, it will not be considered in results.')
    
        # We return the results array in which we have stored the result of each
        # single test run.
        return results
    
    def doPostProcessing(self, results):
        # We create 'TrexPerfOutput' object which contains a reference to 
        # performed runs and aggregate measurements such as mean of DL and also
        # the std. 
        output = None
        
        # We create a numpy array in order to store checked and validate data
        dlRuns = np.array([])
        
        # We process each single result
        for i in range(len(results)):
            run = results[i]
            warn = run.getWarnings()
            
            if warn is not None:
                # There is a warning, so it is better to print out on screen 
                # instead of suppress it.
                print('Run ({0}) - Warning {1}'.format(i, warn))
            else:
                txTotalPackets = run.getTxTotalPackets()
                rxTotalPackets = run.getRxTotalPackets()
                                
                # Let's check if rxTotalPacket is greater than txTotalPacket. 
                # If this is the case (due to lldp packets) we normalize the
                # number of received packets with the 'txTotalPackets' counter.
                # Anyway, if the rxTotalPackets is > rxTotalPacketsTolerance then
                # some issues occurred... and we need to skip the run in order 
                # to let the results valid.
                rxTotalPacketsTolerance = txTotalPackets + (1.0 / 1000.0) * txTotalPackets
                if rxTotalPackets > rxTotalPacketsTolerance:
                    print('Run ({0}) - Warning rxTotalPackets ({1} > {2}) exceeded the threshold. Run will be skipped.'.
                        format(i, float(rxTotalPackets),
                        float(rxTotalPacketsTolerance)))
                    
                    continue
                
                # We already checked that rxTotalPacket <= txTotalPackets + 1%
                if rxTotalPackets > txTotalPackets:
                    rxTotalPackets = txTotalPackets
                
                # We evaluate DL
                dl = rxTotalPackets / (1.0 * txTotalPackets)
                dlRuns = np.append(dlRuns, dl)    
        
        # End of for
    
        # We check if the array which contains the results is empty or not. 
        # In case of empty array something is went wrong and we must terminate
        # the measurements.
        if 0 == dlRuns.size:
            print('Warning - invalid statistics: collected data is not valid.')
            return trexPerfOutput
    
        # We evaluate mean and std of delivery ratios
        dlMean = np.mean(dlRuns)
        dlStd = np.std(dlRuns, ddof=1)
        
        # We build the object wrapper
        output = TrexPerfOutput(results, dlMean, dlStd)
        
        return output
        
    # Run is reentrant and it can be called multiple times without creating
    # a new TrexPerfDriver instance.
    def run(self):
        runs = []
        output = None
        
        # We perform tests and retrieve back the results
        runs = self.doPerformanceTest()
        
        # We apply some post processing operations such as the evaluation of
        # delivery ration mean value and also the std evaluation.
        output = self.doPostProcessing(runs)

        return output
    
# Entry point used for testing
if __name__ == '__main__':
    perfDriver = TrexPerfDriver('127.0.0.1', 0,
                                1, 'pcap/raw-pcap-files/plain-ipv6-64.pcap',
                                '1000000', 5, 10)
    print ('Running ...')
    
    trexPerfOutput = perfDriver.run()
    rrate = trexPerfOutput.getTrexOutput()[0]
    
    print('RRate {0}, Mean {1}, Std. {2}'.format(rrate.getRequestedTxRate(), 
                                                 trexPerfOutput.getAverageDL(), 
                                                 trexPerfOutput.getStdDL()))
    
    print ('Completed ...')
            
