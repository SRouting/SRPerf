#!/usr/local/bin/python2.7

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import sys, traceback, re, numpy

from TrexDriver import *
from TrexPerf import *
from RateSampler import *


def parseInterval(arg):
    output = {}
    output['parsed'] = False
    output['interval'] = False

    # Token T   := <VALUE> | <VALUE>:INTERVAL
    # INTERVAL  := VALUE:VALUE
    # VALUE     := [0-9\.]+
    #
    # NOTE: We don't mind (for now) if the number is correct, i.e: 
    # xx.xx is legal, and also xx.xx.xx.
    p = re.compile(
        '^(?P<start>[0-9\.]+)(?:[\:](?P<step>[0-9\.]+)[\:](?P<stop>[0-9\.]+)){0,1}$'
    )
    m = p.match(arg)

    if (m is None):
        print "Invalid argument: {}".format(arg)
        return output

    start = m.group('start')
    parsedStart = float(start)
    output['start'] = parsedStart

    # Optional
    step = m.group('step')
    stop = m.group('stop')

    if (step is not None and stop is not None):
        parsedStep = float(step)
        parsedStop = float(stop)

        output['interval'] = True
        output['step'] = parsedStep
        output['stop'] = parsedStop

    output['parsed'] = True

    return output


def buildRateInterval(arg):
    parsedOutput = parseInterval(arg)
    if (parsedOutput is None):
        return []
    if (not parsedOutput['parsed']):
        return []

    start = parsedOutput['start']

    if (parsedOutput['interval']):
        step = parsedOutput['step']
        stop = parsedOutput['stop']
        return numpy.arange(start, stop, step)

    # It needs to be closed, so we always return an array with one or more element.
    return [start]


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    try:
        parser = ArgumentParser(description="", formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("--server", dest="server", default='127.0.0.1', type=str)
        parser.add_argument("--txPort", dest="txPort", required=True)
        parser.add_argument("--rxPort", dest="rxPort", required=True)
        parser.add_argument("--pcap", dest="pcap", required=True)
        parser.add_argument("--rates", dest="rates", required=True)
        parser.add_argument("--repetitions", dest="repetitions", default=1, type=int)
        parser.add_argument("--duration", dest="duration", required=True)
        parser.add_argument("--fout", dest="fileOutput")

        # Process arguments
        args = parser.parse_args()
                
        server = str(args.server)
        txPort = int(args.txPort)
        rxPort = int(args.rxPort)
        pcap = str(args.pcap)
        rates = args.rates
        duration = int(args.duration)
        repetitions = int(args.repetitions)
        fileOutput = args.fileOutput

        # Parsing the rates array
        parsedRates = []
        for i in rates.split(): 
            interval = buildRateInterval(i)
            if (len(interval) == 0):
                # Parsing error
                raise ValueError('invalid argument: {}'.format(i))

            for j in interval:
                parsedRates.append(j)

        factory = TrexExperimentFactory(server, txPort, rxPort, pcap,
                                        repetitions, duration)
        drs = DeliveryRatioSampler(parsedRates, factory)

        print("configuration: --server {0:s} --txPort {1:d} --rxPort {2:d} --pcap {3:s} --rates {4:s} --repetitions {5:d} --duration {6:d}".
               format(server, txPort, rxPort, pcap, numpy.around(parsedRates, 3),
                      repetitions, duration))

        drs.sample()

        print('---- Results ----')
        drs.printResults()
        print('-----------------')

        if fileOutput is not None:
            drs.saveResults(str(fileOutput))

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception:
        print '-' * 60
        print "Exception in user code:"
        traceback.print_exc(file=sys.stdout)
        print '-' * 60

        return 2


if __name__ == "__main__":
    sys.exit(main())
