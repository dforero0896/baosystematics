#!/usr/bin/env bash
# This script skips the step of generating the catalogs with systematics.
if [[ $# -gt 3 ]] && [[ $# -lt 7 ]]; then
	ascii_filename_dat=$1 #Path to the mock data.
	results_dir=$2 #Path to the results directory.
	overwrite=$3 #Overwriting flag.
	sys_effect_1=$4
	sys_effect_2=$5
	sys_effect_3=$6
else
	echo "ERROR: Unxepected number of arguments."
	echo "USAGE: bash $0 IN_FILENAME RESULTS_DIR OVERWRITE SYS_EFFECT [SYS_EFFECT SYS_EFFECT]"
	exit 1
fi
[[ "${results_dir}" == */ ]] && results_dir="${results_dir: : -1}"
if [[ ! -e $results_dir ]]; then
	mkdir -v $results_dir
fi
if [[ ! -e $ascii_filename_dat ]]; then
	echo ERROR: Data catalog not found.
	exit 1
fi
if [[ $(echo $ascii_filename_dat | grep .dat.) == '' ]]; then
	echo ERROR: Input is not a data catalog.
	exit 1
fi
ascii_filename_ran=$(echo $ascii_filename_dat | sed -e 's/\.dat\./.ran./g')
if [[ ! -e $ascii_filename_ran ]]; then
	echo ERROR: Random catalog not found.
	exit 1
fi
echo CONVERT SKY TO COMOVING COORDINATES
mocks_gal_xyz=$results_dir/mocks_gal_xyz
if [[ ! -e $mocks_gal_xyz ]]; then
	mkdir -v $mocks_gal_xyz
fi
xyz_filename_dat=$mocks_gal_xyz/$(basename $ascii_filename_dat | sed -e 's/ELG/ELG_XYZ/g')
xyz_filename_ran=$mocks_gal_xyz/$(basename $ascii_filename_ran | sed -e 's/ELG/ELG_XYZ/g')
if [[ ! -e $xyz_filename_dat ]]; then
	/global/cscratch1/sd/dforero/baosystematics/bin/rdz2xyz -c /global/cscratch1/sd/dforero/baosystematics/src/coord_conv/rdz2xyz.conf -i $ascii_filename_dat -o $xyz_filename_dat
elif [[ $overwrite -eq 1 ]]; then
	rm -v $xyz_filename_dat
	/global/cscratch1/sd/dforero/baosystematics/bin/rdz2xyz -c /global/cscratch1/sd/dforero/baosystematics/src/coord_conv/rdz2xyz.conf -i $ascii_filename_dat -o $xyz_filename_dat
fi
if [[ ! -e $xyz_filename_ran ]]; then
	/global/cscratch1/sd/dforero/baosystematics/bin/rdz2xyz -c /global/cscratch1/sd/dforero/baosystematics/src/coord_conv/rdz2xyz.conf -i $ascii_filename_ran -o $xyz_filename_ran
elif [[ $overwrite -eq 1 ]]; then
	rm -v $xyz_filename_ran
	/global/cscratch1/sd/dforero/baosystematics/bin/rdz2xyz -c /global/cscratch1/sd/dforero/baosystematics/src/coord_conv/rdz2xyz.conf -i $ascii_filename_ran -o $xyz_filename_ran
fi


echo CREATE VOID CATALOGS
mocks_void_xyz=$results_dir/mocks_void_xyz
if [[ ! -e $mocks_void_xyz ]]; then
	mkdir -v $mocks_void_xyz
fi
raw_void_filename_dat=$mocks_void_xyz/$(basename $xyz_filename_dat | sed -e 's/\.dat\./.VOID.dat./g')
if [[ ! -e $raw_void_filename_dat ]]; then
	/global/cscratch1/sd/dforero/baosystematics/bin/DIVE $xyz_filename_dat $raw_void_filename_dat
elif [[ $overwrite -eq 1 ]]; then
	rm -v $raw_void_filename_dat
	/global/cscratch1/sd/dforero/baosystematics/bin/DIVE $xyz_filename_dat $raw_void_filename_dat
fi

echo CONVERT VOID CATALOGS FROM COMOVING TO SKY COORDINATES
mocks_void_rdz=$results_dir/mocks_void_rdz
if [[ ! -e $mocks_void_rdz ]]; then
	mkdir -v $mocks_void_rdz
fi
rdz_void_filename_dat=$mocks_void_rdz/$(basename $raw_void_filename_dat | sed -e 's/ELG/ELG_RDZ/g')
if [[ ! -e $rdz_void_filename_dat ]]; then
	/global/cscratch1/sd/dforero/baosystematics/bin/xyz2rdz -c /global/cscratch1/sd/dforero/baosystematics/src/coord_conv/xyz2rdz.conf -i $raw_void_filename_dat -o $rdz_void_filename_dat
elif [[ $overwrite -eq 1 ]]; then
	rm -v $rdz_void_filename_dat
	/global/cscratch1/sd/dforero/baosystematics/bin/xyz2rdz -c /global/cscratch1/sd/dforero/baosystematics/src/coord_conv/xyz2rdz.conf -i $raw_void_filename_dat -o $rdz_void_filename_dat
fi





