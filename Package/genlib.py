#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=multiple-statements
# pylint: disable=too-many-lines

#-------------------------------------------------------------------------------

'''
This source defines the general functions and classes used in Genotype Imputation (gtImputation).

This software has been developed by:

    GI en Desarrollo de Especies y Comunidades Leñosas (WooSp)
    Dpto. Sistemas y Recursos Naturales
    ETSI Montes, Forestal y del Medio Natural
    Universidad Politecnica de Madrid
    https://github.com/ggfhf/

Licence: GNU General Public Licence Version 3.
'''

#-------------------------------------------------------------------------------

import collections
import configparser
import datetime
import os
import re
import subprocess
import sys

#-------------------------------------------------------------------------------

def get_app_code():
    '''
    Get the application code.
    '''

    return 'gtimputation'

#-------------------------------------------------------------------------------

def get_app_long_name():
    '''
    Get the application long name.
    '''

    return 'gtImputation (Genotype Imputation)'

#-------------------------------------------------------------------------------

def get_app_short_name():
    '''
    Get the application short name.
    '''

    return 'gtImputation'

#-------------------------------------------------------------------------------

def get_app_version():
    '''
    Get the application version.
    '''

    return '0.20'

#-------------------------------------------------------------------------------

def get_app_config_dir():
    '''
    Get the application configuration directory.
    '''

    return './config'

#-------------------------------------------------------------------------------

def get_app_config_file():
    '''
    Get the path of the aplication config file.
    '''

    return f'{get_app_config_dir()}/{get_app_code()}-config.txt'

#-------------------------------------------------------------------------------

def get_app_manual_file():
    '''
    Get the file path of application manual.
    '''

    return f'./{get_app_short_name()}-manual.pdf'

#-------------------------------------------------------------------------------

def get_app_image_file():
    '''
    Get the file path of application image.
    '''

    return f'./image-{get_app_short_name()}.png'

#-------------------------------------------------------------------------------

def get_app_background_image_file():
    '''
    Get the file path of the background image.
    '''

    return './arbutus-unedo-768x580.jpg'

#-------------------------------------------------------------------------------

def check_os():
    '''
    Check the operating system.
    '''

    if not sys.platform.startswith('linux') and not sys.platform.startswith('darwin') and not sys.platform.startswith('win32'):
        raise ProgramException('', 'S001', sys.platform)

#-------------------------------------------------------------------------------

def get_default_font_size():
    '''
    Get the default font depending on the Operating System.
    '''

    default_font_and_size = 0
    if sys.platform.startswith('linux'):
        default_font_and_size = ('Verdana', 10)
    elif sys.platform.startswith('darwin'):
        default_font_and_size = ('Verdana', 10)
    elif sys.platform.startswith('win32'):
        default_font_and_size = ('DejaVu 10', 10)

    return default_font_and_size

#-------------------------------------------------------------------------------

def get_gtdb_dir():
    '''
    Get the directory where genotype database data are saved.
    '''

    return f'{get_app_short_name()}-databases'

#-------------------------------------------------------------------------------

def get_result_dir():
    '''
    Get the result directory where results datasets are saved.
    '''

    return f'{get_app_short_name()}-results'

#-------------------------------------------------------------------------------

def get_result_installation_subdir():
    '''
    Get the result subdirectory where installation process results are saved.
    '''

    return 'installation'

#-------------------------------------------------------------------------------

def get_result_gtdb_subdir():
    '''
    Get the result subdirectory where process results related to the genotype database are saved.
    '''

    return 'gtdb'

#-------------------------------------------------------------------------------

def get_result_imputation_subdir():
    '''
    Get the result subdirectory where process results related to the imputation are saved.
    '''

    return 'imputation'

#-------------------------------------------------------------------------------

def get_yml_dir():
    '''
    Get the yml directory where gtImputation environment installation is.
    '''

    return 'yml'

#-------------------------------------------------------------------------------

def get_gtimputation_yml_file():
    '''
    Get the yml file of the gtImputation environment installation.
    '''

    return 'gtimputation.yml'

#-------------------------------------------------------------------------------

def get_log_dir():
    '''
    Get the temporal directory.
    '''

    return './logs'

#-------------------------------------------------------------------------------

def get_run_log_file():
    '''
    Get the log file name of a process run.
    '''

    return 'log.txt'

#-------------------------------------------------------------------------------

def get_temp_dir():
    '''
    Get the temporal directory.
    '''

    return './temp'

#-------------------------------------------------------------------------------

def get_config_dict(config_file):
    '''
    Get a dictionary with the options retrieved from a configuration file.
    '''

    # initialize the configuration dictionary
    option_dict = {}

    try:

        # create class to parse the configuration files
        config = configparser.ConfigParser()

        # read the configuration file
        config.read(config_file)

        # build the dictionary
        for section in config.sections():
            # get the keys dictionary
            keys_dict = option_dict.get(section, {})
            # for each key in the section
            for key in config[section]:
                # get the value of the key
                value = config.get(section, key, fallback='')
                # add a new enter in the keys dictionary
                keys_dict[key] = get_option_value(value)
            # update the section with its keys dictionary
            option_dict[section] = keys_dict

    except Exception as e:
        raise ProgramException(e, 'F005', config_file) from e

    # return the configuration dictionary
    return option_dict

#-------------------------------------------------------------------------------

def get_option_value(option):
    '''
    Remove comments and spaces from an option retrieve from a configuration file.
    '''

    # remove comments
    position = option.find('#')
    if position == -1:
        value = option
    else:
        value = option[:position]

    # remove spaces
    value = value.strip()

    # return the value
    return value

#-------------------------------------------------------------------------------

def windows_path_2_wsl_path(path):
    '''
    Change a Windows format path to a WSL format path.
    '''

    # change the format path
    new_path = path.replace('\\', '/')
    new_path = f'/mnt/{new_path[0:1].lower()}{new_path[2:]}'

    # return the path
    return new_path

#-------------------------------------------------------------------------------

def wsl_path_2_windows_path(path):
    '''
    Change a WSL format path to a Windows format path.
    '''

    # change the format path
    new_path = f'{path[5:6].upper()}:{path[6:]}'
    new_path = new_path.replace('/', '\\')

    # return the path
    return new_path

#-------------------------------------------------------------------------------

def get_wsl_envvar(envvar):
    '''
    Get the value of a varible environment from WSL.
    '''

    # initialize the environment variable value
    envvar_value = get_na()

    # build the command
    command = f'wsl bash -c "echo ${envvar}"'

    # run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    for line in iter(process.stdout.readline, b''):
        envvar_value = line.decode('utf-8').replace('\n' ,'')
        break
    process.wait()

    # return the environment variable value
    return envvar_value

#-------------------------------------------------------------------------------

def get_current_run_dir(result_dir, group, process):
    '''
    Get the run directory of a process.
    '''

    # set the run identificacion
    now = datetime.datetime.now()
    date = datetime.datetime.strftime(now, '%y%m%d')
    time = datetime.datetime.strftime(now, '%H%M%S')
    run_id = f'{process}-{date}-{time}'

    # set the current run directory
    current_run_dir = f'{result_dir}/{group}/{run_id}'

    # return the run directory
    return current_run_dir

#-------------------------------------------------------------------------------

def get_status_dir(current_run_dir):
    '''
    Get the status directory of a process.
    '''

    return f'{current_run_dir}/status'

#-------------------------------------------------------------------------------

def get_status_ok(current_run_dir):
    '''
    Get the OK status file.
    '''

    return f'{current_run_dir}/status/script.ok'

#-------------------------------------------------------------------------------

def get_status_wrong(current_run_dir):
    '''
    Get the WRONG status file.
    '''

    return f'{current_run_dir}/status/script.wrong'

#-------------------------------------------------------------------------------

def get_submission_log_file(function_name):
    '''
    Get the log file name of a process submission.
    '''

    # set the log file name
    now = datetime.datetime.now()
    date = datetime.datetime.strftime(now, '%y%m%d')
    time = datetime.datetime.strftime(now, '%H%M%S')
    log_file_name = f'{get_log_dir()}/{function_name}-{date}-{time}.txt'

    # return the log file name
    return log_file_name

   #---------------

def build_starter(directory, starter_name, script_name, current_run_dir):
    '''
    Build the script to start a process script.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # set the starter path
    starter_path = f'{directory}/{starter_name}'

    # write the starter
    try:
        with open(starter_path, mode='w', encoding='iso-8859-1', newline='\n') as file_id:
            file_id.write( '#!/bin/bash\n')
            file_id.write( '#-------------------------------------------------------------------------------\n')
            if sys.platform.startswith('linux') or sys.platform.startswith('win32'):
                file_id.write(f'{current_run_dir}/{script_name} &>>{current_run_dir}/{get_run_log_file()} &\n')
            elif sys.platform.startswith('darwin'):
                file_id.write(f'{current_run_dir}/{script_name} &>{current_run_dir}/{get_run_log_file()} &\n')
    except Exception as e:
        error_list.append(f'*** EXCEPTION: "{e}".')
        error_list.append(f'*** ERROR: The file {starter_path} is not created.')
        OK = False

    # return the control variable and error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def list_log_files_command(local_process_id):
    '''
    Get the command to list log files depending on the Operating System.
    '''

    # get log dir
    log_dir = get_log_dir()

    # assign the command
    command = ''
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        if local_process_id == 'all':
            command = f'ls {log_dir}/*.txt'
        else:
            command = f'ls {log_dir}/{local_process_id}-*.txt'
    elif sys.platform.startswith('win32'):
        log_dir = log_dir.replace('/', '\\')
        if local_process_id == 'all':
            command = f'dir /B {log_dir}{os.sep}*.txt'
        else:
            command = f'dir /B {log_dir}{os.sep}{local_process_id}-*.txt'

    # return the command
    return command

#-------------------------------------------------------------------------------

def check_startswith(literal, text_list, case_sensitive=False):
    '''
    Check if a literal starts with a text in a list.
    '''

    # initialize the control variable
    OK = False

    # initialize the working list
    new_list = []

    # if the codification is not case sensitive, convert the code and code list to uppercase
    if not case_sensitive:
        try:
            literal = literal.upper()
        except Exception:
            pass
        try:
            new_list = [x.upper() for x in text_list]
        except Exception:
            pass
    else:
        new_list = text_list

    # check if the literal starts with a text in the list
    for text in new_list:
        if literal.startswith(text):
            OK = True
            break

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def check_code(literal, code_list, case_sensitive=False):
    '''
    Check if a literal is in a code list.
    '''

    # initialize the working list
    w_list = []

    # if the codification is not case sensitive, convert the code and code list to uppercase
    if not case_sensitive:
        try:
            literal = literal.upper()
        except Exception:
            pass
        try:
            w_list = [x.upper() for x in code_list]
        except Exception:
            pass
    else:
        w_list = code_list

    # check if the code is in the code list
    OK = literal in w_list

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def check_int(literal, minimum=(-sys.maxsize - 1), maximum=sys.maxsize):
    '''
    Check if a numeric or string literal is an integer number.
    '''

    # initialize the control variable
    OK = True

    # check the number
    try:
        int(literal)
        int(minimum)
        int(maximum)
    except Exception:
        OK = False
    else:
        if int(literal) < int(minimum) or int(literal) > int(maximum):
            OK = False

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def check_float(literal, minimum=float(-sys.maxsize - 1), maximum=float(sys.maxsize), mne=0.0, mxe=0.0):
    '''
    Check if a numeric or string literal is a float number.
    '''

    # initialize the control variable
    OK = True

    # check the number
    try:
        float(literal)
        float(minimum)
        float(maximum)
        float(mne)
        float(mxe)
    except Exception:
        OK = False
    else:
        if float(literal) < (float(minimum) + float(mne)) or float(literal) > (float(maximum) - float(mxe)):
            OK = False

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def split_literal_to_integer_list(literal):
    '''
    Split a text literal with values are separated by comma in a integer list.
    '''

    # initialize the text list and interger list
    text_list = []
    integer_list = []

    # split the text literal in a text list
    text_list = split_literal_to_text_list(literal)

    # convert each item from text to integer
    for text in text_list:
        try:
            integer_list.append(int(text))
        except Exception:
            integer_list = []
            break

    # return the integer values list
    return integer_list

#-------------------------------------------------------------------------------

def split_literal_to_float_list(literal):
    '''
    Split a text literal with values are separated by comma in a float list.
    '''

    # initialize the text list and the float list
    text_list = []
    float_list = []

    # split the text literal in a text list
    text_list = split_literal_to_text_list(literal)

    # convert each value from text to float
    for text in text_list:
        try:
            float_list.append(float(text))
        except Exception:
            float_list = []
            break

    # return the float values list
    return float_list

#-------------------------------------------------------------------------------

def split_literal_to_text_list(literal):
    '''
    Split a text literal with values are separated by comma in a text list.
    '''

    # initialize the new text list
    new_text_list = []

    # split the text literal in a text list
    text_list = literal.split(',')

    # remove the leading and trailing whitespaces in each value
    # and add text item to the new text list
    for item in text_list:
        new_text_list.append(item.strip())

    # return the text list
    return new_text_list

#-------------------------------------------------------------------------------

def is_valid_path(path, operating_system=sys.platform):
    '''
    Check if a path is a valid path.
    '''

    # initialize control variable
    OK = False

    # check if the path is valid
    if operating_system.startswith('linux') or operating_system.startswith('darwin'):
        # -- OK = re.match(r'^(/.+)(/.+)*/?$', path)
        OK = True
    elif operating_system.startswith('win32'):
        OK = True

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def is_absolute_path(path, operating_system=sys.platform):
    '''
    Check if a path is a absolute path.
    '''

    # initialize control variable
    OK = False

    # check if the path is absolute depending on the operating system
    if operating_system.startswith('linux') or operating_system.startswith('darwin'):
        if path != '':
            # -- OK = is_path_valid(path) and path[0] == '/'
            OK = True
    elif operating_system.startswith('win32'):
        OK = True

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def run_command(command, log, is_script):
    '''
    Run a Bash shell command and redirect stdout and stderr to log.
    '''

    # prepare the command to be execuete on WSL if necessary
    if sys.platform.startswith('win32'):
        if is_script:
            command = command.replace('&', '')
            command = f'wsl bash -c "nohup {command} &>/dev/null"'
        else:
            command = f'wsl bash -c "{command}"'

    # run the command
    current_subprocess = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    for line in iter(current_subprocess.stdout.readline, b''):
        line = re.sub(b'[^\x00-\x7F]+', b' ', line) # replace non-ASCII caracters by one blank space
        line = line.decode('iso-8859-1')
        log.write(line)
    rc = current_subprocess.wait()

    # return the return code of the command run
    return rc

#-------------------------------------------------------------------------------

def read_vcf_file(vcf_file_id, sample_number, check_sample_number=True):
    '''
    Read a VCF file record.
    '''

    # initialize the data dictionary
    data_dict = {}

    # initialize the key
    key = None

    # read next record
    record = vcf_file_id.readline()

    # metadata record
    if record != '' and record.startswith('##'):

        pass

    # column description record
    elif record != '' and record.startswith('#CHROM'):

        record_data_list = []
        start = 0
        for end in [i for i, chr in enumerate(record) if chr == '\t']:
            record_data_list.append(record[start:end].strip())
            start = end + 1
        record_data_list.append(record[start:].strip('\n').strip())

        data_dict = {'record_data_list': record_data_list}

    # variant record
    elif record != '' and not record.startswith('##') and not record.startswith('#CHROM'):

        # initialize the record data list
        record_data_list = []

        # build the record data list
        start = 0
        for end in [i for i, chr in enumerate(record) if chr == '\t']:
            record_data_list.append(record[start:end].strip())
            start = end + 1
        record_data_list.append(record[start:].strip('\n').strip())

        # check the length of the record data list
        if check_sample_number and len(record_data_list) - 9 != sample_number:
            print(f'sample_number: {sample_number}')
            print(f'len(record_data_list) - 9: {len(record_data_list) - 9}')
            raise ProgramException('', 'L001', record_data_list[0], record_data_list[1])

        # set data
        data_chrom = record_data_list[0]
        data_pos = record_data_list[1]
        data_id = record_data_list[2]
        data_ref = record_data_list[3]
        data_alt = record_data_list[4]
        data_qual = record_data_list[5]
        data_filter = record_data_list[6]
        data_info = record_data_list[7]
        data_format = record_data_list[8]
        data_sample_list = []
        for i in range(len(record_data_list) - 9):
            data_sample_list.append(record_data_list[i + 9])

        # set the key
        key = f'{data_chrom}-{int(data_pos):09d}'

        # get the record data dictionary
        data_dict = {'chrom': data_chrom, 'pos': data_pos, 'id': data_id, 'ref': data_ref, 'alt': data_alt, 'qual': data_qual, 'filter': data_filter, 'info': data_info, 'format': data_format, 'sample_list': data_sample_list}

    # there is not any record
    else:

        # set the key
        key = bytes.fromhex('7E').decode('utf-8')

    # return the record, key and data dictionary
    return record, key, data_dict

#-------------------------------------------------------------------------------

def get_miniforge3_code():
    '''
    Get the Miniforge3 code used to identify its processes.
    '''

    return 'miniforge3'

#-------------------------------------------------------------------------------

def get_miniforge3_name():
    '''
    Get the Miniforge3 name used to title.
    '''

    return 'Miniforge3'

#-------------------------------------------------------------------------------

def get_miniforge3_url():
    '''
    Get the Miniforge3 URL.
    '''

    # assign the Miniforge3 URL
    miniforge3_url = ''
    if sys.platform.startswith('linux') or sys.platform.startswith('win32'):
        miniforge3_url = 'https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh'
    elif sys.platform.startswith('darwin'):
        miniforge3_url = 'https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh'

    # return the Miniforge3 URL
    return miniforge3_url

#-------------------------------------------------------------------------------

def get_miniforge3_dir():
    '''
    Get the directory where Miniforge3 is installed.
    '''

    return 'Miniforge3'

#-------------------------------------------------------------------------------

def get_miniforge3_dir_in_wsl():
    '''
    Get the directory where Miniforge3 is installed on WSL environment.
    '''

    return '$HOME/Miniforge3'

#-------------------------------------------------------------------------------

def get_miniforge3_current_dir():
    '''
    Get the current directory where Miniforge3 is installed.
    '''

    # get the path of the directory path of the current conda environment
    environment_path = os.getenv('CONDA_PREFIX')
    envs_pos = environment_path.find('/envs')

    # get the miniforge current directory
    miniforge3_current_dir = ''
    if envs_pos == -1:
        miniforge3_current_dir = environment_path
    else:
        miniforge3_current_dir = environment_path[:envs_pos]

    # return the miniforge current directory
    return miniforge3_current_dir

#-------------------------------------------------------------------------------

def get_gtimputation_env_code():
    '''
    Get the Miniforge3 environment code where the Python packages used by gtImputation are
    installed.
    '''

    return 'gtimputation'

#-------------------------------------------------------------------------------

def get_gtimputation_env_name():
    '''
    Get the Miniforge3 environment name where the Python packages used by gtImputation are
    installed.
    '''

    return 'gtImputation environment'

#-------------------------------------------------------------------------------

def get_bioconda_code():
    '''
    Get the Bioconda code used to identify its processes.
    '''

    return 'bioconda'

#-------------------------------------------------------------------------------

def get_bioconda_name():
    '''
    Get the Bioconda name used to title.
    '''

    return 'Bioconda'

#-------------------------------------------------------------------------------

def get_naive_imputation_code():
    '''
    Get the code of the naive imputation used to identify its processes.
    '''

    return 'naive'

#-------------------------------------------------------------------------------

def get_naive_imputation_name():
    '''
    Get the name of the naive imputation used to title its processess.
    '''

    return 'Naive imputation process'

#-------------------------------------------------------------------------------

def get_gtdb_building_code():
    '''
    Get the code of the genotype database building used to identify its processes.
    '''

    return 'gtdb'

#-------------------------------------------------------------------------------

def get_gtdb_building_name():
    '''
    Get the name of the genotype database building used to title its processess.
    '''

    return 'Genotype database building'

#-------------------------------------------------------------------------------

def get_som_imputation_code():
    '''
    Get the code of the naive imputation used to identify its processes.
    '''

    return 'som'

#-------------------------------------------------------------------------------

def get_som_imputation_name():
    '''
    Get the name of the naive imputation used to title its processess.
    '''

    return 'SOM imputation process'

#-------------------------------------------------------------------------------

def get_submitting_dict():
    '''
    Get the process submitting dictionary.
    '''

    # build the submitting process dictionary
    submitting_dict = {}
    submitting_dict['install_miniforge3']= {'text': f'{get_miniforge3_name()} installation'}
    submitting_dict['install_gtimputation_env']= {'text': f'{get_gtimputation_env_name()} installation'}
    submitting_dict['install_bioconda_package_list']= {'text': 'Bioconda package list installation'}
    submitting_dict['run_naive_imputation']= {'text': get_naive_imputation_name()}
    submitting_dict['run_gtdb_building']= {'text': get_gtdb_building_name()}
    submitting_dict['run_som_imputation']= {'text': get_som_imputation_name()}

    # return the submitting process dictionary
    return submitting_dict

#-------------------------------------------------------------------------------

def get_submitting_id(submitting_text):
    '''
    Get the process submitting identification from the submission process text.
    '''

    # initialize the control variable
    submitting_id_found = None

    # get the dictionary of the submitting processes
    submitting_dict = get_submitting_dict()

    # search the submitting process identification
    for key, value in submitting_dict.items():
        if value['text'] == submitting_text:
            submitting_id_found = key
            break

    # return the submitting process identification
    return submitting_id_found

#-------------------------------------------------------------------------------

def get_process_dict():
    '''
    Get the process dictionary.
    '''

    # build the process dictionary
    process_dict = {}
    process_dict[get_miniforge3_code()]= {'name': get_miniforge3_name(), 'process_type': get_result_installation_subdir()}
    process_dict[get_gtimputation_env_code()]= {'name': get_gtimputation_env_name(), 'process_type': get_result_installation_subdir()}
    process_dict[get_naive_imputation_code()]= {'name': get_naive_imputation_name(), 'process_type': get_result_imputation_subdir()}
    process_dict[get_gtdb_building_code()]= {'name': get_gtdb_building_name(), 'process_type': get_result_imputation_subdir()}
    process_dict[get_som_imputation_code()]= {'name': get_som_imputation_name(), 'process_type': get_result_imputation_subdir()}

    # return the process dictionary
    return process_dict

#-------------------------------------------------------------------------------

def get_process_id(process_name):
    '''
    Get the process identification from the process name.
    '''

    # initialize the process identication
    process_id_found = None

    # get the process ddictionary
    process_dict = get_process_dict()

    # search the process identification
    for key, value in process_dict.items():
        if value['name'] == process_name:
            process_id_found = key
            break

    # return the process identication
    return process_id_found

#-------------------------------------------------------------------------------

def get_process_name_list(process_type):
    '''
    Get the code list of installation processes.
    '''

    # initialize the process name list
    process_name_list = []

    # get the process ddictionary
    process_dict = get_process_dict()

    # search the process names corresponding to the process type
    for _, value in process_dict.items():
        if value['process_type'] == process_type:
            process_name_list.append(value['name'])

    # return the process name list sorted
    return sorted(process_name_list)

#-------------------------------------------------------------------------------

def get_md_symbol():
    '''
    Get the "missing_data" symbol.
    '''

    return '.'

#-------------------------------------------------------------------------------

def get_r_estimator_code_list():
    '''
    Get the code list of "r_estimator".
    '''

    return ['ru', 'rw']

#-------------------------------------------------------------------------------

def get_r_estimator_code_list_text():
    '''
    Get the code list of "r_estimator" as text.
    '''

    return 'ru (the unweighted average estimator) or rw (the weighted estimator)'

#-------------------------------------------------------------------------------

def get_genotype_imputation_method_code_list():
    '''
    Get the code list of "genotype_imputation_method".
    '''

    return ['MF', 'CK']

#-------------------------------------------------------------------------------

def get_genotype_imputation_method_code_list_text():
    '''
    Get the code list of "genotype_ imputation_method" as text.
    '''

    return 'MF (most frequent genotype) or CK (genotype of the closest kinship individual)'

#-------------------------------------------------------------------------------

def get_genotype_imputation_method_text_list():
    '''
    Get the code list of "genotype_ imputation_method" as text.
    '''

    return ['Most frequent genotype', 'Closest kinship ind. gt.']

#-------------------------------------------------------------------------------

def get_format_type_code_list():
    '''
    Get the code list of "genotype_imputation_method".
    '''

    return ['tabular', 'VCF']

#-------------------------------------------------------------------------------

def get_verbose_code_list():
    '''
    Get the code list of "verbose".
    '''

    return ['Y', 'N']

#-------------------------------------------------------------------------------

def get_verbose_code_list_text():
    '''
    Get the code list of "verbose" as text.
    '''

    return 'Y (yes) or N (no)'

#-------------------------------------------------------------------------------

def get_trace_code_list():
    '''
    Get the code list of "trace".
    '''

    return ['Y', 'N']

#-------------------------------------------------------------------------------

def get_trace_code_list_text():
    '''
    Get the code list of "trace" as text.
    '''

    return 'Y (yes) or N (no)'

#-------------------------------------------------------------------------------

def get_na():
    '''
    Get the characters to represent not available.
    '''

    return 'N/A'

#-------------------------------------------------------------------------------

def get_separator():
    '''
    Get the separation line between process steps.
    '''

    return '**************************************************'

#-------------------------------------------------------------------------------

class Const():
    '''
    This class has attributes with values will be used as constants.
    '''

    #---------------

    DEFAULT_R_ESTIMATOR = 'ru'
    DEFAULT_GENOTYPE_IMPUTATION_METHOD = 'MF'
    DEFAULT_TRACE = 'N'
    DEFAULT_VERBOSE = 'N'

   #---------------

#-------------------------------------------------------------------------------

class Message():
    '''
    This class controls the informative messages printed on the console.
    '''

    #---------------

    verbose_status = False
    trace_status = False

    #---------------

    @staticmethod
    def set_verbose_status(status):
        '''
        Set the verbose status.
        '''

        Message.verbose_status = status

    #---------------

    @staticmethod
    def set_trace_status(status):
        '''
        Set the trace status.
        '''

        Message.trace_status = status

    #---------------

    @staticmethod
    def print(message_type, message_text):
        '''
        Print a message depending to its type.
        '''

        if message_type == 'info':
            print(message_text, file=sys.stdout)
            sys.stdout.flush()
        elif message_type == 'verbose' and Message.verbose_status:
            sys.stdout.write(message_text)
            sys.stdout.flush()
        elif message_type == 'trace' and Message.trace_status:
            print(message_text, file=sys.stdout)
            sys.stdout.flush()
        elif message_type == 'error':
            print(message_text, file=sys.stderr)
            sys.stderr.flush()

    #---------------

#-------------------------------------------------------------------------------

class ProgramException(Exception):
    '''
    This class controls various exceptions that can occur in the execution of the application.
    '''

   #---------------

    def __init__(self, e, code_exception, param1='', param2='', param3=''):
        '''Initialize the object to manage a passed exception.'''

        # call the init method of the parent class
        super().__init__()

        # print the message of the exception
        if e != '':
            Message.print('error', f'*** EXCEPTION: "{e}"')

        # manage the code of exception
        if code_exception == 'B001':
            Message.print('error', f'*** ERROR {code_exception}: The database {param1} can not be connected.')
        elif code_exception == 'B002':
            Message.print('error', f'*** ERROR {code_exception} in sentence:')
            Message.print('error', f'{param1}')
        elif code_exception == 'F001':
            Message.print('error', f'*** ERROR {code_exception}: The file {param1} can not be opened.')
        elif code_exception == 'F002':
            Message.print('error', f'*** ERROR {code_exception}: The GZ compressed file {param1} can not be opened.')
        elif code_exception == 'F003':
            Message.print('error', f'*** ERROR {code_exception}: The file {param1} can not be written.')
        elif code_exception == 'F004':
            Message.print('error', f'*** ERROR {code_exception}: The GZ compressed file {param1} can not be written.')
        elif code_exception == 'F005':
            Message.print('error', f'*** ERROR {code_exception}: The file {param1} has a wrong format.')
        elif code_exception == 'P001':
            Message.print('error', f'*** ERROR {code_exception}: The program has parameters with invalid values.')
        elif code_exception == 'L001':
            Message.print('error', f'*** ERROR {code_exception}: There are wrong species identifications.')
        elif code_exception == 'L002':
            Message.print('error', f'*** ERROR {code_exception}: The field {param1} is not found in the variant with identification {param2} and position {param3}.')
        elif code_exception == 'L003':
            Message.print('error', f'*** ERROR {code_exception}: The field {param1} has an invalid value in the variant with identification {param2} and position {param3}.')
        elif code_exception == 'L004':
            Message.print('error', f'*** ERROR {code_exception}: The field {param1} is not found in the variant with identification {param2} and position {param3}.')
        elif code_exception == 'L005':
            Message.print('error', f'*** ERROR {code_exception}: The field {param1} has an invalid value in the variant with identification {param2} and position {param3}.')
        elif code_exception == 'L006':
            Message.print('error', f'\n*** ERROR {code_exception}: The variant {param1} has more than one alternative allele.')
        elif code_exception == 'L007':
            Message.print('error', f'\n*** ERROR {code_exception}: The genotype number does not correspond to variant number in the sample {param1}.')
        elif code_exception == 'S001':
            Message.print('error', f'*** ERROR {code_exception}: The {param1} OS is not supported.')
        elif code_exception == 'S002':
            Message.print('error', f'*** ERROR {code_exception}: The library {param1} is not installed. Please, review how to install {param1} in the manual.')
        else:
            Message.print('error', f'*** ERROR {code_exception}: The exception is not managed.')

        sys.exit(1)

   #---------------

#-------------------------------------------------------------------------------

class NestedDefaultDict(collections.defaultdict):
    '''
    This class is used to create nested dictionaries.
    '''

    def __init__(self, *args, **kwargs):
        super(NestedDefaultDict, self).__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))

#-------------------------------------------------------------------------------

class BreakAllLoops(Exception):
    '''
    This class is used to break out of nested loops.
    '''

    pass    #pylint: disable=unnecessary-pass

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print(f'This source contains general functions and classes used in {get_app_long_name()}.')
    sys.exit(0)

#-------------------------------------------------------------------------------
