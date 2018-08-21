
import math


class NoDropRateSolver:
    
    DATA_SEPARATOR = ";"
    
    @staticmethod
    def buildResultFormat(nl=""):
        res_format_line = "{{0:f}}{sep}{{1:f}}{end}".format(
            sep=NoDropRateSolver.DATA_SEPARATOR, end=nl)
        return res_format_line
    
    def __init__(self, startingTxRate, epsilon, dlTreshold, experimentFactory):
        self.rateLowerBound = startingTxRate
        self.rateUpperBound = self.rateLowerBound
        self.eps = epsilon
        self.dlTreshold = dlTreshold
        self.experimentFactory = experimentFactory
        
        self.incFactor = 2
        # Step is evaluated on the basis of eps divided by a default scale factor
        # which is in this case 10
        self.step = self.eps / 10.0
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
                stop = True
            else:
                self.rateLowerBound = curRate
            
            print("Exp search initial rate:{0:f}, <rate:{1:f}, DR:{2:f}>, Thres:{3:f}".
                   format(self.rateLowerBound, curRate, curDelRatio,
                   self.dlTreshold))
    
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
                else:
                    self.rateLowerBound = curRate
                    
                print("Log search [{0:f},{1:f}], <rate:{2:f}, DR:{3:f}>, Thres:{4:f}".
                      format(self.rateLowerBound, self.rateUpperBound, curRate,
                      curDelRatio, self.dlTreshold))
        pass
    
    def linearSearch(self):
        rateUpperBound = self.rateUpperBound + (self.eps / 2.0)
        rateLowerBound = self.rateLowerBound - (self.eps / 2.0)
        curRate = rateLowerBound
        curDelRatio = 0.0
        
        while(curRate < rateUpperBound):
            output = self.buildAndRunExperiment(curRate)
            curDelRatio = output.getAverageDL()
            
            self.results.append((curRate, curDelRatio))
            
            print("Linear search [{0:f},{1:f}], <rate:{2:f}, DR:{3:f}>, Thres:{4:f}".
                   format(rateLowerBound, rateUpperBound, curRate,
                   curDelRatio, self.dlTreshold))
            
            curRate += self.step

    def solve(self):
        print("Solver started...")
        print("Exponential search")
        self.expSearch()
        
        print("\nLogarithmic search")
        self.logSearch()
        
        #print("\nLinear search")
        #self.linearSearch()
        
        print("Solver completed...")
        
    def printResults(self):
        for x in self.results:
            print(NoLossRegionSolver.buildResultFormat().format(x[0], x[1]))
            
    def saveResults(self, filename):
        try:
            writer = open(filename, "w")
            
            for x in self.results:
                writer.write(NoLossRegionSolver.buildResultFormat("\n").
                             format(x[0], x[1]))
            
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        else:
            writer.close()
    
