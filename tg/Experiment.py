
from _pyio import __metaclass__
from abc import ABCMeta, abstractmethod
from exceptions import Exception


# An Experiment must extends this class.
class Experiment():
    __metaclass__ = ABCMeta
    
    # Implementing this function allows to define how an experiment
    # has to be invoked.
    @abstractmethod
    def run(self, *args):
        pass
    
class ExperimentException(Exception):
    
    def __init__(self, message):
        super(Exception, self).__init__(message)