
import math

class NoDropRateSolver:
    
#    DATA_SEPARATOR = ";"
    
#     @staticmethod
#     def buildResultFormat(nl=""):
#         res_format_line = "{{0:f}}{sep}{{1:f}}{end}".format(
#             sep=NoDropRateSolver.DATA_SEPARATOR, end=nl)
#         return res_format_line
    
    def __init__(self, startingTxRate, epsilon, dlTreshold, experimentFactory):
        self.delRatioLowerBound = 0
        self.rateLowerBound = startingTxRate
        self.delRatioUpperBound = 0
        self.rateUpperBound = self.rateLowerBound
        
        self.eps = epsilon
        self.dlTreshold = dlTreshold
        self.experimentFactory = experimentFactory
        
        self.incFactor = 2
        # Step is evaluated on the basis of eps divided by a default scale factor
        # which is in this case 10
        self.step = self.eps / 10.0
            
        #self.linearResults = []
        self.results = []
        
    def buildAndRunExperiment(self, txRate):
        experiment = self.experimentFactory.build(str(txRate))
        output = experiment.run()
        
        return output
        # return -0.02 * rate + 1;
    
    def expSearch(self):
        stop = False    
        curRate = self.rateLowerBound
        curDelRatio = 1.0
        
        while(not stop):
            curRate = curRate * self.incFactor
            
            # We run the experiment using the given curRate value.
            output = self.buildAndRunExperiment(curRate)
            curDelRatio = output.getAverageDL()
            
            if (curDelRatio < self.dlTreshold):
                self.rateUpperBound = curRate
                self.delRatioUpperBound = curDelRatio
                stop = True
            else:
                self.rateLowerBound = curRate
                self.delRatioLowerBound = curDelRatio
            
            # We create a tuple that collects relevant data for this iteration
            tuple = (self.rateLowerBound, self.delRatioLowerBound, 
                     self.rateUpperBound, self.delRatioUpperBound,
                     curRate, curDelRatio, self.dlTreshold)
            self.results.append(tuple)
            
            print("Exp search <probed:{0:f}/DR:{1:f}>, Thres:{2:f}".format(
                tuple[4], tuple[5], tuple[6]))
    
    def logSearch(self):
        stop = False
        solutionInterval = 0.0
        curRate = 0.0
        curDelRatio = 0.0
        
        while(not stop):
            solutionInterval = math.fabs(self.rateUpperBound - self.rateLowerBound)
            if (solutionInterval <= self.eps):
                stop = True
            else:
                curRate = (self.rateUpperBound + self.rateLowerBound) / 2.0
                output = self.buildAndRunExperiment(curRate)
                curDelRatio = output.getAverageDL()
                
                if (curDelRatio < self.dlTreshold):
                    self.rateUpperBound = curRate
                    self.delRatioUpperBound = curDelRatio
                else:
                    self.rateLowerBound = curRate
                    self.delRatioLowerBound = curDelRatio
                
                # We create a tuple that collects relevant data for this iteration
                tuple = (self.rateLowerBound, self.delRatioLowerBound, 
                         self.rateUpperBound, self.delRatioUpperBound,
                         curRate, curDelRatio, self.dlTreshold)
                self.results.append(tuple)
                
                print("Log search [{0:f}/{1:f},{2:f}/{3:f}], <probed:{4:f}/DR:{5:f}>, Thres:{6:f}".
                      format(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], 
                             tuple[5], tuple[6]))

    def solve(self):
        print("Solver started...")
        print("Exponential search")
        self.expSearch()
        
        print("Logarithmic search")
        self.logSearch()
        
        #print("\nLinear search")
        #self.linearSearch()
        
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



#     def linearSearch(self):
#         rateUpperBound = self.rateUpperBound + (self.eps / 2.0)
#         rateLowerBound = self.rateLowerBound - (self.eps / 2.0)
#         curRate = rateLowerBound
#         curDelRatio = 0.0
#         
#         while(curRate < rateUpperBound):
#             output = self.buildAndRunExperiment(curRate)
#             curDelRatio = output.getAverageDL()
#             
#             self.linearResults.append((curRate, curDelRatio))
#             
#             print("Linear search [{0:f},{1:f}], <rate:{2:f}, DR:{3:f}>, Thres:{4:f}".
#                    format(rateLowerBound, rateUpperBound, curRate,
#                    curDelRatio, self.dlTreshold))
#             
#             curRate += self.step
#        
#     def printResults(self):
#         for x in self.linearResults:
#             print(NoLossRegionSolver.buildResultFormat().format(x[0], x[1]))
#             
#     def saveResults(self, filename):
#         try:
#             writer = open(filename, "w")
#             
#             for x in self.linearResults:
#                 writer.write(NoLossRegionSolver.buildResultFormat("\n").
#                              format(x[0], x[1]))
#             
#         except IOError as e:
#             print "I/O error({0}): {1}".format(e.errno, e.strerror)
#         else:
#             writer.close()
    
