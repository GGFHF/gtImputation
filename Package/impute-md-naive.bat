@echo off

rem ----------------------------------------------------------------------------

rem This script runs the program impute-md-naive.py in a Windows environment.
rem
rem This software has been developed by:
rem
rem     GI Sistemas Naturales e Historia Forestal (formerly known as GI Genetica, Fisiologia e Historia Forestal)
rem     Dpto. Sistemas y Recursos Naturales
rem     ETSI Montes, Forestal y del Medio Natural
rem     Universidad Politecnica de Madrid
rem     https://github.com/ggfhf/
rem
rem Licence: GNU General Public Licence Version 3.

rem ----------------------------------------------------------------------------

rem Set environment

setlocal EnableDelayedExpansion

set ERROR=0

set PYTHON=python.exe
set PYTHON_OPTIONS=
set ARGV=
set PYTHONPATH=.

set APP_DIR=C:\Users\FMM\Documents\ProyectosVS\gtImputation\gtImputation

set INITIAL_DIR=%cd%
cd %APP_DIR%

rem ----------------------------------------------------------------------------

%PYTHON% %PYTHON_OPTIONS% impute-md-naive.py %* %ARGV%
if %ERRORLEVEL% neq 0 (set RC=%ERRORLEVEL% & set ERROR=1 & goto END)

rem ----------------------------------------------------------------------------

:END

cd %INITIAL_DIR%

if %ERROR% equ 0 (
    rem -- exit 0
)

if %ERROR% equ 1 (
    echo *** ERROR: The program ended with return code %RC%.
    rem -- pause
    rem -- exit %RC%
)

rem ----------------------------------------------------------------------------