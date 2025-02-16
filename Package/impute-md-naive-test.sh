#!/bin/bash

#-------------------------------------------------------------------------------

# This script performs a test of the program  a impute-md-naive.py 
# in a Linux environment.
#
# This software has been developed by:
#
#    GI en Desarrollo de Especies y Comunidades Leñosas (WooSp)
#    Dpto. Sistemas y Recursos Naturales
#    ETSI Montes, Forestal y del Medio Natural
#    Universidad Politecnica de Madrid
#    https://github.com/ggfhf/
#
# Licence: GNU General Public Licence Version 3.

#-------------------------------------------------------------------------------

if [ -n "$*" ]; then echo 'This script does not have parameters'; exit 1; fi

#-------------------------------------------------------------------------------

# Set environment

APP_DIR=$TRABAJO/ProyectosVScode/gtImputation
DATA_DIR=$TRABAJO/ProyectosVScode/NGShelper/data
OUTPUT_DIR=$TRABAJO/ProyectosVScode/NGShelper/output

if [ ! -d "$OUTPUT_DIR" ]; then mkdir --parents $OUTPUT_DIR; fi

INITIAL_DIR=$(pwd)
cd $APP_DIR

#-------------------------------------------------------------------------------

# Run the program impute-md-naive.py

/usr/bin/time \
    ./impute-md-naive.py \
        --threads=4 \
        --input_vcf=$DATA_DIR/variants-nonko.vcf \
        --output_vcf=$OUTPUT_DIR/variants-nonko-imputed.vcf \
        --impdata=$OUTPUT_DIR/imputation_data.csv \
        --verbose=Y \
        --trace=N \
        --tvi=NONE
if [ $? -ne 0 ]; then echo 'Script ended with errors.'; cd $INITIAL_DIR; exit 1; fi

#-------------------------------------------------------------------------------

# End

cd $INITIAL_DIR

exit 0

#-------------------------------------------------------------------------------
