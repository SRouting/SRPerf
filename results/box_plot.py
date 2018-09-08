#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import math
import json

# Init steps
DATA = [0, 0, 0, 0]
TICK = ['', '', '', '']
X_LABEL = "Forwarding behavior"
Y_LABEL = "PDR (Kpps)"
GRAPH = "end_slow.pdf"
RESULTS_FILE = "results.txt"
#FONT_SIZE = 19
# Labels mapping and o
LABELS_MAPPING = {
  'ipv6': 'IPv6',
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
LABELS_ORDER = {
  'ipv6': 0,
  't_insert_v6': 1,
  't_encaps_v6': 2,
  't_encaps_l2': 3,
  'end': 1,
  'end_t': 2,
  'end_x': 3,
  'end_dx2': 1,
  'end_dt6': 2,
  'end_dx6': 3
}

# Load data from results.txt
with open(RESULTS_FILE, 'r') as file:
  data = json.load(file)
for key, results in data.iteritems():
  TICK.insert(LABELS_ORDER[key], LABELS_MAPPING[key])
  # Results coming from the test is pps
  kpps = []
  for result in results:
    kpps.append(float(result)/1000)
  DATA.insert(LABELS_ORDER[key], kpps)

# Filter out place older
TICK = filter(lambda a: a != '', TICK)
DATA = filter(lambda a: a != 0, DATA)

# Update font size
#plt.rcParams.update({'font.size': FONT_SIZE})

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
#plt.xlabel(X_LABEL)

# Define ymin
plt.ylim(ymin=80)
plt.ylim(ymax=130)

# Save the figure
fig.savefig(GRAPH, bbox_inches='tight')