#!/usr/bin/env python

import json
import csv
import argparse

def generate_series(x_points, y_points, label):
  data = zip(x_points, y_points)
  obj = {
    'label': label,
    'data': data
  }

  return obj

def parse_csv(filename, xcol, ycol):
  with open(filename, 'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter = '\t')
    field_names = reader.next()
    
    x_points = []
    y_points = []

    for row in reader:
      x_points.append(round(float(row[xcol]), 2))
      y_points.append(round(float(row[ycol]), 2))

  return (x_points, y_points)

def find_ymax(x_points, y_points):
  ymax = max(y_points)
  x = x_points[y_points.index(ymax)]

  return (x, ymax)

def main():
  parser = argparse.ArgumentParser(description = 'Generate a single series object from a TSV file')
  parser.add_argument('-f', type=str, help='TSV Filename')
  parser.add_argument('-xcol', type=int, default=0, help='X Column (zero-based)')
  parser.add_argument('-ycol', type=int, required=True, help='Y Column (zero-based)')
  parser.add_argument('-l', type=str, required=True, help='Series label')
  parser.add_argument('-ymax', action='store_true', help='print out max value from the Y column, instead of a series object')
  args = parser.parse_args()

  x_points, y_points = parse_csv(args.f, args.xcol, args.ycol)

  if (args.ymax):
    print(json.dumps(find_ymax(x_points, y_points)))
  else:
    obj = generate_series(x_points, y_points, args.l)
    print(json.dumps(obj))

if __name__ == '__main__':
  main()