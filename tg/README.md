# TG Scripts

This folder contains all TG scripts for the Linux SRv6 performance experiment

### Generation of the config file ###

Config file can be manually generated using this convention. Config file can contain multiple lines, each one will be a different test to perform:

	type\texperiment\tsize\trate\n

For example:

	srv6	end	max	pdr
	srv6	end	max	mrr
	srv6	end	min	pdr
	srv6	end	min	mrr

Otherwise, it is possible to use the ***config_generator.py*** utility to automatically generate a configuration file:

	Usage: config_generator.py [options]

	Options:
  		-h, --help            show this help message and exit
  		-t TYPE, --type=TYPE  Test type {plain|transit|end|proxy|all}
