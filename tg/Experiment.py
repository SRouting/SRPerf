
from abc import ABCMeta, abstractmethod
import six


# An Experiment must extends this class.
class Experiment(six.with_metaclass(ABCMeta)):
    
    # Implementing this function allows to define how an experiment
    # has to be invoked.
    @abstractmethod
    def run(self, *args):
        pass

# Factory for Experiment.
# Every Experiment should define its own factory method (and class).
class ExperimentFactory(six.with_metaclass(ABCMeta)):
    
    @abstractmethod
    def build(self, *args):
        pass
    
class ExperimentOutput(six.with_metaclass(ABCMeta)):
    
    @abstractmethod
    def getRequestedTxRate(self):
        pass
    
    @abstractmethod
    def getAverageDR(self):
        pass
    
    @abstractmethod
    def getStdDL(self):
        pass
    
    @abstractmethod
    def toString(self):
        pass
    
class ExperimentException(Exception):
    
    def __init__(self, message):
        super(Exception, self).__init__(message)