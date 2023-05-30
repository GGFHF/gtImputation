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

if [ -n "$*" ]; then echo 'This script has not parameters.'; exit 1; fi

#-------------------------------------------------------------------------------

SEP="#########################################"

MINIDONDA3_BIN=~/Miniconda3/bin
NGSHELPERDIR=$TRABAJO/ProyectosVScode/NGShelper
IMPUTATIONDIR=$TRABAJO/ProyectosVScode/Imputation

ALGORITM=SOM
DATASET_ID=AL
PROCESS_ID=B2
MDP=0.10
MPIWMD=10

DATA_DIR=$IMPUTATIONDIR/SUBERINTRO-data
OUTPUT_DIR=$TRABAJO/test-SUBERINTRO-$DATASET_ID-$PROCESS_ID

EXPERIMENT_ID=SUBERINTRO-$DATASET_ID-$PROCESS_ID
FILE_NAME=test-SUBERINTRO-$DATASET_ID
VCF_FILE_3_WMD=$OUTPUT_DIR/$FILE_NAME-3-wmd.vcf
SUMMARY_FILE=$OUTPUT_DIR/$FILE_NAME-summary.csv
DB_FILE=$OUTPUT_DIR/$FILE_NAME.db

DIM=(3 4 5)
SIGMA=(0.5 1.0 2.0)
LR=0.5
ITER=1000
MR2=(0.001 0.1 0.2)
SNPS=(5 10 15)
GIM=(MF CK)

HIGH_LD_SITES=SOM
NN=SOM
MAX_DIST=SOM

PATH=$NGSHELPERDIR:$MINIDONDA3_BIN:$PATH

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

function check_imputations
{
    echo "$SEP"
    echo 'Creating the file where the summaries of checkings are saved ...'
    echo 'file_name;algorithm;experiment_id;dataset_id;method;mdp;mpiwmd;dim;sigma;lr;iter;mr2;snps;gim;high_ld_sites;nn;max_dist;ok_genotypes_counter;ko_genotypes_counter;genotypes_withmd_counter;ok_imputed_genotypes_counter;ko_imputed_genotypes_counter;average_accuracy;error_rate;micro_precision;micro_recall;micro_fscore;macro_precision;macro_recall;macro_fscore;macro_precision_zde;macro_recall_zde' > $SUMMARY_FILE
    echo 'File is created.'

    for I in "${DIM[@]}"; do
        for J in "${SIGMA[@]}"; do
            for K in "${MR2[@]}"; do
                for L in "${SNPS[@]}"; do
                    for M in "${GIM[@]}"; do

                        echo "$SEP"
                        echo "VCF FILE: $VCF_FILE_3_WMD"
                        echo "SOM PARAMETERS - XDIM: $I - YDIM: $I - SIGMA: $J - LEARNING RATE: $LR - ITERATIONS NUMBER: $ITER"
                        echo "MINIMUM R^2: $K - SNPS NUMBER: $L - GENOTYPE IMPUTATION METHOD: $M"

                        RESULT_FILE_NAME=$OUTPUT_DIR/$FILE_NAME'-imputed-'$I'x'$I'-'$J'-'$K'-'$L'-'$M'.vcf'
                        MAP_FILE=$OUTPUT_DIR/$FILE_NAME'-imputed-'$I'x'$I'-'$J'-'$K'-'$L'-'$M'-map.csv'
                        CM_FILE=$OUTPUT_DIR/$FILE_NAME'-imputed-'$I'x'$I'-'$J'-'$K'-'$L'-'$M'-cm.csv'
                        EXPDATA=$ALGORITM';'$EXPERIMENT_ID';'$DATASET_ID';RANDOM;'$MDP';'$MPIWMD';'$I'x'$I';'$J';'$LR';'$ITER';'$K';'$L';'$M';'$HIGH_LD_SITES';'$NN';'$MAX_DIST

                        echo 'Checking imputations ...'
                        /usr/bin/time \
                            check-imputations.py \
                                --db=$DB_FILE \
                                --chvcffile=$RESULT_FILE_NAME \
                                --mdvcffile=$VCF_FILE_3_WMD \
                                --mapfile=$MAP_FILE \
                                --summfile=$SUMMARY_FILE \
                                --cmfile=$CM_FILE \
                                --expdata=$EXPDATA \
                                --verbose=N \
                                --trace=N \
                                --tsi=NONE
                        RC=$?
                        if [ $RC -ne 0 ]; then manage_error check-imputations.py $RC; fi
                        echo 'Imputations are checked.'

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
check_imputations
end
