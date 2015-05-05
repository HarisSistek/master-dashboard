#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def get_data(f):
    data = {'time': f.readline().strip()}
    for line in f.readlines():
        if 'READ' in line and 'AverageLatency' in line:
            data['average'] = line.split(' ')[2].strip()
        elif 'READ' in line and 'MinLatency' in line:
            data['min'] = line.split(' ')[2].strip()
        elif 'READ' in line and 'MaxLatency' in line:
            data['max'] = line.split(' ')[2].strip()
        elif 'OVERALL' in line and 'Throughput' in line:
            data['throughput'] = line.split(' ')[2].strip()

    return data

def read_files(directory):
    data = {}
    for fil in os.listdir(directory):
        if 'clients' in fil:
            with open(fil, 'r') as f:
                data[fil] = get_data(f)
    return data

def write(data,tofile=False):
    for key, value in data.iteritems():
        with open(key.split('.')[0], 'a') as f:
            f.write(str(value) + '\n')

if __name__ == '__main__':
    data = read_files(os.path.dirname(os.path.realpath(__file__)))
    write(data, tofile=True)
