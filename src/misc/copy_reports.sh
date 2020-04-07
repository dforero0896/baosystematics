#!/bin/bash
find patchy_results/ -name '*.pdf' | xargs -I '{}' cp -u -v {} --parents reports/
find results/ -name '*.pdf' | xargs -I '{}' cp -u -v {} --parents reports/
find lrg_results/ -name '*.pdf' | xargs -I '{}' cp -u -v {} --parents reports/
