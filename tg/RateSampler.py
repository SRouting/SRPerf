

class DeliveryRatioSampler:
    
    DATA_SEPARATOR = " "
    
    @staticmethod
    def buildResultFormat(nl=""):
        res_format_line = "{{0:f}}{sep}{{1:f}}{sep}{{2:f}}{end}".format(
            sep=DeliveryRatioSampler.DATA_SEPARATOR, end=nl)
        return res_format_line

    def __init__(self, rates, experimentFactory):
        self.rates = rates
        self.experimentFactory = experimentFactory
        
        self.results = []        
    
    def sample(self):
        print("Sampling...")
        
        # For every rate value we create a new test and we perform it in order
        # to evaluate the rx rate and also the DR.
        for curRate in self.rates:
            
            # Experiment accepts any kind of rate, anyway it is always a
            # string 'str' type.
            experiment = self.experimentFactory.build(str(curRate))
            output = experiment.run()
            
            # It evaluates the rxRate using the DR
            curDelRatio = output.getAverageDR()
            rxRate = curDelRatio * curRate
            
            tuple = (curRate, rxRate, curDelRatio)
            self.results.append(tuple)
            
            print(DeliveryRatioSampler.buildResultFormat().format(
                curRate, rxRate, curDelRatio))
        
        print("Sampling process completed...")
    
    def printResults(self):
        for tuple in self.results:
             print(DeliveryRatioSampler.buildResultFormat().format(
                tuple[0], tuple[1], tuple[2]))
            
    def saveResults(self, filename):
        try:
            writer = open(filename, "w")
            
            for tuple in self.results:
                writer.write(DeliveryRatioSampler.buildResultFormat("\n").
                             format(tuple[0], tuple[1], tuple[2]))
            
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        else:
            writer.close()
        
