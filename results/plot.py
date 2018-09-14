#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

# Init steps
GRAPH = "th_ra_dr.pdf"
RESULTS_FILE = "results.txt"
X_LABEL = "Incoming Packet Rate [kpps]"
Y1_LABEL = "Outgoing Packet Rate [kpps]"
Y2_LABEL = "Delivery Ratio"

RATES = []
THROUGHPUTS = []
DELIVER_RATIOS = []
TICK = [0, 500, 1000, 1500, 2000]

# Load data from results.txt
with open(RESULTS_FILE, 'r') as file:
  lines = file.readlines()
lines = lines[0:len(lines)-1:10]

# Iterate over the lines and extract the data
for line in lines:
  data = line.split(" ")
  RATES.append(float(data[0])/1000.0)
  THROUGHPUTS.append(float(data[1])/1000.0)
  DELIVER_RATIOS.append(float(data[2]))

# Create first axis - Throughtput
fig, ax1 = plt.subplots(figsize=(6.5, 4))
lns1 = ax1.plot(RATES, THROUGHPUTS, 'black', marker='o',
          markerfacecolor='None', label='Net Throughput')
ax1.set_xlabel(X_LABEL)
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel(Y1_LABEL)
ax1.set_xlim([0, 2000])
ax1.set_ylim([0, 1500])
ax1.grid(color='lightgray')

# Create second axis - Delivery ratio
ax2 = ax1.twinx()
lns2 = ax2.plot(RATES, DELIVER_RATIOS, 'orange', marker='^',
          label='Delivery Ratio', zorder=10)
ax2.set_ylabel(Y2_LABEL)
ax2.set_xlim([0, 2000])
ax2.set_ylim([0.4, 1.0])

# added these three lines
lns = lns1+lns2
labs = [l.get_label() for l in lns]
# Create the legend
ax1.legend(lns, labs, loc='lower right')

# Save the figure
fig.savefig(GRAPH, bbox_inches='tight')