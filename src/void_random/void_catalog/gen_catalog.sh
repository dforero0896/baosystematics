#!/bin/bash

rm mocksCombined*
rm -rf binned_catalogs_L/slice*
rm -rf binned_catalogs_R/slice*
./combine_mocks.sh
python gen_bins.py mocksCombined100NGC.ascii
./shuffle.sh
cat BIG_VOID_RAN_CATALOG.ascii > ~/results/BIG_VOID_RAN_CATALOG_NGC.ascii
shuf -n 2700000 ~/results/BIG_VOID_RAN_CATALOG_NGC.ascii > ~/results/ELG_MOCK_VOID_RAN_NGC.ascii

rm -rf binned_catalogs_L/slice*
rm -rf binned_catalogs_R/slice*
./combine_mocks.sh
python gen_bins.py mocksCombined100SGC.ascii
./shuffle.sh
cat BIG_VOID_RAN_CATALOG.ascii > ~/results/BIG_VOID_RAN_CATALOG_SGC.ascii
shuf -n 2700000 ~/results/BIG_VOID_RAN_CATALOG_SGC.ascii > ~/results/ELG_MOCK_VOID_RAN_SGC.ascii
