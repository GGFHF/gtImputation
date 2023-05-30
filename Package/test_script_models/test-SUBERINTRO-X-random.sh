#!/bin/bash

#-------------------------------------------------------------------------------

# This software has been developed by:
#
#    GI Sistemas Naturales e Historia Forestal (formerly known as GI Genetica, Fisiologia e Historia Forestal)
#    Dpto. Sistemas y Recursos Naturales
#    ETSI Montes, Forestal y del Medio Natural
#    Universidad Politecnica de Madrid
#    https://github.com/ggfhf/
#
# Licence: GNU General Public Licence Version 3.

#-------------------------------------------------------------------------------

if [ -n "$*" ]; then echo 'This script does not have parameters'; exit 1; fi

#-------------------------------------------------------------------------------

SEP="#########################################"

DATASET_ID=AL

ALGORITHM=RANDOM
PROCESS_NAME=random

MDP=$ALGORITHM
MPIWMD=$ALGORITHM
DIM=$ALGORITHM
SIGMA=$ALGORITHM
LR=$ALGORITHM
ITER=$ALGORITHM
MR2=$ALGORITHM
SNPS=$ALGORITHM
GIM=$ALGORITHM
S=$ALGORITHM
N=$ALGORITHM
D=$ALGORITHM

NGSHELPER_DIR=$TRABAJO/ProyectosVScode/NGShelper
OUTPUT_DIR=$TRABAJO/test-SUBERINTRO-$DATASET_ID-$PROCESS_NAME
SUMMARY_FILE=$OUTPUT_DIR/test-SUBERINTRO-$DATASET_ID-summary-$PROCESS_NAME.csv

if [ ! -d "$OUTPUT_DIR" ]; then mkdir --parents $OUTPUT_DIR; fi

cd $NGSHELPER_DIR

#-------------------------------------------------------------------------------

PROCESS_ID=(B C D E F G H I J)

echo "$SEP"
echo 'Creating the file where the summaries of checkings are saved ...'
echo 'file_name;algorithm;experiment_id;dataset_id;method;mdp;mpiwmd;dim;sigma;lr;iter;mr2;snps;gim;high_ld_sites;nn;max_dist;ok_genotypes_counter;ko_genotypes_counter;genotypes_withmd_counter;ok_imputed_genotypes_counter;ko_imputed_genotypes_counter;average_accuracy;error_rate;micro_precision;micro_recall;micro_fscore;macro_precision;macro_recall;macro_fscore;macro_precision_zde;macro_recall_zde' > $SUMMARY_FILE
echo 'File is created.'

for I in "${PROCESS_ID[@]}"; do

    EXPERIMENT_ID=SUBERINTRO-$DATASET_ID-$I
    ROOT_NAME=test-$EXPERIMENT_ID
    DATA_DIR=$TRABAJO/$ROOT_NAME

    MDVCFFILE=$DATA_DIR/$ROOT_NAME-3-wmd.vcf 
    CHVCFFILE=$OUTPUT_DIR/$ROOT_NAME-imputed-$PROCESS_NAME.vcf

    echo "$SEP"
    echo "Imputing DATASET_ID: $DATA_DIR - PROCESS_ID: $I ..."
    /usr/bin/time \
        ./impute-md-random.py \
            --threads=4 \
            --vcf=$MDVCFFILE \
            --out=$CHVCFFILE \
            --verbose=N \
            --trace=N \
            --tvi=NONE
    if [ $? -ne 0 ]; then echo 'Script ended with errors.'; exit 1; fi
    echo 'Imputations is done.'

    DB_FILE=$DATA_DIR/$ROOT_NAME.db
    MAP_FILE=$OUTPUT_DIR/$ROOT_NAME-imputed-$PROCESS_NAME-map.csv
    CM_FILE=$OUTPUT_DIR/$ROOT_NAME-imputed-$PROCESS_NAME-cm.csv
    EXPDATA=$ALGORITHM';'$EXPERIMENT_ID';'$DATASET_ID';RANDOM;'$MDP';'$MPIWMD';'$DIM';'$SIGMA';'$LR';'$ITER';'$MR2';'$SNPS';'$GIM';'$S';'$N';'$D

    echo "$SEP"
    echo "VCF FILE: $CHVCFFILE"
    echo 'Checking imputations ...'
    /usr/bin/time \
        ./check-imputations.py \
            --db=$DB_FILE \
            --chvcffile=$CHVCFFILE \
            --mdvcffile=$MDVCFFILE \
            --mapfile=$MAP_FILE \
            --summfile=$SUMMARY_FILE \
            --cmfile=$CM_FILE \
            --expdata=$EXPDATA \
            --verbose=N \
            --trace=N \
            --tsi=NONE
    if [ $? -ne 0 ]; then echo 'Script ended with errors.'; exit 1; fi
    echo 'Imputations are checked.'

done

#-------------------------------------------------------------------------------

# End

exit 0

#-------------------------------------------------------------------------------
