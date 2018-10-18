#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import math
import json
import math

RESULTS_FILE = "results.txt"
OUT = {}
MEAN = "mean"
CV = "cv"
CI_95 = "ci_95"

# Load data from results.txt
with open(RESULTS_FILE, 'r') as file:
  data = json.load(file)
for key, results in data.iteritems():
  # Let's create a dict inside the dict
  metrics = {}
  # Calculate mean
  temp = 0
  for result in results:
    result = float(result)/1000
    temp = temp + result
  mean = float(temp)/len(results)
  metrics[MEAN] = mean
  # Calculate variance
  for result in results:
    result = float(result)/1000
    temp = math.pow(result - mean, 2)
  variance = float(temp)/(len(results) - 1)
  dev = math.sqrt(variance)
  cv = float(dev/mean)
  cv = cv * 100
  metrics[CV] = cv
  ci_95 = (2 * cv)/math.sqrt(len(results))
  metrics[CI_95] = ci_95
  OUT[key] = metrics
# dump the results
print json.dumps(OUT)
