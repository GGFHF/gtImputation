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
VCF_FILE_0=$DATA_DIR/$FILE_NAME-samples-filtered2.vcf
VCF_FILE_1=$OUTPUT_DIR/$FILE_NAME-1.vcf
VCF_FILE_1_WMD=$OUTPUT_DIR/$FILE_NAME-1-wmd.vcf
SAMPLES_FILE=$DATA_DIR/$FILE_NAME-samples-filtered2-IDs.txt
DB_FILE=$OUTPUT_DIR/$FILE_NAME.db

PATH=$NGSHELPERDIR:$MINIDONDA3_BIN:$PATH

MDP=0.10
MPIWMD=10

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

function sort_vcf_file
{
    echo "$SEP"
    echo 'Sorting VCF file ...'
    source activate bcftools
    /usr/bin/time \
        bcftools sort --output-type v --output-file $VCF_FILE_1 $VCF_FILE_0
    RC=$?
    if [ $RC -ne 0 ]; then manage_error bcftools-sort $RC; fi
    echo 'The file is sorted.'
    conda deactivate
}

#-------------------------------------------------------------------------------

function load_vcf_data
{
    echo "$SEP"
    echo 'Loading VCF file 1 data in the database ...'
    /usr/bin/time \
        load-vcf-data.py \
            --db=$DB_FILE \
            --vcf=$VCF_FILE_1 \
            --samples=$SAMPLES_FILE \
            --sp1_id=AL \
            --sp2_id=NONE \
            --hyb_id=NONE \
            --new_mdi=. \
            --imd_id=99 \
            --trans=NONE \
            --verbose=N \
            --trace=N \
            --tvi=NONE
    RC=$?
    if [ $RC -ne 0 ]; then manage_error load-vcf-data.py $RC; fi
    echo 'The file is sorted.'
    conda deactivate
}

#-------------------------------------------------------------------------------

function simulate_missing_data
{
    echo "$SEP"
    echo 'Simulating missing data in VCF file 1 (with intial data) ...'
    /usr/bin/time \
        simulate-md.py \
            --vcf=$VCF_FILE_1 \
            --method=RANDOM \
            --mdp=$MDP \
            --mpiwmd=$MPIWMD \
            --out=$VCF_FILE_1_WMD \
            --verbose=N \
            --trace=N \
            --tsi=NONE
    RC=$?
    if [ $RC -ne 0 ]; then manage_error simulate-md.py $RC; fi
    echo 'Missing data are simulated.'
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
sort_vcf_file
load_vcf_data
simulate_missing_data
end
