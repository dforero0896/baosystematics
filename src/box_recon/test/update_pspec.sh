#!/bin/bash

OLDPWD=$PWD
cd ../../powspec/ && bash compute_gal_powspec.sh | bash
cd ${OLDPWD}
cd ../../powspec/ && bash compute_gal_recon_powspec.sh | bash
