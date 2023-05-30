#!/bin/bash

#-------------------------------------------------------------------------------

INPUT_DIR=.
OUTPUT_DIR=.
VCF_FILE_LIST=(test-SUBERINTRO-AL-samples-filtered2.vcf test-SUBERINTRO-EN-samples-filtered2.vcf)
VCF_FILE_LIST_TEXT=''
for VCF_FILE in "${VCF_FILE_LIST[@]}"; do
    VCF_FILE_LIST_TEXT="$VCF_FILE_LIST_TEXT $OUTPUT_DIR/$VCF_FILE.gz"
done
WMD_VCF_FILE=test-SUBERINTRO-ALandEN-samples-filtered2-wmd.vcf
OUTPUT_VCF_FILE=test-SUBERINTRO-ALandEN-samples-filtered2.vcf

#-------------------------------------------------------------------------------

echo 'Compressing and indexing VCF files:'
source activate tabix
for VCF_FILE in "${VCF_FILE_LIST[@]}"; do
    echo "    Compressing $VCF_FILE ..."
    bgzip -c $INPUT_DIR/$VCF_FILE > $OUTPUT_DIR/$VCF_FILE.gz
    RC=$?
    if [ $RC -ne 0 ]; then echo "*** ERROR: bgzip ended with $RC.";  exit 1; fi
    echo '    File is compressed.'
    echo "    Indexing $VCF_FILE.gz ..."
    parallel tabix -p vcf ::: $OUTPUT_DIR/$VCF_FILE.gz
    RC=$?
    if [ $RC -ne 0 ]; then echo "*** ERROR: parallel tabix RC: $RC."; exit 1; fi
    echo '    File is indexed.'
done
conda deactivate

#-------------------------------------------------------------------------------

echo 'Merging VCF files ...'
source activate bcftools
bcftools merge --output-type v --output $OUTPUT_DIR/$WMD_VCF_FILE $VCF_FILE_LIST_TEXT
RC=$?
if [ $RC -ne 0 ]; then echo "*** ERROR: bcftools merge RC: $RC."; exit 1; fi
echo '    File is indexed.'
conda deactivate
echo 'Files are merged.'

#-------------------------------------------------------------------------------

echo 'Filtering missing data ...'
source activate bcftools
bcftools view --exclude 'FMT/GT="mis"' --output-type v --output $OUTPUT_DIR/$OUTPUT_VCF_FILE $WMD_VCF_FILE
RC=$?
if [ $RC -ne 0 ]; then echo "*** ERROR: bcftools view RC: $RC."; exit 1; fi
echo '    File is indexed.'
conda deactivate
echo 'Mising data are filtered.'

#-------------------------------------------------------------------------------

exit 0

#-------------------------------------------------------------------------------
