#!/bin/bash

#-------------------------------------------------------------------------------

# This software has been developed by:
#
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
NGSHELPER_DIR=~/Documents/NGShelper
DATA_DIR=~/gtImputation-master/test-vcf-files

DATASET_ID=mr-QS
PROCESS_ID=B
MDP=0.10
MPIWMD=10

EXPERIMENT_ID=$DATASET_ID-$PROCESS_ID
ROOT_NAME=test-$EXPERIMENT_ID

DATA_DIR=$TRABAJO/SUBERINTRO-data
OUTPUT_DIR=$TRABAJO/$ROOT_NAME

VCF_PATH_0=$DATA_DIR/$DATASET_ID.vcf
SAMPLES_PATH=$DATA_DIR/$DATASET_ID-samples.txt

VCF_PATH_1_SORTED=$OUTPUT_DIR/$ROOT_NAME-1-sorted.vcf
VCF_PATH_2_FILTERED=$OUTPUT_DIR/$ROOT_NAME-2-filtered.vcf
VCF_PATH_3_WMD=$OUTPUT_DIR/$ROOT_NAME-3-wmd.vcf
DB_PATH=$OUTPUT_DIR/$ROOT_NAME.db
VCFTOOLS_STATS_PREFIX=$OUTPUT_DIR/$ROOT_NAME-3-wmd-vcftools-stats
BCFTOOLS_STATS_PATH=$OUTPUT_DIR/$ROOT_NAME-3-wmd-bcftools-stats.txt
BCFTOOLS_PLOT_DIR=$OUTPUT_DIR/$ROOT_NAME-3-wmd-bcftools-stats-plot

PATH=$NGSHELPER_DIR:$MINIDONDA3_BIN:$PATH

THREADS=4

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

function compress_vcf_file
{
    echo "$SEP"
    echo 'Compressing VCF file ...'
    source activate tabix
    bgzip --keep --stdout $VCF_PATH_0 > $VCF_PATH_0.gz
    RC=$?
    if [ $RC -ne 0 ]; then manage_error bgzip $RC; fi
    echo 'The dile is compressed.'
    conda deactivate
}

#-------------------------------------------------------------------------------

function index_vcf_file
{
    echo "$SEP"
    echo 'Indexing VCF file ...'
    source activate tabix
    /usr/bin/time \
        tabix --preset vcf $VCF_PATH_0.gz
    RC=$?
    if [ $RC -ne 0 ]; then manage_error parallel-tabix $RC; fi
    echo 'The File is indexed.'
    conda deactivate
}

#-------------------------------------------------------------------------------

function sort_vcf_file
{
    echo "$SEP"
    echo 'Sorting VCF file ...'
    source activate bcftools
    /usr/bin/time \
        bcftools sort --output-type v --output-file $VCF_PATH_1_SORTED $VCF_PATH_0.gz
    RC=$?
    if [ $RC -ne 0 ]; then manage_error bcftools-sort $RC; fi
    echo 'The file is sorted.'
    conda deactivate
}

#-------------------------------------------------------------------------------

function filter_vcf_file
{
    echo "$SEP"
    echo 'Filtering VCF file ...'
        /usr/bin/time \
            filter-vcf.py \
                --threads=$THREADS \
                --action=MM \
                --vcf=$VCF_PATH_1_SORTED \
                --out=$VCF_PATH_2_FILTERED \
                --verbose=N \
                --trace=N \
                --tvi=NONE
        RC=$?
        if [ $RC -ne 0 ]; then manage_error filter-vcf.py $RC; fi
        echo 'The file is filtered.'
}

#-------------------------------------------------------------------------------

function load_vcf_data
{
    echo "$SEP"
    echo 'Loading filtered VCF file data in the database ...'
    /usr/bin/time \
        load-vcf-data.py \
            --db=$DB_PATH \
            --vcf=$VCF_PATH_2_FILTERED \
            --samples=$SAMPLES_PATH \
            --sp1_id=EFS \
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
    echo 'Simulating missing data in filtered VCF file ...'
    /usr/bin/time \
        simulate-md.py \
            --vcf=$VCF_PATH_2_FILTERED \
            --method=RANDOM \
            --mdp=$MDP \
            --mpiwmd=$MPIWMD \
            --out=$VCF_PATH_3_WMD \
            --verbose=N \
            --trace=N \
            --tsi=NONE
    RC=$?
    if [ $RC -ne 0 ]; then manage_error simulate-md.py $RC; fi
    echo 'Missing data are simulated.'
}

#-------------------------------------------------------------------------------

function calculate_vcftools_stats
{
    echo "$SEP"
    echo "Calculating stats with VCFtools of the filtered VCF file ($I individuals) ..."
    source activate vcftools
    /usr/bin/time \
        vcftools --vcf $VCF_PATH_3_WMD --site-pi --out $VCFTOOLS_STATS_PREFIX 
        vcftools --vcf $VCF_PATH_3_WMD --het --out $VCFTOOLS_STATS_PREFIX 
        vcftools --vcf $VCF_PATH_3_WMD --singletons --out $VCFTOOLS_STATS_PREFIX 
    RC=$?
    if [ $RC -ne 0 ]; then manage_error bcftools-stats $RC; fi
    echo 'Stats are calculated.'
}

#-------------------------------------------------------------------------------

function calculate_bcftools_stats
{
    echo "$SEP"
    echo "Calculating stats with BCFtools of the VCF file ($I individuals) ..."
    source activate bcftools
    /usr/bin/time \
        bcftools stats --threads $THREADS $VCF_PATH_3_WMD > $BCFTOOLS_STATS_PATH
    RC=$?
    if [ $RC -ne 0 ]; then manage_error bcftools-stats $RC; fi
    /usr/bin/time \
        plot-vcfstats --prefix $BCFTOOLS_PLOT_DIR $BCFTOOLS_STATS_PATH
    RC=$?
    if [ $RC -ne 0 ]; then manage_error plot-vcfstats $RC; fi
    echo 'Stats are calculated.'
    conda deactivate
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
compress_vcf_file
index_vcf_file
sort_vcf_file
filter_vcf_file
load_vcf_data
simulate_missing_data
calculate_vcftools_stats
calculate_bcftools_stats
end
