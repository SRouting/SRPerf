#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import math
import json

# Init steps
DATA = []
TICK = []
X_LABEL = "Forwarding behavior"
Y_LABEL = "PDR (Kpps)"
GRAPH = "pdr.pdf"
RESULTS_FILE = "results.txt"

# Load data from results.txt
with open(RESULTS_FILE, 'r') as file:
  data = json.load(file)
for key, results in data.iteritems():
  TICK.append(key)
  # Results coming from the test is pps
  kpps = []
  for result in results:
    kpps.append(float(result)/1000)
  DATA.append(kpps)

# Create figure
fig = plt.figure(1, figsize=(9, 6))

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
plt.xlabel(X_LABEL)

# Define ymin
plt.ylim(ymin=200)
plt.ylim(ymax=1500)

# Save the figure
fig.savefig(GRAPH, bbox_inches='tight')