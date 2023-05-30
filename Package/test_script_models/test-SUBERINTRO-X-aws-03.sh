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

MINIDONDA3_BIN=/ngscloud2/apps/Miniconda3/bin
NGSHELPERDIR=/ngscloud2/apps/NGShelper
IMPUTATIONDIR=/ngscloud2/results/imputations

DATA_DIR=$IMPUTATIONDIR/SUBERINTRO-data
OUTPUT_DIR=$IMPUTATIONDIR/test-SUBERINTRO-AL

FILE_NAME=test-SUBERINTRO-AL
VCF_FILE_1_WMD=$OUTPUT_DIR/$FILE_NAME-1-wmd.vcf
SUMMARY_FILE_1=$OUTPUT_DIR/$FILE_NAME-1-summary.csv
DB_FILE=$OUTPUT_DIR/$FILE_NAME.db

DIM=(3 4 5)
SIGMA=(0.5 1.0 2.0)
LR=0.5
ITER=1000
MR2=(0.001 0.1 0.2)
SNPS=(5 10 15)
GIM=(MF CK)

PATH=$NGSHELPERDIR:$MINIDONDA3_BIN:$PATH

THREADS=8

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
            --db=$DB_FILE \
            --vcf=$VCF_FILE_1_WMD \
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
    echo 'file_name;ok_genotypes_counter;ko_genotypes_counter;genotypes_withmd_counter;ok_imputed_genotypes_counter;ko_imputed_genotypes_counter' > $SUMMARY_FILE_1
    echo 'File is created.'
    for I in "${DIM[@]}"; do
        for J in "${SIGMA[@]}"; do
            for K in "${MR2[@]}"; do
                for L in "${SNPS[@]}"; do
                    for M in "${GIM[@]}"; do
                        echo "$SEP"
                        echo "VCF FILE: $VCF_FILE_1_WMD"
                        echo "SOM PARAMETERS - XDIM: $I - YDIM: $I - SIGMA: $J - LEARNING RATE: $LR - ITERATIONS NUMBER: $ITER"
                        echo "MINIMUM R^2: $K - SNPS NUMBER: $L - GENOTYPE IMPUTATION METHOD: $M"
                        RESULT_FILE_NAME=$OUTPUT_DIR/$FILE_NAME'-imputed-'$I'x'$I'-'$J'-'$K'-'$L'-'$M'.vcf'
                        MAP_FILE=$OUTPUT_DIR/$FILE_NAME'-imputed-'$I'x'$I'-'$J'-'$K'-'$L'-'$M'-map.csv'
                        echo 'Imputing missing data ...'
                        /usr/bin/time \
                            impute-md-som.py \
                                --threads=$THREADS \
                                --db=$DB_FILE \
                                --vcf=$VCF_FILE_1_WMD \
                                --out=$RESULT_FILE_NAME \
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
                        echo 'Checking imputations ...'
                        /usr/bin/time \
                            check-imputations.py \
                                --db=$DB_FILE \
                                --chvcffile=$RESULT_FILE_NAME \
                                --mdvcffile=$VCF_FILE_1_WMD \
                                --mapfile=$MAP_FILE \
                                --summfile=$SUMMARY_FILE_1 \
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
