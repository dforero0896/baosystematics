#!/bin/bash
WORKDIR=/home/epfl/dforero/scratch/projects/baosystematics
RUN=$WORKDIR/bin/make_survey/mply_trim
RUN_COMP=$WORKDIR/bin/eBOSS_completeness.py
MASKS=$WORKDIR/data/LRG_masks
GEOM_SURV=$WORKDIR/data/LRG_geometry/eboss_geometry_eboss0_eboss27
COMP_LRG=$WORKDIR/data/LRG_geometry/eBOSS_LRGgeometry_v7.fits
if [[ $# -ne 1 ]]; then
echo ERROR: Unexpected number of arguments
echo USAGE $0 INPUT_CATALOG
exit 1
fi
in_catalog=$1
in_dir=$(dirname $in_catalog)
out_dir="$in_dir"_finalmask
tmp_catalog=$out_dir/$(basename $in_catalog | sed -e 's/VOID/VOID.MASKED.TMP/g')
new_in_catalog=$out_dir/$(basename $in_catalog | sed -e 's/VOID/VOID.MASKED.TMPNEWIN/g')
out_catalog=$out_dir/$(basename $in_catalog | sed -e 's/VOID/VOID.MASKED/g')
if [[ -e $out_catalog ]] ;then
echo File $out_catalog already exists and not overwritten. Skipping.
exit 0
fi 
echo Applying survey geometry mask.
$RUN $in_catalog $GEOM_SURV".ply" 0 F > $tmp_catalog
mv $tmp_catalog $new_in_catalog
echo Applying selection wrt completeness.
$RUN_COMP $GEOM_SURV $COMP_LRG $new_in_catalog $tmp_catalog
mv $tmp_catalog $new_in_catalog

#mv $new_in_catalog $out_catalog
#exit 0
### Up to here to fix old ones
for mask in $(ls -d $MASKS/*)
do
echo Applying mask $mask
$RUN $new_in_catalog $mask 1 T > $tmp_catalog
mv $tmp_catalog $new_in_catalog
done
mv $new_in_catalog $out_catalog
