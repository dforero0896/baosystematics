#!/usr/bin/env python
import os
import sys

WORKDIR = '/hpcstorage/dforero/projects/baosystematics'
RESULTS = f"{WORKDIR}/patchy_results"
if __name__ == '__main__':
    try:
        command = sys.argv[1]
    except IndexError:
        command = ''
    placeholder='PATH'
    boxes = ['box1']
    #functions = ['parabola_0.8']
    functions = ['flat_0.5', 'flat_0.55', 'flat_0.6', 'flat_0.65', 'flat_0.7', 'flat_0.75','flat_0.8', 'flat_0.85', 'flat_0.9', 'flat_0.95']#,'parabola']
    spaces = ['real', 'redshift']
    systematics = ['nosyst']
    [systematics.append(f"{a}/{b}") for a in ['noise', 'smooth'] for b in functions]
    for box in boxes:
        for space in spaces:
            for systematic in systematics:
                path = f"{RESULTS}/{box}/{space}/{systematic}"
                print(command.replace(placeholder, path))
