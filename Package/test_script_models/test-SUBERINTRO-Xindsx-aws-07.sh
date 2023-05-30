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

SPECIES=AL
TOTINDS=98
SELINDS=(10 25 50 75 90)

DATA_DIR=$IMPUTATIONDIR/SUBERINTRO-data
OUTPUT_DIR=$IMPUTATIONDIR/'test-SUBERINTRO-'$SPECIES'indsx'

DIM=(4)
SIGMA=(1.0)
LR=0.5
ITER=1000
MR2=(0.1)
SNPS=(5)
GIM=(MF)

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
    for I in "${SELINDS[@]}"; do
        FILE_NAME='test-SUBERINTRO-'$SPECIES'inds'$I
        VCF_FILE_4_WMD=$OUTPUT_DIR/$FILE_NAME-4-wmd.vcf
        DB_FILE=$OUTPUT_DIR/$FILE_NAME.db
        echo "$SEP"
        echo "Calculating genotype data for $I individuas ..."
        /usr/bin/time \
            calculate-genotype-data.py \
                --threads=$THREADS \
                --db=$DB_FILE \
                --vcf=$VCF_FILE_4_WMD \
                --verbose=N \
                --trace=Y \
                --tvi=NONE
        RC=$?
        if [ $RC -ne 0 ]; then manage_error calculate-genotype-data.py $RC; fi
        echo 'Genotype data are calculated.'
    done
}

#-------------------------------------------------------------------------------

function impute_missing_data
{
    echo "$SEP"
    SUMMARY_FILE=$OUTPUT_DIR/'test-SUBERINTRO-'$SPECIES'indsx-summary.csv'
    echo 'Creating the file where the summaries of checkings are saved ...'
    echo 'file_name;ok_genotypes_counter;ko_genotypes_counter;genotypes_withmd_counter;ok_imputed_genotypes_counter;ko_imputed_genotypes_counter' > $SUMMARY_FILE
    echo 'File is created.'
    for I in "${SELINDS[@]}"; do
        FILE_NAME='test-SUBERINTRO-'$SPECIES'inds'$I
        VCF_FILE_4_WMD=$OUTPUT_DIR/$FILE_NAME-4-wmd.vcf
        DB_FILE=$OUTPUT_DIR/$FILE_NAME.db
        for J in "${DIM[@]}"; do
            for K in "${SIGMA[@]}"; do
                for L in "${MR2[@]}"; do
                    for M in "${SNPS[@]}"; do
                        for N in "${GIM[@]}"; do
                            echo "$SEP"
                            echo "VCF FILE: $VCF_FILE_4_WMD"
                            echo "SOM PARAMETERS - XDIM: $J - YDIM: $J - SIGMA: $L - LEARNING RATE: $LR - ITERATIONS NUMBER: $ITER"
                            echo "MINIMUM R^2: $L - SNPS NUMBER: $M - GENOTYPE IMPUTATION METHOD: $N"
                            RESULT_FILE_NAME=$OUTPUT_DIR/$FILE_NAME'-imputed-'$J'x'$J'-'$K'-'$L'-'$M'-'$N'.vcf'
                            MAP_FILE=$OUTPUT_DIR/$FILE_NAME'-imputed-'$J'x'$J'-'$K'-'$L'-'$M'-'$N'-map.csv'
                            echo 'Imputing missing data ...'
                            /usr/bin/time \
                                impute-md-som.py \
                                    --threads=$THREADS \
                                    --db=$DB_FILE \
                                    --vcf=$VCF_FILE_4_WMD \
                                    --out=$RESULT_FILE_NAME \
                                    --xdim=$J \
                                    --ydim=$J \
                                    --sigma=$K \
                                    --ilrate=$LR \
                                    --iter=$ITER \
                                    --mr2=$L \
                                    --snps=$M \
                                    --gim=$N \
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
                                    --mdvcffile=$VCF_FILE_4_WMD \
                                    --mapfile=$MAP_FILE \
                                    --summfile=$SUMMARY_FILE \
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
