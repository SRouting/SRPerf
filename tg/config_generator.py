#!/usr/bin/python

from optparse import OptionParser

CONFIG_FILE = "config.txt"

def generate_config(configs=[]):
  with open(CONFIG_FILE, 'w') as outfile:
    for config in configs:
      outfile.write(config)

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
  "plain\tipv6\tmax\tpdr\n",
  "plain\tipv6\tmax\tmrr\n",
  "plain\tipv6\tmin\tpdr\n",
  "plain\tipv6\tmin\tmrr\n",
  "plain\tipv4\tmax\tpdr\n",
  "plain\tipv4\tmax\tmrr\n",
  "plain\tipv4\tmin\tpdr\n",
  "plain\tipv4\tmin\tmrr\n"
  ]
  if not generate:
    return configs
  # Write the PLAIN configuration
  generate_config(configs)

# Generate config for transit tests
def generate_transit(generate=True):
  configs = [
  "srv6\tt_encaps_v6\tmax\tpdr\n",
  "srv6\tt_encaps_v6\tmax\tmrr\n",
  "srv6\tt_encaps_v6\tmin\tpdr\n",
  "srv6\tt_encaps_v6\tmin\tmrr\n",
  "srv6\tt_encaps_v4\tmax\tpdr\n",
  "srv6\tt_encaps_v4\tmax\tmrr\n",
  "srv6\tt_encaps_v4\tmin\tpdr\n",
  "srv6\tt_encaps_v4\tmin\tmrr\n",
  "srv6\tt_encaps_l2\tmax\tpdr\n",
  "srv6\tt_encaps_l2\tmax\tmrr\n",
  "srv6\tt_encaps_l2\tmin\tpdr\n",
  "srv6\tt_encaps_l2\tmin\tmrr\n",
  "srv6\tt_insert_v6\tmax\tpdr\n",
  "srv6\tt_insert_v6\tmax\tmrr\n",
  "srv6\tt_insert_v6\tmin\tpdr\n",
  "srv6\tt_insert_v6\tmin\tmrr\n"
  ]
  if not generate:
    return configs
  # Write the TRANSIT configuration
  generate_config(configs)    

# Generate config for end tests
def generate_end(generate=True):
  configs = [
  "srv6\tend\tmax\tpdr\n",
  "srv6\tend\tmax\tmrr\n",
  "srv6\tend\tmin\tpdr\n",
  "srv6\tend\tmin\tmrr\n",
  "srv6\tend_x\tmax\tpdr\n",
  "srv6\tend_x\tmax\tmrr\n",
  "srv6\tend_x\tmin\tpdr\n",
  "srv6\tend_x\tmin\tmrr\n",
  "srv6\tend_t\tmax\tpdr\n",
  "srv6\tend_t\tmax\tmrr\n",
  "srv6\tend_t\tmin\tpdr\n",
  "srv6\tend_t\tmin\tmrr\n",
  "srv6\tend_b6\tmax\tpdr\n",
  "srv6\tend_b6\tmax\tmrr\n",
  "srv6\tend_b6\tmin\tpdr\n",
  "srv6\tend_b6\tmin\tmrr\n",
  "srv6\tend_b6_encaps\tmax\tpdr\n",
  "srv6\tend_b6_encaps\tmax\tmrr\n",
  "srv6\tend_b6_encaps\tmin\tpdr\n",
  "srv6\tend_b6_encaps\tmin\tmrr\n",
  "srv6\tend_dx6\tmax\tpdr\n",
  "srv6\tend_dx6\tmax\tmrr\n",
  "srv6\tend_dx6\tmin\tpdr\n",
  "srv6\tend_dx6\tmin\tmrr\n",
  "srv6\tend_dx4\tmax\tpdr\n",
  "srv6\tend_dx4\tmax\tmrr\n",
  "srv6\tend_dx4\tmin\tpdr\n",
  "srv6\tend_dx4\tmin\tmrr\n",
  "srv6\tend_dx2\tmax\tpdr\n",
  "srv6\tend_dx2\tmax\tmrr\n",
  "srv6\tend_dx2\tmin\tpdr\n",
  "srv6\tend_dx2\tmin\tmrr\n",
  "srv6\tend_dt6\tmax\tpdr\n",
  "srv6\tend_dt6\tmax\tmrr\n",
  "srv6\tend_dt6\tmin\tpdr\n",
  "srv6\tend_dt6\tmin\tmrr\n",
  ]
  if not generate:
    return configs
  # Write the END configuration
  generate_config(configs)

# Generate config for proxy tests
def generate_proxy(generate=True):
  configs = [
  "srv6\tend_ad6\tmax\tpdr\n",
  "srv6\tend_ad6\tmax\tmrr\n",
  "srv6\tend_ad6\tmin\tpdr\n",
  "srv6\tend_ad6\tmin\tmrr\n",
  "srv6\tend_ad4\tmax\tpdr\n",
  "srv6\tend_ad4\tmax\tmrr\n",
  "srv6\tend_ad4\tmin\tpdr\n",
  "srv6\tend_ad4\tmin\tmrr\n",
  "srv6\tend_am\tmax\tpdr\n",
  "srv6\tend_am\tmax\tmrr\n",
  "srv6\tend_am\tmin\tpdr\n",
  "srv6\tend_am\tmin\tmrr\n"
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