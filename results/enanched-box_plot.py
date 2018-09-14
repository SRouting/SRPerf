#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import math
import json
import sys
import re
from numpy import source

# Labels
X_LABEL = "Forwarding behavior"
Y_LABEL = "PDR (Kpps)"

# Graph output filename.
GRAPH = "graph.eps"

# Data sources.
SOURCE_FILES = {
    'Linux' :   'data/Linux.txt',
    'VPP'   :   'data/VPP.txt'
}

# We select which kind of forwading behaviour we want to report in the graph.
#
# NOTICE: every fwd behaviour MUST be generate following the grammar:
#
# FWD_NAME          := <BEHAVIOUR_NAME>@<STRING>
# BEHAVIOUR_NAME    := <STRING>-<SOLVER>
# SOLVER            : = pdr | mrr
# STRING            := [a-zA-Z0-9-_]+
#
# For example: ipv6-pdr@Linux, t_insert_v6-mrr@VPP and so on.
#
# Notice: such encoding allows us to encode in one element (avoiding another
# dictionary) the behaviour, solver and also the source at once!
LABELS_FILTER = [
    'ipv4-pdr@VPP',
    'ipv4-pdr@Linux',
    'ipv6-pdr@VPP',
    'ipv6-pdr@Linux',
]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ DATA INITIALIZATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Label filter regular expression, please look at the grammar in the example
# above.
LABEL_FILTER_REGEXPR = '^(?P<fwd>(?P<bhname>[a-zA-Z0-9-_]+)-(?:pdr|mrr))@(?P<source>[a-zA-Z0-9-_]+)$'

# Mapping between forwarding behaviour and its name real name.
LABELS_MAPPING = {
  'ipv6': 'IPv6',
  'ipv4': 'IPv4',
  't_insert_v6': 'T.Insert',
  't_encaps_v6': 'T.Encaps',
  't_encaps_l2': 'T.Encaps.L2',
  'end': 'End',
  'end_t': 'End.T',
  'end_x': 'End.X',
  'end_dx2': 'End.DX2',
  'end_dt6': 'End.DT6',
  'end_dx6': 'End.DX6'
}

DATA = []
TICK = []
DATASETS = {}

# We build dynamically the LABELS_ORDER leveraging the precedence given by the
# order in the LABELS_FILTER.
LABELS_ORDER = {}
LABELS_ORDER_COUNTER = 0
for item in LABELS_FILTER:
    LABELS_ORDER[item] = LABELS_ORDER_COUNTER
    LABELS_ORDER_COUNTER += 1

# Load data from multiple sources.
for sourceName, sourcePath in SOURCE_FILES.iteritems():
    with open(sourcePath, 'r') as fileName:
        DATASETS[sourceName] = json.load(fileName)
        
# We need to populate the DATA array used by the graph library in order to build
# the box graph. We consider the list of forwarding behaviours specified in the
# LABELS_FILTER
for item in LABELS_FILTER:
    # We do not want to have in the LABELS_MAPPING the distinction between
    # a fwd behaviour for pdr and another one for the mrr. So we need to remove
    # the pdr or mrr suffix at the end of fwdName and use the prefix as the key
    # in the LABELS_MAPPING. In this way we are able to retrieve the full 
    # real name for the behaviour.
    itemPattern = re.compile(LABEL_FILTER_REGEXPR)
    itemMatcher = itemPattern.match(item)
    if itemMatcher is None:
        print('Invalid behaviour <{0}>, please check forwarding name, solver and source'.format(item))
        sys.exit(1)
    
    # Let's extract groups (also known as tokens)
    fwdName = itemMatcher.group('fwd')
    sourceName = itemMatcher.group('source')        
    fwd = itemMatcher.group('bhname')
    
    if fwd not in LABELS_MAPPING:
        print('Unrecognized label mapping {0}'.format(fwd))
        sys.exit(1)
    if sourceName not in SOURCE_FILES:
        print('Unrecognized source mapping {0}'.format(sourceName))
        sys.exit(1)
    
    fwdNameWithSourceName = '{0} ({1})'.format(LABELS_MAPPING[fwd], sourceName)
    TICK.insert(LABELS_ORDER[item], fwdNameWithSourceName)
    
    # Results coming from the test is pps. Moreover, results coming from the 
    # right source on the basis of the sourceName parameter.
    results = DATASETS[sourceName][fwdName]
    
    kpps = []
    for result in results:
        kpps.append(float(result) / 1000)
     
    DATA.insert(LABELS_ORDER[item], kpps)

# ~~~~~~~~~~~~~~~~~~~ GRAPH INITIALIZATION AND SETTINGS ~~~~~~~~~~~~~~~~~~~~~~~~ 
 
plt.rcParams['font.size'] = 6
 
# Create figure
fig = plt.figure(1, figsize=(3, 3))
 
# Create axes instance
ax = fig.add_subplot(111)
 
# Create the boxplot
bp = ax.boxplot(DATA, 0, '', patch_artist=True)
 
# change edge color and fill color
for box in bp['boxes']:
    box.set(facecolor='w')
 
# Set tick labels
ax.set_xticklabels(TICK)
 
# Defines labels and tile
plt.ylabel(Y_LABEL)
# plt.xlabel(X_LABEL)

# Let's try to use the built-in autoscale
# Define ymin
# plt.ylim(ymin=400)
# plt.ylim(ymax=1200)
 
# Save the figure
fig.savefig(GRAPH, bbox_inches='tight')

print('Done...')
