
#!/bin/bash

#-------------------------------------------------------------------------------

# This script performs a test of the program  a vcf2tab.py 
# in a Linux environment.
#
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

# Control parameters

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

# Run the program vcf2tab.py

/usr/bin/time \
    ./vcf2tab.py \
        --vcf=$OUTPUT_DIR/variants-TabularFormatExample.vcf \
        --tab=$OUTPUT_DIR/variants-TabularFormatExample-new.txt \
        --mdc=0 \
        --verbose=Y \
        --trace=N \
        --tvi=NONE
if [ $? -ne 0 ]; then echo 'Script ended with errors.'; exit 1; fi

#-------------------------------------------------------------------------------

# End

cd $INITIAL_DIR

exit 0

#-------------------------------------------------------------------------------
