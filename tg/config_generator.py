#!/usr/bin/python

import yaml
from optparse import OptionParser

CONFIG_FILE = "config.yaml"

def generate_config(configs=[]):
  with open(CONFIG_FILE, 'w') as outfile:
    outfile.write(yaml.dump(configs, default_flow_style=False))

# Generate config for all tests
def generate_all():
  configs = []
  configs.extend(generate_plain(False))
  configs.extend(generate_transit(False))
  configs.extend(generate_end(False))
  configs.extend(generate_proxy(False))
  # Write the entire configuration
  generate_config(configs)

# Generate config for plain tests
def generate_plain(generate=True):
  configs = [
    {'type': 'plain', 'experiment': 'ipv6', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'plain', 'experiment': 'ipv6', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'plain', 'experiment': 'ipv6', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'plain', 'experiment': 'ipv6', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'plain', 'experiment': 'ipv4', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'plain', 'experiment': 'ipv4', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'plain', 'experiment': 'ipv4', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'plain', 'experiment': 'ipv4', 'size': 'min', 'rate': 'mrr', 'run': 1}
  ]
  if not generate:
    return configs
  # Write the PLAIN configuration
  generate_config(configs)

# Generate config for transit tests
def generate_transit(generate=True):
  configs = [
    {'type': 'srv6', 'experiment': 't_encaps_v6', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 't_encaps_v6', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 't_encaps_v6', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 't_encaps_v6', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 't_encaps_v4', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 't_encaps_v4', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 't_encaps_v4', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 't_encaps_v4', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 't_encaps_l2', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 't_encaps_l2', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 't_encaps_l2', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 't_encaps_l2', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 't_insert_v6', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 't_insert_v6', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 't_insert_v6', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 't_insert_v6', 'size': 'min', 'rate': 'mrr', 'run': 1}
  ]
  if not generate:
    return configs
  # Write the TRANSIT configuration
  generate_config(configs)    

# Generate config for end tests
def generate_end(generate=True):
  configs = [
    {'type': 'srv6', 'experiment': 'end', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_x', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_x', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_x', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_x', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_t', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_t', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_t', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_t', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_b6', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_b6', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_b6', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_b6', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_b6_encaps', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_b6_encaps', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_b6_encaps', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_b6_encaps', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_dx6', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_dx6', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_dx6', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_dx6', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_dx4', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_dx4', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_dx4', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_dx4', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_dx2', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_dx2', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_dx2', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_dx2', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_dt6', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_dt6', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_dt6', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_dt6', 'size': 'min', 'rate': 'mrr', 'run': 1}
  ]
  if not generate:
    return configs
  # Write the END configuration
  generate_config(configs)

# Generate config for proxy tests
def generate_proxy(generate=True):
  configs = [
    {'type': 'srv6', 'experiment': 'end_ad6', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_ad6', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_ad6', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_ad6', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_ad4', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_ad4', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_ad4', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_ad4', 'size': 'min', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_am', 'size': 'max', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_am', 'size': 'max', 'rate': 'mrr', 'run': 1},
    {'type': 'srv6', 'experiment': 'end_am', 'size': 'min', 'rate': 'pdr', 'run': 10},
    {'type': 'srv6', 'experiment': 'end_am', 'size': 'min', 'rate': 'mrr', 'run': 1}
  ]
  if not generate:
    return configs
  # Write the PROXY configuration
  generate_config(configs)

# Parse options
def generate():
  # Init cmd line parse
  parser = OptionParser()
  parser.add_option("-t", "--type", dest="type", type="string",
    default="plain", help="Test type {plain|transit|end|proxy|all}")
  # Parse input parameters
  (options, args) = parser.parse_args()
  # Run proper generator according to the type
  if options.type == "plain":
    generate_plain()
  elif options.type == "transit":
    generate_transit()
  elif options.type == "end":
    generate_end()
  elif options.type == "proxy":
    generate_proxy()
  elif options.type == "all":
    generate_all()
  else:
    print "Type %s Not Supported Yet" % options.type

if __name__ == "__main__":
  generate()