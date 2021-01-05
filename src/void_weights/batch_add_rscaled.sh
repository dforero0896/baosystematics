#!/bin/bash

source ../.env
RUN=./add_rscaled.py
for box in 1 #5
do
    for space in redshift #real 
    do



        for syst in radialgauss #smooth/parabola_0.8
        do
        VOIDIDIR=${WORKDIR}/patchy_results/box${box}/${space}/${syst}/mocks_void_xyz
        case ${syst} in
         smooth/parabola_0.8)
         #   VOIDIDIR=${VOIDIDIR}_wt
            NGAL=${WORKDIR}/patchy_results/box${box}/${space}/${syst}/plots/ngal_ang.npy
            ;;
        radialgauss)
            NGAL=${WORKDIR}/patchy_results/box${box}/${space}/${syst}/plots/ngal_radial.npy
            ;;
        esac

        srun -n100 -c1 --mpi=pmi2 ${RUN} ${NGAL} ${VOIDIDIR}/* 

    done
done
done

