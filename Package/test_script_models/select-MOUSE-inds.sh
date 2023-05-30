#!/bin/bash

#-------------------------------------------------------------------------------

INDS=98inds
DATA_DIR=/home/fmm/Documents/Trabajo/MOUSE-data
INPUT_VCF_PATH=$DATA_DIR/reference.vcf
OUTPUT_VCF_PATH=$DATA_DIR/reference-$INDS.vcf
SAMPLES_PATH=$DATA_DIR/samples-$INDS-names.txt

#-------------------------------------------------------------------------------

source activate tabix
echo "Compressing $INPUT_VCF_PATH ..."
bgzip -c $INPUT_VCF_PATH > $INPUT_VCF_PATH.gz
RC=$?
if [ $RC -ne 0 ]; then echo "*** ERROR: bgzip ended with $RC.";  exit 1; fi
echo 'File is compressed.'
echo "Indexing $INPUT_VCF_PATH.gz ..."
parallel tabix -p vcf ::: $INPUT_VCF_PATH.gz
RC=$?
if [ $RC -ne 0 ]; then echo "*** ERROR: parallel tabix RC: $RC."; exit 1; fi
echo 'File is indexed.'
conda deactivate

#-------------------------------------------------------------------------------

echo 'Selecting individuals in VCF file ...'
source activate bcftools
bcftools view --force-samples --samples-file $SAMPLES_PATH --output-type v --output $OUTPUT_VCF_PATH $INPUT_VCF_PATH.gz
RC=$?
if [ $RC -ne 0 ]; then echo "*** ERROR: bcftools view RC: $RC."; exit 1; fi
echo '    File is indexed.'
conda deactivate
echo 'Individual are selected.'

#-------------------------------------------------------------------------------

exit 0

#-------------------------------------------------------------------------------
