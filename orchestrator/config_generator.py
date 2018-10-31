#!/usr/bin/python

import yaml
import sys
from optparse import OptionParser

# Config file
CONFIG_FILE = "config.yaml"
# Number of runs
RUN = 10

def write_config(configs=[]):
  with open(CONFIG_FILE, 'w') as outfile:
    outfile.write(yaml.dump(configs, default_flow_style=False))

# Generate config for all tests
def generate_all(size):
  configs = []
  configs.extend(generate_plain(False, size))
  configs.extend(generate_transit(False, size))
  configs.extend(generate_end(False, size))
  configs.extend(generate_proxy(False, size))
  # Write the entire configuration
  write_config(configs)

def generate_size(size="all"):
  if size == "all":
    configs = [
      {'size': 'max'},
      {'size': 'min'}
    ]
  elif size == "min":
    configs = [
      {'size': 'min'}
    ]
  elif size == "max":
    configs = [
      {'size': 'max'}
    ]
  else:
    print "Size %s Not Supported Yet" % size
    sys.exit(-1)
  return configs

def generate_configs(experiments, size):
  configs = []
  # Generate the sizes
  sizes = generate_size(size)
  # Iterate over the experiments
  for experiment in experiments:
    # Iterate over the sizes
    for size in sizes:
      config = experiment.copy()
      config.update(size)
      configs.append(config)
  return configs

# Generate config for plain tests
def generate_plain(write=True, size="all"):
  # Define the experiments
  experiments = [
    {'type': 'plain', 'experiment': 'ipv6', 'rate': 'pdr', 'run': RUN},
    {'type': 'plain', 'experiment': 'ipv6', 'rate': 'mrr', 'run': RUN},
    {'type': 'plain', 'experiment': 'ipv4', 'rate': 'pdr', 'run': RUN},
    {'type': 'plain', 'experiment': 'ipv4', 'rate': 'mrr', 'run': RUN}
  ]
  # Generate configs
  configs = generate_configs(experiments, size)
  if not write:
    return configs
  # Write the PLAIN configuration
  write_config(configs)

# Generate config for transit tests
def generate_transit(write=True, size="all"):
  # Define the experiments
  experiments = [
    {'type': 'srv6', 'experiment': 't_encaps_v6', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 't_encaps_v6', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 't_encaps_v4', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 't_encaps_v4', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 't_encaps_l2', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 't_encaps_l2', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 't_insert_v6', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 't_insert_v6', 'rate': 'mrr', 'run': RUN}
  ]
  # Generate configs
  configs = generate_configs(experiments, size)
  if not write:
    return configs
  # Write the TRANSIT configuration
  write_config(configs)

# Generate config for end tests
def generate_end(write=True, size="all"):
  # Define the experiments
  experiments = [
    {'type': 'srv6', 'experiment': 'end', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_x', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_x', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_t', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_t', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_b6', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_b6', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_b6_encaps', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_b6_encaps', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_dx6', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_dx6', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_dx4', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_dx4', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_dx2', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_dx2', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_dt6', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_dt6', 'rate': 'mrr', 'run': RUN}
  ]
  # Generate configs
  configs = generate_configs(experiments, size)
  if not write:
    return configs
  # Write the END configuration
  write_config(configs)

# Generate config for proxy tests
def generate_proxy(write=True, size="all"):
  # Define the experiments
  experiments = [
    {'type': 'srv6', 'experiment': 'end_ad6', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_ad6', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_ad4', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_ad4', 'rate': 'mrr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_am', 'rate': 'pdr', 'run': RUN},
    {'type': 'srv6', 'experiment': 'end_am', 'rate': 'mrr', 'run': RUN}
  ]
  # Generate configs
  configs = generate_configs(experiments, size)
  if not write:
    return configs
  # Write the PROXY configuration
  write_config(configs)

# Parse options
def generate():
  # Init cmd line parse
  parser = OptionParser()
  parser.add_option("-t", "--type", dest="type", type="string",
    default="plain", help="Test type {plain|transit|end|proxy|all}")
  parser.add_option("-s", "--size", dest="size", type="string",
    default="all", help="Size type {max|min|all}")
  # Parse input parameters
  (options, args) = parser.parse_args()
  # Run proper generator according to the type
  if options.type == "plain":
    generate_plain(True, options.size)
  elif options.type == "transit":
    generate_transit(True, options.size)
  elif options.type == "end":
    generate_end(True, options.size)
  elif options.type == "proxy":
    generate_proxy(True, options.size)
  elif options.type == "all":
    generate_all(options.size)
  else:
    print "Type %s Not Supported Yet" % options.type

if __name__ == "__main__":
  generate()