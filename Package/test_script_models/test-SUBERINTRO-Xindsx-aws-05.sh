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


PATH=$NGSHELPERDIR:$MINIDONDA3_BIN:$PATH

MDP=0.20
MPIWMD=20

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

function generate_vcf_files
{
    for I in "${SELINDS[@]}"; do
        VCF_FILE_0=$DATA_DIR/'test-SUBERINTRO-'$SPECIES'-samples-filtered2.vcf'
        FILE_NAME='test-SUBERINTRO-'$SPECIES'inds'$I
        VCF_FILE_1_INDSX=$OUTPUT_DIR/$FILE_NAME-1-indsx.vcf
        VCF_FILE_2_SORTED=$OUTPUT_DIR/$FILE_NAME-2-sorted.vcf
        VCF_FILE_3_FILTERED=$OUTPUT_DIR/$FILE_NAME-3-filtered.vcf
        VCF_FILE_4_WMD=$OUTPUT_DIR/$FILE_NAME-4-wmd.vcf
        SAMPLES_FILE_1=$OUTPUT_DIR/$FILE_NAME-samples-ids-1.txt
        SAMPLES_FILE_2=$OUTPUT_DIR/$FILE_NAME-samples-ids-2.txt
        DB_FILE=$OUTPUT_DIR/$FILE_NAME.db
        VCFTOOLS_STATS_PREFIX=$OUTPUT_DIR/$FILE_NAME-4-wmd-vcftools-stats
        BCFTOOLS_STATS_FILE=$OUTPUT_DIR/$FILE_NAME-4-wmd-bcftools-stats.txt
        BCFTOOLS_PLOT_DIR=$OUTPUT_DIR/$FILE_NAME-4-wmd-bcftools-stats-plot
        echo "$SEP"
        echo "Creating identification files ($I individuals) ..."
        /usr/bin/time \
            generate-id-files.py \
                --sp1_id=$SPECIES \
                --sp1_totinds=$TOTINDS \
                --sp1_selinds=$I \
                --sp2_id=NONE \
                --sp2_totinds=0 \
                --sp2_selinds=0 \
                --hyb_id=NONE \
                --hyb_totinds=0 \
                --hyb_selinds=0 \
                --outfile1=$SAMPLES_FILE_1 \
                --outfile2=$SAMPLES_FILE_2 \
                --verbose=Y \
                --trace=N
        RC=$?
        if [ $RC -ne 0 ]; then generate-id-files.py $RC; fi
        echo 'The file is created.'
        echo "$SEP"
        echo "Creating the VCF file ($I individuals) ..."
        source activate bcftools
        /usr/bin/time \
            bcftools view --samples-file $SAMPLES_FILE_1 --output-type v --output-file $VCF_FILE_1_INDSX $VCF_FILE_0
        RC=$?
        if [ $RC -ne 0 ]; then manage_error bcftools-sort $RC; fi
        echo 'The file is created.'
        conda deactivate
        echo "$SEP"
        echo "Sorting the VCF file ($I individuals) ..."
        source activate bcftools
        /usr/bin/time \
            bcftools sort --output-type v --output-file $VCF_FILE_2_SORTED $VCF_FILE_1_INDSX
        RC=$?
        if [ $RC -ne 0 ]; then manage_error bcftools-sort $RC; fi
        echo 'The file is sorted.'
        conda deactivate
        echo "$SEP"
        echo "Filtering variants with all monomorphic individual in the VCF file VCF file ($I individuals) ..."
        /usr/bin/time \
            filter-vcf.py \
                --threads=$THREADS \
                --action=MM \
                --vcf=$VCF_FILE_2_SORTED \
                --out=$VCF_FILE_3_FILTERED \
                --verbose=N \
                --trace=N \
                --tvi=NONE
        RC=$?
        if [ $RC -ne 0 ]; then manage_error bcftools-view $RC; fi
        echo 'The file is filtered.'
        echo "$SEP"
        echo "Loading data of the sorted VCF file ($I individuals) in the database ..."
        /usr/bin/time \
            load-vcf-data.py \
                --db=$DB_FILE \
                --vcf=$VCF_FILE_3_FILTERED \
                --samples=$SAMPLES_FILE_2 \
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
        echo "$SEP"
        echo "Simulating missing data in the sorted VCF file ($I individuals) ..."
        /usr/bin/time \
            simulate-md.py \
                --vcf=$VCF_FILE_3_FILTERED \
                --method=RANDOM \
                --mdp=$MDP \
                --mpiwmd=$MPIWMD \
                --out=$VCF_FILE_4_WMD \
                --verbose=N \
                --trace=N \
                --tsi=NONE
        RC=$?
        if [ $RC -ne 0 ]; then manage_error simulate-md.py $RC; fi
        echo 'Missing data are simulated.'
        echo "$SEP"
        echo "Calculating stats with VCFtools of the VCF file ($I individuals) ..."
        source activate vcftools
        /usr/bin/time \
            vcftools --vcf $VCF_FILE_4_WMD --site-pi --out $VCFTOOLS_STATS_PREFIX 
            vcftools --vcf $VCF_FILE_4_WMD --het --out $VCFTOOLS_STATS_PREFIX 
            vcftools --vcf $VCF_FILE_4_WMD --singletons --out $VCFTOOLS_STATS_PREFIX 
        RC=$?
        if [ $RC -ne 0 ]; then manage_error bcftools-stats $RC; fi
        echo 'Stats are calculated.'
        conda deactivate
        echo "$SEP"
        echo "Calculating stats with BCFtools of the VCF file ($I individuals) ..."
        source activate bcftools
        /usr/bin/time \
            bcftools stats --threads $THREADS $VCF_FILE_4_WMD > $BCFTOOLS_STATS_FILE
        RC=$?
        if [ $RC -ne 0 ]; then manage_error bcftools-stats $RC; fi
        /usr/bin/time \
            plot-vcfstats --prefix $BCFTOOLS_PLOT_DIR $BCFTOOLS_STATS_FILE
        RC=$?
        if [ $RC -ne 0 ]; then manage_error plot-vcfstats $RC; fi
        echo 'Stats are calculated.'
        conda deactivate
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
generate_vcf_files
end
