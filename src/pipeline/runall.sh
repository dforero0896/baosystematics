#! /usr/bin/env bash
ID=$1
RAW=$2
N_JOBARRAY=$3
if [[ $3 == '' ]];
then
	N_JOBARRAY=10
fi
## Pipeline
#Generate necessary directory structure
/home/epfl/dforero/zhao/void/baosystematics/src/generate_file_structure.sh $ID
#Combine catalogs by zone
sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/combineJob/combine_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/combineJob/combine_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/combineJob.sh /home/epfl/zhaoc/data/EZmock/eBOSS/ELG/obs/EZ_clustering_v4_mask-all_photo-hplin_cp-colgroup_noz-fitplatesnfitfiberid_randz-window-MODEL_Z-10-10 /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mocks_combined/ 0

#Convert from sky to comoving coordinates
#Mocks
python /home/epfl/dforero/zhao/void/baosystematics/src/coord_conv.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mocks_combined/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mocks_xyz_combined/ /home/epfl/dforero/zhao/void/baosystematics/src/rdz2xyz.conf $ID 0
#Obs
python /home/epfl/dforero/zhao/void/baosystematics/src/coord_conv.py /home/epfl/dforero/zhao/void/baosystematics/data/$ID/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_xyz/ /home/epfl/dforero/zhao/void/baosystematics/src/rdz2xyz.conf $ID 0

#Mocks 
bash /home/epfl/dforero/zhao/void/baosystematics/src/convJob_wrapper.sh $ID $N_JOBARRAY rdz2xyz
#Obs
bash /home/epfl/dforero/zhao/void/baosystematics/src/convJob_wrapper.sh $ID 4 rdz2xyz

#Mocks
python /home/epfl/dforero/zhao/void/baosystematics/src/catalog_gen.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mocks_xyz_combined/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_catalogs/ $ID 0
#Obs
python /home/epfl/dforero/zhao/void/baosystematics/src/catalog_gen.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_xyz/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_catalogs/ $ID 0

#Mocks and Obs
sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/diveJob/dive_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/diveJob/dive_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/diveJob.sh


#Mocks
python /home/epfl/dforero/zhao/void/baosystematics/src/coord_conv.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_rdz_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/src/xyz2rdz.conf $ID 0
#Obs
python /home/epfl/dforero/zhao/void/baosystematics/src/coord_conv.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_rdz_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/src/xyz2rdz.conf $ID 1
#Mocks
bash /home/epfl/dforero/zhao/void/baosystematics/src/convJob_wrapper.sh $ID 10 xyz2rdz DEPENDENCYID
#Obs
bash /home/epfl/dforero/zhao/void/baosystematics/src/convJob_wrapper.sh $ID 2 xyz2rdz DEPENDENCYID

#Mocks
sbatch --array=0-9 --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/mergeJob/merge_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/mergeJob/merge_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/mergeJob.sh /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_rdz_catalogs /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_combined_catalogs/ 10
#Obs (Not preferred approach)
sbatch --array=0-9 --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/mergeJob/merge_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/mergeJob/merge_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/mergeJob.sh /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_rdz_catalogs /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_combined_catalogs/ 2


#Mocks (preferred)
python /home/epfl/dforero/zhao/void/baosystematics/src/catalog_mask.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_combined_catalogs /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_combined_masked_catalogs /home/epfl/dforero/zhao/void/baosystematics/src/brickmask.conf $ID 1
#Obs 
python /home/epfl/dforero/zhao/void/baosystematics/src/catalog_mask.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_combined_catalogs /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_combined_masked_catalogs /home/epfl/dforero/zhao/void/baosystematics/src/brickmask.conf $ID 1
```
 If mask is to be applied to separated ascii catalogs
```
#Mocks 
python /home/epfl/dforero/zhao/void/baosystematics/src/catalog_mask.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_rdz_catalogs /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_masked_catalogs /home/epfl/dforero/zhao/void/baosystematics/src/brickmask.conf $ID 1
#Obs (preferred)
python /home/epfl/dforero/zhao/void/baosystematics/src/catalog_mask.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_rdz_catalogs /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_masked_catalogs /home/epfl/dforero/zhao/void/baosystematics/src/brickmask.conf $ID 1
```
In any case, submit job with help of the wrapper script (TODO: helper files to `vetomask` should be moved to the `data` directory of the project)
```
bash /home/epfl/dforero/zhao/void/baosystematics/src/maskJob_wrapper.sh $ID 10 DEPENDENCYID

```
Trim catalogs by selecting lines with `VETOMASK=1`
If files were merged for masking, do
```
python /home/epfl/dforero/zhao/void/baosystematics/src/trim_masked_fits.py INPUT_PATH OUTPUT_PATH N_SLICES THIS_SLICE OVERWRITE(int)

/*
python /home/epfl/dforero/zhao/void/baosystematics/src/trim_masked_fits.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_combined_masked_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_masked_trimmed_catalogs/ 10 SLURM_TASK 0
*/
#Mocks (preferred)
sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/split_trimJob/split_trim_%j_%A_%a_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/split_trimJob/split_trim_%j_%A_%a_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/split_trim_fitsJob.sh /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_combined_masked_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_masked_trimmed_catalogs/ 10 1
#Obs
sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/split_trimJob/split_trim_%j_%A_%a_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/split_trimJob/split_trim_%j_%A_%a_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/split_trim_fitsJob.sh /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_combined_masked_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_masked_trimmed_catalogs/ 2 1

```
If not, do

```
mpiexec python /home/epfl/dforero/zhao/void/baosystematics/src/trim_masked_ascii.py INPUT_PATH OUTPUT_PATH OVERWRITE(int)

sbatch /home/epfl/dforero/zhao/void/baosystematics/src/split_trim_asciiJob.sh INPUT_PATH OUTPUT_PATH OVERWRITE(int)

#Mocks
sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/split_trimJob/split_trim_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/split_trimJob/split_trim_%j_%x.err --ntasks=10 /home/epfl/dforero/zhao/void/baosystematics/src/split_trim_asciiJob.sh /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_masked_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_masked_trimmed_catalogs/ 1

#Obs (preferred)
sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/split_trimJob/split_trim_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/split_trimJob/split_trim_%j_%x.err --ntasks=2 /home/epfl/dforero/zhao/void/baosystematics/src/split_trim_asciiJob.sh /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_masked_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_masked_trimmed_catalogs/ 1

```

+ Now, generate random void catalog
```
#NGC ran void catalog
bash /home/epfl/dforero/zhao/void/baosystematics/src/void_ran_gen.sh /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_masked_trimmed_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/RAW_RAN_VOID_NGC.ascii NGC 100
# Load python 2.7.15
python /home/epfl/dforero/zhao/void/baosystematics/src/void_ran_gen.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/RAW_RAN_VOID_NGC.ascii /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/BIG_RAN_VOID_NGC.ascii 1

shuf -n 2700000 /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/BIG_RAN_VOID_NGC.ascii> /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/EZ_ELG_RDZ_void_ran_NGC.ascii

#SGC ran void catalog
bash /home/epfl/dforero/zhao/void/baosystematics/src/void_ran_gen.sh /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_masked_trimmed_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/RAW_RAN_VOID_SGC.ascii SGC 100

python /home/epfl/dforero/zhao/void/baosystematics/src/void_ran_gen.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/RAW_RAN_VOID_SGC.ascii /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/BIG_RAN_VOID_SGC.ascii 1

shuf -n 2700000 /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/BIG_RAN_VOID_SGC.ascii> /home/epfl/dforero/zhao/void/baosystematics/results/$ID/void_ran/EZ_ELG_RDZ_void_ran_SGC.ascii

```
+ Finally, start computing 2PCF
For galaxy catalogs
```
python fcfc.py INPUT_PATH OUTPUT_PATH JOB_LIST_ID CONF_FILE R_MIN R_MAX OVERWRITE

#Mocks
python /home/epfl/dforero/zhao/void/baosystematics/src/fcfc.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mocks_combined/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_gal_mock/ $ID /home/epfl/dforero/zhao/void/baosystematics/src/fcfc_mock_gal.conf NA NA 1

sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/fcfcJob/fcfc_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/fcfcJob/fcfc_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/fcfcJob.sh


#Obs
python /home/epfl/dforero/zhao/void/baosystematics/src/fcfc.py /home/epfl/dforero/zhao/void/baosystematics/data/$ID/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_gal_obs/ $ID /home/epfl/dforero/zhao/void/baosystematics/src/fcfc_obs_gal.conf NA NA 1

sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/fcfcJob/fcfc_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/fcfcJob/fcfc_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/fcfcJob.sh

```
For void catalogs
```
#Mocks
python /home/epfl/dforero/zhao/void/baosystematics/src/fcfc.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/mock_void_masked_trimmed_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_void_mock/ $ID /home/epfl/dforero/zhao/void/baosystematics/src/fcfc_all_void.conf 16 50 1

sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/fcfcJob/fcfc_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/fcfcJob/fcfc_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/fcfcJob.sh

#Obs
python /home/epfl/dforero/zhao/void/baosystematics/src/fcfc.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/obs_void_masked_trimmed_catalogs/ /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_void_obs/ $ID /home/epfl/dforero/zhao/void/baosystematics/src/fcfc_all_void.conf 16 50 1

sbatch --output=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/fcfcJob/fcfc_%j_%x.out --error=/home/epfl/dforero/zhao/void/baosystematics/results/$ID/fcfcJob/fcfc_%j_%x.err /home/epfl/dforero/zhao/void/baosystematics/src/fcfcJob.sh

```
+ Avergage mock 2pcf
```
average_2PCF.py IN_PATH OUT_PATH NAME
or
average_2PCF.py IN_PATH OUT_PATH CAT_TYPE ZONE ID

#Mock Galaxies
python /home/epfl/dforero/zhao/void/baosystematics/src/average_2PCF.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_gal_mock /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_gal_mock_avg gal ngc $ID

python /home/epfl/dforero/zhao/void/baosystematics/src/average_2PCF.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_gal_mock /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_gal_mock_avg gal sgc $ID
#Mock Voids
python /home/epfl/dforero/zhao/void/baosystematics/src/average_2PCF.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_void_mock /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_void_mock_avg void ngc $ID

python /home/epfl/dforero/zhao/void/baosystematics/src/average_2PCF.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_void_mock /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_void_mock_avg void sgc $ID

```
Do the plots

```
Usage: plot2pcf.py OBS_IN MOCK_IN OUT_PATH
#Voids
python /home/epfl/dforero/zhao/void/baosystematics/src/plot2pcf.py /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_void_obs /home/epfl/dforero/zhao/void/baosystematics/results/$ID/tpcf_void_mock_avg /home/epfl/dforero/zhao/void/baosystematics/results/plots_all/
# Should this code plot automatically all available 2pcf? For instance, use cat_type/region extracted from mock filename to look for the obs files.

```
Combine paircounts by zones
```
# Obs Gal
python /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/src/combine_paircounts.py /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/results/$ID/tpcf_gal_obs /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/results/$ID/tpcf_gal_obs_cbz
#Obs Voids
python /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/src/combine_paircounts.py /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/results/$ID/tpcf_void_obs /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/results/$ID/tpcf_void_obs_cbz

# Mock Gal
python /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/src/combine_paircounts.py /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/results/$ID/tpcf_gal_mock /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/results/$ID/tpcf_gal_mock_cbz
#Mock Voids
python /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/src/combine_paircounts.py /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/results/$ID/tpcf_void_mock /hpcstorage/zhaoc/EZmock/eBOSS/ELG/obs/void/baosystematics/results/$ID/tpcf_void_mock_cbz

```


TODO:	Combine galaxies and voids.
		do plots and compute fits
		Create script to build file structure
		Generalize this documentation with environment variables.
