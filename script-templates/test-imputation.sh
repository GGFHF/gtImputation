#!/bin/bash

#-------------------------------------------------------------------------------

# This software has been developed by:
#
#    GI en Desarrollo de Especies y Comunidades Leñosas (WooSp)
#    Dpto. Sistemas y Recursos Naturales
#    ETSI Montes, Forestal y del Medio Natural
#    Universidad Politecnica de Madrid
#    https://github.com/ggfhf/
#
# Licence: GNU General Public Licence Version 3.

# This script uses the following software: NGShelper and Miniforge3. Installation instructions:
#
#    - NGShelper: see https://github.com/GGFHF/NGShelper/
#
#    - Miniforge3: see https://github.com/conda-forge/miniforge

#-------------------------------------------------------------------------------

if [ -n "$*" ]; then echo 'This script has not parameters.'; exit 1; fi

#-------------------------------------------------------------------------------

SEP="#########################################"

MINIDONDA3_BIN=~/Miniforge3/bin
NGSHELPER_DIR=~/Documents/NGShelper-master/Package

DATASET_ID=mr-QS
PROCESS_ID=B
MDP=0.10
MPIWMD=10

EXPERIMENT_ID=$DATASET_ID-$PROCESS_ID
ROOT_NAME=test-$EXPERIMENT_ID
DATA_DIR=~/Documents/gtImputation-main/test-vcf-files
OUTPUT_DIR=~/Documents/$ROOT_NAME

VCF_PATH_3_WMD=$OUTPUT_DIR/$ROOT_NAME-3-wmd.vcf
DB_PATH=$OUTPUT_DIR/$ROOT_NAME.db
SUMMARY_PATH=$OUTPUT_DIR/$ROOT_NAME-summary.csv

ALGORITHM=SOM
DIM=(3 4 5)
SIGMA=(0.5 1.0 2.0)
LR=0.5
ITER=1000
MR2=(0.001 0.1 0.2)
SNPS=(5 10 15)
GIM=(MF CK)
HIGH_LD_SITES=$ALGORITHM
NN=$ALGORITHM
MAX_DIST=$ALGORITHM

PATH=$NGSHELPER_DIR:$MINIDONDA3_BIN:$PATH

THREADS=1

if [ `ulimit -n` -lt 1024 ]; then ulimit -n 1024; fi

#-------------------------------------------------------------------------------

function init
{
    INIT_DATETIME=`date --utc +%s`
    FORMATTED_INIT_DATETIME=`date --date="@$INIT_DATETIME" "+%Y-%m-%d %H:%M:%S"`
    echo "$SEP"
    echo "Script started at $FORMATTED_INIT_DATETIME+00:00."
}

#-------------------------------------------------------------------------------

function calculate_genotype_data
{
    echo "$SEP"
    echo 'Calculating genotype data ...'
    /usr/bin/time \
        calculate-genotype-data.py \
            --threads=$THREADS \
            --db=$DB_PATH \
            --vcf=$VCF_PATH_3_WMD \
            --verbose=N \
            --trace=Y \
            --tvi=NONE
    RC=$?
    if [ $RC -ne 0 ]; then manage_error calculate-genotype-data.py $RC; fi
    echo 'Missing data are simulated.'
}

#-------------------------------------------------------------------------------

function impute_missing_data
{
    echo "$SEP"
    echo 'Creating the file where the summaries of checkings are saved ...'
    echo 'file_name;algorithm;experiment_id;dataset_id;method;mdp;mpiwmd;dim;sigma;lr;iter;mr2;snps;gim;high_ld_sites;nn;max_dist;ok_genotypes_counter;ko_genotypes_counter;genotypes_withmd_counter;ok_imputed_genotypes_counter;ko_imputed_genotypes_counter;average_accuracy;error_rate;micro_precision;micro_recall;micro_fscore;macro_precision;macro_recall;macro_fscore;macro_precision_zde;macro_recall_zde' > $SUMMARY_PATH
    echo 'File is created.'

    for I in "${DIM[@]}"; do
        for J in "${SIGMA[@]}"; do
            for K in "${MR2[@]}"; do
                for L in "${SNPS[@]}"; do
                    for M in "${GIM[@]}"; do

                        echo "$SEP"
                        echo "VCF FILE: $VCF_PATH_3_WMD"
                        echo "SOM PARAMETERS - XDIM: $I - YDIM: $I - SIGMA: $J - LEARNING RATE: $LR - ITERATIONS NUMBER: $ITER"
                        echo "MINIMUM R^2: $K - SNPS NUMBER: $L - GENOTYPE IMPUTATION METHOD: $M"

                        IMPUTED_VCF_PATH=$OUTPUT_DIR/$ROOT_NAME'-imputed-'$I'x'$I'-'$J'-'$K'-'$L'-'$M'.vcf'

                        echo 'Imputing missing data ...'
                        /usr/bin/time \
                            impute-md-som.py \
                                --threads=$THREADS \
                                --db=$DB_PATH \
                                --vcf=$VCF_PATH_3_WMD \
                                --out=$IMPUTED_VCF_PATH \
                                --xdim=$I \
                                --ydim=$I \
                                --sigma=$J \
                                --ilrate=$LR \
                                --iter=$ITER \
                                --mr2=$K \
                                --snps=$L \
                                --gim=$M \
                                --verbose=N \
                                --trace=N \
                                --tvi=NONE
                        RC=$?
                        if [ $RC -ne 0 ]; then manage_error impute-md-som.py $RC; fi
                        echo 'Missing data are imputated.'

                        MAP_PATH=$OUTPUT_DIR/$ROOT_NAME'-imputed-'$I'x'$I'-'$J'-'$K'-'$L'-'$M'-map.csv'
                        CM_PATH=$OUTPUT_DIR/$ROOT_NAME'-imputed-'$I'x'$I'-'$J'-'$K'-'$L'-'$M'-cm.csv'
                        EXPDATA=$ALGORITHM';'$EXPERIMENT_ID';'$DATASET_ID';RANDOM;'$MDP';'$MPIWMD';'$I'x'$I';'$J';'$LR';'$ITER';'$K';'$L';'$M';'$HIGH_LD_SITES';'$NN';'$MAX_DIST

                        echo 'Checking imputations ...'
                        /usr/bin/time \
                            check-imputations.py \
                                --db=$DB_PATH \
                                --chvcffile=$IMPUTED_VCF_PATH \
                                --mdvcffile=$VCF_PATH_3_WMD \
                                --mapfile=$MAP_PATH \
                                --summfile=$SUMMARY_PATH \
                                --cmfile=$CM_PATH \
                                --expdata=$EXPDATA \
                                --verbose=N \
                                --trace=N \
                                --tsi=NONE
                        RC=$?
                        if [ $RC -ne 0 ]; then manage_error check-imputations.py $RC; fi
                        echo 'Missing data are simulated.'

                    done
                done
            done
        done
    done
}

#-------------------------------------------------------------------------------

function end
{
    END_DATETIME=`date --utc +%s`
    FORMATTED_END_DATETIME=`date --date="@$END_DATETIME" "+%Y-%m-%d %H:%M:%S"`
    calculate_duration
    echo "$SEP"
    echo "Script ended OK at $FORMATTED_END_DATETIME+00:00 with a run duration of $DURATION s ($FORMATTED_DURATION)."
    echo "$SEP"
    exit 0
}

#-------------------------------------------------------------------------------

function manage_error
{
    END_DATETIME=`date --utc +%s`
    FORMATTED_END_DATETIME=`date --date="@$END_DATETIME" "+%Y-%m-%d %H:%M:%S"`
    calculate_duration
    echo "$SEP"
    echo "ERROR: $1 returned error $2"
    echo "Script ended WRONG at $FORMATTED_END_DATETIME+00:00 with a run duration of $DURATION s ($FORMATTED_DURATION)."
    echo "$SEP"
    exit 3
}

#-------------------------------------------------------------------------------

function calculate_duration
{
    DURATION=`expr $END_DATETIME - $INIT_DATETIME`
    HH=`expr $DURATION / 3600`
    MM=`expr $DURATION % 3600 / 60`
    SS=`expr $DURATION % 60`
    FORMATTED_DURATION=`printf "%03d:%02d:%02d\n" $HH $MM $SS`
}

#-------------------------------------------------------------------------------

init
calculate_genotype_data
impute_missing_data
end
