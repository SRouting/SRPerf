
import math
import sys, traceback

from enum import Enum

# Supported rate types.
class RateType(Enum):
    INVALID = 0
    PPS = 1
    PERCENTAGE = 2

class NoDropRateSolver:
    
    def __init__(self, minTxRate, maxTxRate, epsilon, drThreshold, rateType,
                 experimentFactory):
        # We check the input parameters
        self.checkAndSet(minTxRate, maxTxRate, epsilon, drThreshold, rateType)
        if (experimentFactory is None):
            self.printAndDie('Experiment must be set.', 1)
        self.experimentFactory = experimentFactory
        
        self.delRatioLowerBound = 0
        self.delRatioUpperBound = 0
        self.incFactor = 2
        
        # Step is evaluated on the basis of eps divided by a default scale factor
        # which is in this case 10
        self.step = self.eps / 10.0
        self.results = []
    
    # It prints a message and exits returning the specified code.
    def printAndDie(self, message, exitCode):
        print '{0:s}'.format(message)
        sys.exit(exitCode)
        
    # We sanitize input parameters.
    def checkAndSet(self, minTxRate, maxTxRate, epsilon, drThreshold, rateType):
        if (0 >= drThreshold  or 1 < drThreshold):
            self.printAndDie("Threshold value is not valid.", 1)
        
        if (0 > minTxRate):
            self.printAndDie('Invalid searching window lower bound value.', 1)
        if (minTxRate > maxTxRate):
            self.printAndDie('Invalid searching window boundaries.', 1)
        
        if (0 > epsilon):
            self.printAndDie("Epsilon can not be less than zero.", 1)
        if (epsilon > (maxTxRate - minTxRate)):
            self.printAndDie("Epsilon is not valid.", 1)
        
        if (RateType.INVALID == rateType):
            self.printAndDie('Invalid rate type, allowed: { PERCENTAGE, PPS }.', 1)
        if (RateType.PERCENTAGE == rateType):
            if (maxTxRate > 100.0):
                self.printAndDie('Invalid searching window upper bound value.', 1)
        
        self.rateLowerBound = minTxRate
        self.rateUpperBound = maxTxRate
        self.rateType = rateType
        self.eps = epsilon 
        self.dlThreshold = drThreshold
        
    def buildAndRunExperiment(self, txRate):
        # On the basis of the txRate type (aka PPS or PERCENTAGE) we have to
        # append the '%' symbol at the txRate in case of PERCENTAGE or nothing
        # if the txRate is expressed in PPS.
        txRate = str(txRate)
        if (RateType.PERCENTAGE == self.rateType):
            txRate = '{0:s}%'.format(txRate)
        
        experiment = self.experimentFactory.build(txRate)
        output = experiment.run()
        
        return output
    
    def logSearch(self):
        stop = False
        solutionInterval = 0.0
        curRate = 0.0
        curDelRatio = 0.0
        
        # We have removed the Exponential Search, so we need to be sure that
        # lower bound delivery ratio is above the threshold. Indeed, if the
        # lower bound DR does not respect the threshold, it is completely useless
        # to continue.
        curRate = self.rateLowerBound
        output = self.buildAndRunExperiment(curRate)
        self.delRatioLowerBound = output.getAverageDR()
        
        if (self.delRatioLowerBound < self.dlThreshold):
            print 'Invalid lower bound for the current searching window: DR is below the threshold.'
            return 0
        
        # Let's find out the PDR value
        while(not stop):
            solutionInterval = math.fabs(self.rateUpperBound - self.rateLowerBound)
            if (solutionInterval <= self.eps):
                stop = True
            else:
                curRate = (self.rateUpperBound + self.rateLowerBound) / 2.0
                output = self.buildAndRunExperiment(curRate)
                curDelRatio = output.getAverageDR()
                
                if (curDelRatio < self.dlThreshold):
                    self.rateUpperBound = curRate
                    self.delRatioUpperBound = curDelRatio
                else:
                    self.rateLowerBound = curRate
                    self.delRatioLowerBound = curDelRatio
                
                # We create a tuple that collects relevant data for this iteration
                tuple = (self.rateLowerBound, self.delRatioLowerBound,
                         self.rateUpperBound, self.delRatioUpperBound,
                         curRate, curDelRatio, self.dlThreshold)
                self.results.append(tuple)
                
                print("Log search [{0:f}/{1:f},{2:f}/{3:f}], <probed:{4:f}/DR:{5:f}>, Thres:{6:f}".
                      format(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4],
                             tuple[5], tuple[6]))
    
    def solve(self):
        print("Solver started...")
        
        self.logSearch()
        
        print("Solver completed...\n")
    
    # Retrieves the smallest searching window obtained combining exponential and
    # logarithmic phases.
    # If no SW has been found, it returns None; otherwise it returns a tuple,
    # whose values are:
    #    position 0: SW's lower bound
    #    position 1: SW's delivery ratio for lower bound
    #    position 2: SW's upper bound
    #    position 3: SW's delivery ratio for upper bound
    #    position 4,5,6: ancillary data. For further information please look at
    #                    function expSearch() and logSearch().
    def getSW(self):
        if 0 == len(self.results):
            return None
        else:
            # We return the last element of the list. In this case the last
            # element is the smallest searching window evaluated during the
            # log search.
            return self.results[-1]
#        
