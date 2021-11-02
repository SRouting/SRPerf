#!/usr/local/bin/python2.7
# encoding: utf-8

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import sys, traceback, re, numpy

from TrexDriver import *

def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    try:
        # Setup argument parser
        parser = ArgumentParser(description="", formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("--server", dest="server")
        parser.add_argument("--txPort", dest="txPort", required=True)
        parser.add_argument("--rxPort", dest="rxPort", required=True)
        parser.add_argument("--pcap", dest="pcap", required=True)
        parser.add_argument("--rate", dest="rate", required=True)
        parser.add_argument("--duration", dest="duration", required=True)

        # Process arguments
        args = parser.parse_args()

        server = args.server
        if server is None:
            server = '127.0.0.1'
                
        server = str(server)
        txPort = int(args.txPort)
        rxPort = int(args.rxPort)
        pcap = str(args.pcap)
        rate = str(args.rate)
        duration = int(args.duration) 
        
        driver = TrexDriver(server, txPort, rxPort, pcap, rate, duration)
        output = driver.run()
        
        # Print out results
        print(output.toString())
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception:
        print('-' * 60)
        print("Exception in user code:")
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)
        return 2

if __name__ == "__main__":
    sys.exit(main())
