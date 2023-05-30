#!/bin/bash

#-------------------------------------------------------------------------------

ERROR=0

export PATH=/home/fmm/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH
PYTHON=python3
PYTHON_OPTIONS=
ARGV=
PYTHONPATH=.
APP_DIR=/mnt/c/Users/FMM/Documents/ProyectosVS/gtImputation/gtImputation

INITIAL_DIR=$PWD
cd $APP_DIR

#-------------------------------------------------------------------------------

$PYTHON $PYTHON_OPTIONS ./gtImputation.py $* $ARGV
RC=$?
if [ $RC -ne 0 ]; then echo "ERROR: gtImputation.py ended with $RC."; ERROR=1;  fi

#-------------------------------------------------------------------------------

cd $INITIAL_DIR

exit $ERROR

#-------------------------------------------------------------------------------
