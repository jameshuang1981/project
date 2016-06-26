from __future__ import division
import math
import sys
import os
import csv

import numpy as np
import matplotlib.pyplot as plt

from scipy.stats.stats import pearsonr

dic = {}

# read file and get dic
def read_input_file(file):
  if '\0' in open(file).read():
    print("have null byte")

  with open(file, 'r') as f:
    spamreader = list(csv.reader(x.replace('\0', '') for x in f))
    #for i in range(20):
    for i in range(len(spamreader)):
      #for j in range(10):
      for j in range(len(spamreader[i])):
        if not j in dic:
          dic[j] = []
        # print spamreader[i][j]
        val = float(spamreader[i][j])
        dic[j].append(val)


# get cross correlation and write file
def write_output_file(file):
  with open(file, 'wb') as f:
    spamwriter = csv.writer(f, delimiter = ',')
    var_var_cros_corr_LL = []
    for var_i in dic:
      for var_j in dic:
        if var_i < var_j:
          print [var_i, var_j]
          val_L_i = dic[var_i]
          val_L_j = dic[var_j]
          #print [val_L_i, val_L_j]
          cros_corr = pearsonr(val_L_i, val_L_j)
          cros_corr = cros_corr[0]
          print cros_corr
          if not math.isnan(cros_corr):
            var_var_cros_corr_LL.append([var_i, var_j, cros_corr])
    var_var_cros_corr_LL = sorted(var_var_cros_corr_LL, key = lambda x: x[2])
    for var_var_cros_corr_L in var_var_cros_corr_LL:
      spamwriter.writerow(var_var_cros_corr_L)


# main function        
if __name__ == "__main__":
  if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])

  for file in os.listdir(sys.argv[1]):
    if file.endswith("-new.csv"):
      print file
      read_input_file(sys.argv[1] + file)
      write_output_file(sys.argv[2] + file)
