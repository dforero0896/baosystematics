#!/bin/bash
find patchy_results/ -wholename '*plots/*' | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_results/ -name '*.npy' | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_results/ -name '*mockavg*' | xargs -I '{}' cp -u -v {} --parents reports/
find results/ -name '*.pdf' | xargs -I '{}' cp -u -v {} --parents reports/
find lrg_results/ -name '*.pdf' | xargs -I '{}' cp -u -v {} --parents reports/
