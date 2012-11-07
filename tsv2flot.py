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
      x_points.append(float(row[xcol]))
      y_points.append(float(row[ycol]))

  return (x_points, y_points)

def main():
  parser = argparse.ArgumentParser(description = 'Generate a single series object from a TSV file')
  parser.add_argument('-f', type=str, help='TSV Filename')
  parser.add_argument('-xcol', type=int, default=0, help='X Column (zero-based)')
  parser.add_argument('-ycol', type=int, required=True, help='Y Column (zero-based)')
  parser.add_argument('-l', type=str, required=True, help='Series label')
  args = parser.parse_args()

  x_points, y_points = parse_csv(args.f, args.xcol, args.ycol)
  obj = generate_series(x_points, y_points, args.l)
  print(json.dumps(obj))

if __name__ == '__main__':
  main()