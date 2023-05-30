#!/bin/bash

#-------------------------------------------------------------------------------

# This script performs a test of the program  a calculate-genotype-data.py 
# in a Linux environment.
#
# This software has been developed by:
#
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

/usr/bin/time \
    ./calculate-genotype-data.py \
        --threads=8 \
        --gtdb=$DATA_DIR/ddRADseqTools2.db \
        --vcf=$DATA_DIR/variants-nonko.vcf \
        --verbose=Y \
        --trace=N \
        --tvi=NONE
if [ $? -ne 0 ]; then echo 'Script ended with errors.'; cd $INITIAL_DIR; exit 1; fi

#-------------------------------------------------------------------------------

# End

cd $INITIAL_DIR

exit 0

#-------------------------------------------------------------------------------
