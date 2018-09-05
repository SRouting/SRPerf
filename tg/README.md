# TG Scripts

This folder contains all TG scripts for the Linux SRv6 performance experiment

### Generation of the config file ###

Config file can be manually generated using yaml convention. Config file can contain multiple yaml sequences, each one will be a different test to perform:

    - experiment: ipv6
      rate: pdr
      run: 10
      size: max
      type: plain

For example:

    - experiment: ipv6
      rate: pdr
      run: 10
      size: max
      type: plain
    - experiment: ipv6
      rate: mrr
      run: 1
      size: max
      type: plain
    - experiment: ipv6
      rate: pdr
      run: 10
      size: min
      type: plain
    - experiment: ipv6
      rate: mrr
      run: 1
      size: min
      type: plain
    - experiment: ipv4
      rate: pdr
      run: 10
      size: max
      type: plain
    - experiment: ipv4
      rate: mrr
      run: 1
      size: max
      type: plain
    - experiment: ipv4
      rate: pdr
      run: 10
      size: min
      type: plain
    - experiment: ipv4
      rate: mrr
      run: 1
      size: min
      type: plain


Otherwise, it is possible to use the ***config_generator.py*** utility to automatically generate a configuration file:

	Usage: config_generator.py [options]

	Options:
  		-h, --help            show this help message and exit
  		-t TYPE, --type=TYPE  Test type {plain|transit|end|proxy|all}
