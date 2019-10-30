#! /usr/bin/env bash
ID=$1
RAW=$2
N_JOBARRAY=$3
if [[ $3 == '' ]];
then
	N_JOBARRAY=10
fi
module use /astro/soft/modulefiles/
module unuse /etc/modulefiles
module add astro
module load python/2.7.15
#Generate necessary directory structure
bash /home/epfl/zhaoc/data/EZmock/eBOSS/ELG/obs/void/baosystematics/src/generate_file_structure.sh $ID
echo Directory structure done.
#Combine catalogs by zone
combineJobid=$(sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/combineJob/combine_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/combineJob/combine_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/combineJob.sh $RAW /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mocks_combined/ 0 | sed 's/[^0-9]*//g')
echo Combine Job $combineJobid
#Convert from sky to comoving coordinates
#Mocks
echo Convert mock galaxies from sky to comoving.
convgenid=$(sbatch --job-name=convgen --dependency=afterok:$combineJobid --wrap="python /home/epfl/dforero/zhao/void/baosystematics/src/coord_conv.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mocks_combined/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mocks_xyz_combined/ /home/epfl/dforero/zhao/void/baosystematics/src/rdz2xyz.conf $ID 0" | sed 's/[^0-9]*//g')
echo Conversion job list $convgenid
convJobid=$(bash /home/epfl/dforero/zhao/void/baosystematics/src/convJob_wrapper.sh $ID $N_JOBARRAY rdz2xyz $combineJobid:$convgenid | tail -1 | sed 's/[^0-9]*//g')
echo Coordinate conversion job $convJobid
#Run DIVE
echo Run DIVE
divegenid=$(sbatch --job-name=divegen --dependency=afterok:$convJobid --wrap="python /home/epfl/dforero/zhao/void/baosystematics/src/catalog_gen.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mocks_xyz_combined/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_catalogs/ $ID 0" | sed 's/[^0-9]*//g')
diveJobid=$(sbatch --dependency=afterok:$convJobid:$divegenid --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/diveJob/dive_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/diveJob/dive_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/diveJob.sh | sed 's/[^0-9]*//g')
echo DIVE job $diveJobid
echo Convert void catalogs from comoving to sky coordinates.
#Convert void from comoving to sky
convgenid=$(sbatch --job-name=convgen2 --dependency=afterok:$diveJobid --wrap="python /home/epfl/dforero/zhao/void/baosystematics/src/coord_conv.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_rdz_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/src/xyz2rdz.conf $ID 0" | sed 's/[^0-9]*//g')
echo Conversion job list $convgenid
convJobid=$(bash /home/epfl/dforero/zhao/void/baosystematics/src/convJob_wrapper.sh $ID $N_JOBARRAY xyz2rdz $diveJobid:$convgenid | tail -1| sed 's/[^0-9]*//g')
echo Coordinate conversion job $convJobid
#Merge catalogs into big ones to reduce I/O
echo Merging all catalogs and writing dictionaries.
sbatch --dependency=afterok:$convJobid --array=0-$(($N_JOBARRAY-1)) --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/mergeJob/merge_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/mergeJob/merge_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/mergeJob.sh /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_rdz_catalogs /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_combined_catalogs/ $N_JOBARRAY


