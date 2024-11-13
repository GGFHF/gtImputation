#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=multiple-statements
# pylint: disable=too-many-lines

#-------------------------------------------------------------------------------

'''
This file contains the classes related to the imputation processes of
Genotype Imputation (gtImputation).

This software has been developed by:

    GI en Desarrollo de Especies y Comunidades Leñosas (WooSp)
    Dpto. Sistemas y Recursos Naturales
    ETSI Montes, Forestal y del Medio Natural
    Universidad Politecnica de Madrid
    https://github.com/ggfhf/

Licence: GNU General Public Licence Version 3.
'''

#-------------------------------------------------------------------------------

import os
import sys

from PyQt5.QtCore import Qt                      # pylint: disable=no-name-in-module
from PyQt5.QtGui import QColor                   # pylint: disable=no-name-in-module
from PyQt5.QtGui import QCursor                  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QFontMetrics             # pylint: disable=no-name-in-module
from PyQt5.QtGui import QGuiApplication          # pylint: disable=no-name-in-module
from PyQt5.QtGui import QIcon                    # pylint: disable=no-name-in-module
from PyQt5.QtGui import QPixmap                  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QAbstractItemView    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QApplication         # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QComboBox            # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QFileDialog          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGroupBox            # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QHeaderView          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel               # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLineEdit            # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMessageBox          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QPushButton          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QSizePolicy          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QTableWidget         # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QTableWidgetItem     # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QVBoxLayout          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget              # pylint: disable=no-name-in-module

import genlib
import dialogs

#-------------------------------------------------------------------------------

class FormNaiveImputation(QWidget):
    '''
    Class used to perform a naive imputation.
    '''

    #---------------

    def __init__(self, parent):
        '''
        Create a class instance.
        '''

        # save parameters in instance variables
        self.parent = parent

        # call the init method of the parent class
        super().__init__()

        # set the dimensions window
        self.window_height = self.parent.WINDOW_HEIGHT - 100
        self.window_width = self.parent.WINDOW_WIDTH - 50

        # set the head and title
        self.head = genlib.get_naive_imputation_name()
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

        # get the dictionary of application configuration
        self.app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())

        # build the graphic user interface of the window
        self.build_gui()

        # load initial data in inputs
        self.initialize_inputs()

        # check the content of inputs
        self.check_inputs()

        # show the window
        self.show()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        # set the width and height of the window
        self.setFixedSize(self.window_width, self.window_height)

        # move the window at center
        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        # get font metrics information
        fontmetrics = QFontMetrics(QApplication.font())

        # create and configure "label_head"
        label_head = QLabel(self.head, alignment=Qt.AlignCenter)
        label_head.setStyleSheet('font: bold 14px; color: black; background-color: lightGray; max-height: 30px')

        # create and configure "label_threads"
        label_threads = QLabel()
        label_threads.setText('Threads')
        label_threads.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_threads"
        self.lineedit_threads = QLineEdit()
        self.lineedit_threads.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_threads.editingFinished.connect(self.check_inputs)
        self.lineedit_threads.setReadOnly(True)

        # create and configure "label_file_format"
        label_file_format = QLabel()
        label_file_format.setText('File format')
        label_file_format.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "combobox_file_format"
        self.combobox_file_format = QComboBox()
        self.combobox_file_format.setFixedWidth(fontmetrics.width('9'*10))
        self.combobox_file_format.currentIndexChanged.connect(self.check_inputs)

        # create and configure "label_mdc"
        label_mdc = QLabel()
        label_mdc.setText('MD char in tabular format')
        label_mdc.setFixedWidth(fontmetrics.width('9'*20))

        # create and configure "lineedit_mdc"
        self.lineedit_mdc  = QLineEdit()
        self.lineedit_mdc.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_mdc.editingFinished.connect(self.check_inputs)

        # create and configure "label_file_path"
        label_file_path = QLabel()
        label_file_path.setText('File path')
        label_file_path.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_file_path"
        self.lineedit_file_path  = QLineEdit()
        self.lineedit_file_path.editingFinished.connect(self.check_inputs)

        # create and configure "pushbutton_search"
        pushbutton_search = QPushButton('Search ...')
        pushbutton_search.setToolTip('Search and select the file with missing data in genotypes.')
        pushbutton_search.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_search.clicked.connect(self.pushbutton_search_clicked)

        # create and configure "label_empty"
        label_empty = QLabel()
        label_empty.setFixedWidth(fontmetrics.width('9'*3))

        # create and configure "gridlayout_data"
        gridlayout_data = QGridLayout()
        gridlayout_data.setRowMinimumHeight(0, 60)
        gridlayout_data.setRowMinimumHeight(1, 60)
        gridlayout_data.setRowMinimumHeight(2, 60)
        gridlayout_data.setColumnStretch(0,1)
        gridlayout_data.setColumnStretch(1,1)
        gridlayout_data.setColumnStretch(2,1)
        gridlayout_data.setColumnStretch(3,1)
        gridlayout_data.setColumnStretch(4,1)
        gridlayout_data.setColumnStretch(5,15)
        gridlayout_data.setColumnStretch(6,1)
        gridlayout_data.addWidget(label_threads, 0, 0)
        gridlayout_data.addWidget(self.lineedit_threads, 0, 1)
        gridlayout_data.addWidget(label_file_format, 1, 0)
        gridlayout_data.addWidget(self.combobox_file_format, 1, 1)
        gridlayout_data.addWidget(label_empty, 1, 2)
        gridlayout_data.addWidget(label_mdc, 1, 3)
        gridlayout_data.addWidget(self.lineedit_mdc, 1, 4)
        gridlayout_data.addWidget(label_file_path, 2, 0)
        gridlayout_data.addWidget(self.lineedit_file_path, 2, 1, 1, 5)
        gridlayout_data.addWidget(pushbutton_search, 2, 6)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        # create and configure "pushbutton_execute"
        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Execute the process of the naive imputation.')
        self.pushbutton_execute.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_execute.clicked.connect(self.pushbutton_execute_clicked)

        # create and configure "pushbutton_close"
        pushbutton_close = QPushButton('Close')
        pushbutton_close.setToolTip('Cancel the process of the naive imputation and close the window.')
        pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        # create and configure "gridlayout_buttons"
        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 15)
        gridlayout_buttons.setColumnStretch(1, 1)
        gridlayout_buttons.setColumnStretch(2, 1)
        gridlayout_buttons.addWidget(self.pushbutton_execute, 0, 1, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(pushbutton_close, 0, 2, alignment=Qt.AlignCenter)

        # create and configure "groupbox_buttons"
        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)

        # create and configure "gridlayout_central"
        gridlayout_central = QGridLayout()
        gridlayout_central.setRowStretch(0, 1)
        gridlayout_central.setRowStretch(1, 1)
        gridlayout_central.setRowStretch(2, 1)
        gridlayout_central.setRowStretch(3, 1)
        gridlayout_central.setRowStretch(4, 1)
        gridlayout_central.setColumnStretch(0, 0)
        gridlayout_central.setColumnStretch(1, 1)
        gridlayout_central.setColumnStretch(2, 0)
        gridlayout_central.addWidget(label_head, 0, 1)
        gridlayout_central.addWidget(QLabel(), 1, 1)
        gridlayout_central.addWidget(groupbox_data, 2, 1)
        gridlayout_central.addWidget(QLabel(), 3, 1)
        gridlayout_central.addWidget(groupbox_buttons, 4, 1)

        # create and configure "groupbox_central"
        groupbox_central = QGroupBox()
        groupbox_central.setLayout(gridlayout_central)

        # create and configure "vboxlayout"
        vboxlayout = QVBoxLayout(self)
        vboxlayout.addWidget(groupbox_central)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # set initial value in "lineedit_threads"
        self.lineedit_threads.setText('1')

        # populate data in "combobox_file_format"
        self.combobox_file_format_populate()
        self.combobox_file_format.setCurrentIndex(1)

        # set initial value in "lineedit_mdc"
        self.lineedit_mdc.setText('0')

        # set initial value in "lineedit_file_path"
        self.lineedit_file_path.setText('')

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # check "lineedit_threads" when the editing finished
        if not self.lineedit_threads_editing_finished():
            OK = False

        # check "combobox_file_format" when the index changed
        self.combobox_file_format_currentIndexChanged()

        # check "lineedit_mdc_editing" when the editing finished
        if not self.lineedit_mdc_editing_finished():
            OK = False

        # check "lineedit_file_path" when the editing finished
        if not self.lineedit_file_path_editing_finished():
            OK = False

        # check all inputs are OK
        if OK:
            self.parent.statusBar().showMessage('')
        else:
            self.parent.statusBar().showMessage('There are one or more inputs without data or with wrong values.')

        # enable "pushbutton_execute"
        if OK and self.lineedit_threads.text() != '' and self.combobox_file_format.currentText() != '' and self.lineedit_mdc.text() != '' and self.lineedit_file_path.text() != '':
            self.pushbutton_execute.setEnabled(True)
        else:
            self.pushbutton_execute.setEnabled(False)

        # return the control variable
        return OK

    #---------------

    def lineedit_threads_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_threads"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_threads" is empty
        if self.lineedit_threads.text() == '':
            OK = False
            self.lineedit_threads.setStyleSheet('background-color: white')

        # chek if "lineedit_threads" is an integer number between 1 and the CPUs number in the computer
        elif self.lineedit_threads.text() != '' and not genlib.check_int(self.lineedit_threads.text(), minimum=1, maximum=os.cpu_count()):
            OK = False
            self.lineedit_threads.setStyleSheet('background-color: red')
            text = f'The value of threads number has to be an integer number between 1 and {os.cpu_count()} (threads available in the computer).'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_threads.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def combobox_file_format_populate(self):
        '''
        Populate data in "combobox_file_format".
        '''

        # populate data in "combobox_file_format"
        self.combobox_file_format.addItems(genlib.get_format_type_code_list())

        # simultate "combobox_file_format" index has changed
        self.combobox_file_format_currentIndexChanged()

    #---------------

    def combobox_file_format_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_file_format" has been selected.
        '''

        pass

    #---------------

    def lineedit_mdc_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_mcd"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_mcd" is empty
        if self.lineedit_mdc.text() == '':
            OK = False

        # return the control variable
        return OK

    #---------------

    def lineedit_file_path_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_file_path"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_file_path" is empty
        if self.lineedit_file_path.text() == '':
            OK = False
            self.lineedit_file_path.setStyleSheet('background-color: white')

        # chek if "lineedit_file_path" is an integer number between 1 and the CPUs number in the computer
        elif self.lineedit_file_path.text() != '' and not os.path.isfile(self.lineedit_file_path.text()):
            OK = False
            self.lineedit_file_path.setStyleSheet('background-color: red')
            text = 'The file path has to be an existing file.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_file_path.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def pushbutton_search_clicked(self):
        '''
        Search and select a file with missing data.
        '''

        # get the file with missing data
        if self.combobox_file_format.currentText() == 'tabular':
            (file, _) = QFileDialog.getOpenFileName(self, f'{self.head} - Selection of the file', os.path.expanduser('~'), 'Text files (*.txt);;TSV files (*.tsv);;All files (*)')
        elif self.combobox_file_format.currentText() == 'VCF':
            (file, _) = QFileDialog.getOpenFileName(self, f'{self.head} - Selection of the file', os.path.expanduser('~'), 'VCF files (*.vcf);;All files (*)')
        self.lineedit_file_path.setText(file)

        # check the content of inputs
        self.check_inputs()

    #---------------

    def pushbutton_execute_clicked(self):
        '''
        Execute the process.
        '''

        # check the content of inputs
        OK = self.check_inputs()
        if not OK:
            text = 'Some input values are not OK.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        # confirm the process is executed
        if OK:
            text = 'The naive imputation process is going to be run.\n\nAre you sure to continue?'
            botton = QMessageBox.question(self, self.title, text, buttons=QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)
            if botton == QMessageBox.No:
                OK = False

        # execute the process
        if OK:
            threads = self.lineedit_threads.text()
            file_format = self.combobox_file_format.currentText()
            mdc = self.lineedit_mdc.text()
            file_path = self.lineedit_file_path.text()
            process = dialogs.DialogProcess(self, self.head, self.run_naive_imputation, threads, file_format, mdc, file_path)
            process.exec()

        # close the windows
        if OK:
            self.pushbutton_close_clicked()

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.parent.current_subwindow = None
        self.close()
        self.parent.set_background_image()

   #---------------

    def run_naive_imputation(self, process, threads, file_format, mdc, file_path):
        '''
        Run a naive imputation process.
        '''

        # initialize the control variable
        OK = True

        # warn that the log window does not have to be closed
        process.write('This process might take several minutes. Do not close this window, please wait!\n')

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # determine the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write('Determining the temporal directory ...\n')
            temp_dir = genlib.get_temp_dir()
            command = f'mkdir -p {temp_dir}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write(f'The directory path is {temp_dir}.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # determine the run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n'); process.show()
            process.write('Determining the run directory ...\n'); process.show()
            current_run_dir = genlib.get_current_run_dir(result_dir, genlib.get_result_imputation_subdir(), genlib.get_naive_imputation_code())
            command = f'mkdir -p {current_run_dir}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write(f'The directory path is {current_run_dir}.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False


        # build the naive imputation script in the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            script_name = f'{genlib.get_naive_imputation_code()}-process.sh'
            process.write(f'Building the script {script_name} ...\n')
            (OK, _) = self.build_naive_imputation_script(temp_dir, script_name, current_run_dir, threads, file_format, mdc, file_path)
            if OK:
                process.write('The file is built.\n')
            else:
                process.write('*** ERROR: The file could not be built.\n')

        # copy the naive imputation script to the current run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Copying the script {script_name} to the directory {current_run_dir} ...\n')
            command = f'cp {temp_dir}/{script_name} {current_run_dir}; [ $? -eq 0 ] &&  exit 0 || exit 1'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The file is copied.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')

        # set run permision to the imputation script
        if OK and not sys.platform.startswith('win32'):
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Setting on the run permision of {script_name} ...\n')
            command = f'chmod u+x {current_run_dir}/{script_name}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The run permision is set.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # build the starter script in the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            starter_name = f'{genlib.get_naive_imputation_code()}-process-starter.sh'
            process.write(f'Building the starter script {starter_name} ...\n')
            (OK, _) = genlib.build_starter(temp_dir, starter_name, script_name, current_run_dir)
            if OK:
                process.write('The file is built.\n')
            if not OK:
                process.write('***ERROR: The file could not be built.\n')

        # copy the starter script to the current run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Copying the starter {starter_name} to the directory {current_run_dir} ...\n')
            command = f'cp {temp_dir}/{starter_name} {current_run_dir}; [ $? -eq 0 ] &&  exit 0 || exit 1'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The file is copied.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')

        # set run permision to the starter script
        if OK and not sys.platform.startswith('win32'):
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Setting on the run permision of {starter_name} ...\n')
            command = f'chmod u+x {current_run_dir}/{starter_name}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The run permision is set.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # submit the starter
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Submitting the starter {starter_name} ...\n')
            command = f'{current_run_dir}/{starter_name} &'
            rc = genlib.run_command(command, process, is_script=True)
            if rc == 0:
                process.write('The script is submitted.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        process.write(f'{genlib.get_separator()}\n')
        process.write('You can close this window now.\n')

        # return the control variable
        return OK

   #---------------

    def build_naive_imputation_script(self, directory, script_name, current_run_dir, threads, file_format, mdc, file_path):
        '''
        Build the script to run the naive imputation process.
        '''

        # initialize the control variable and error list
        OK = True
        error_list = []

        # get items from dictionary of application configuration
        app_dir = self.app_config_dict['Environment parameters']['app_dir']
        miniconda3_bin_dir = self.app_config_dict['Environment parameters']['miniconda3_bin_dir']

        # set the parameters file
        params_file = f'{current_run_dir}/params.txt'

        # set the file path in WSL
        if sys.platform.startswith('win32'):
            file_path = genlib.windows_path_2_wsl_path(file_path)

        # set the file with missing data
        if file_format == 'tabular':
            vcf_wmd_file = f'{current_run_dir}/vcf_wmd.vcf'
        elif file_format == 'VCF':
            vcf_wmd_file = file_path

        # set the imputed VCF
        vcf_imputed_file = f'{current_run_dir}/imputed.vcf'

        # set the imputed file in tabular format
        tab_imputed_file = f'{current_run_dir}/imputed.tsv'

        # set the VCF with missing data
        imputation_data_file = f'{current_run_dir}/imputation_data.csv'

        # set the script path
        script_path = f'{directory}/{script_name}'

        # write the script
        try:
            with open(script_path, mode='w', encoding='iso-8859-1', newline='\n') as file_id:
                file_id.write( '#!/bin/bash\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'THREADS={threads}\n')
                file_id.write(f'FILE_FORMAT={file_format}\n')
                file_id.write(f'MDC={mdc}\n')
                file_id.write(f'FILE_PATH="{file_path}"\n')
                file_id.write(f'VCF_WMD_FILE="{vcf_wmd_file}"\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'export PATH={miniconda3_bin_dir}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin\n')
                file_id.write( 'SEP="#########################################"\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'STATUS_DIR={genlib.get_status_dir(current_run_dir)}\n')
                file_id.write(f'SCRIPT_STATUS_OK={genlib.get_status_ok(current_run_dir)}\n')
                file_id.write(f'SCRIPT_STATUS_WRONG={genlib.get_status_wrong(current_run_dir)}\n')
                file_id.write( 'mkdir -p $STATUS_DIR\n')
                file_id.write( 'if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi\n')
                file_id.write( 'if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi\n')
                file_id.write(f'PARAMS_FILE={params_file}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function init\n')
                file_id.write( '{\n')
                file_id.write( '    INIT_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Script started at $FORMATTED_INIT_DATETIME."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function activate_env_base\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Activating environment base ..."\n')
                file_id.write(f'    source {miniconda3_bin_dir}/activate\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "Environment is activated."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function save_params\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Saving parameters ..."\n')
                file_id.write( '    echo "[General parameters]" > $PARAMS_FILE\n')
                file_id.write( '    echo "threads = $THREADS" >> $PARAMS_FILE\n')
                file_id.write( '    echo "file_format = $FILE_FORMAT" >> $PARAMS_FILE\n')
                file_id.write( '    echo "mdc = $MDC" >> $PARAMS_FILE\n')
                file_id.write( '    echo "file_path = $FILE_PATH" >> $PARAMS_FILE\n')
                file_id.write( '    echo "vcf_wmd_file = $VCF_WMD_FILE" >> $PARAMS_FILE\n')
                file_id.write( '    echo "Parameters are saved."\n')
                file_id.write( '}\n')
                if file_format == 'tabular':
                    file_id.write( '#-------------------------------------------------------------------------------\n')
                    file_id.write( 'function convert_tab_to_vcf\n')
                    file_id.write( '{\n')
                    file_id.write( '    echo "$SEP"\n')
                    file_id.write(f'    echo "Converting file {os.path.basename(file_path)} in tabular format to VCF ..."\n')
                    file_id.write( '    /usr/bin/time \\\n')
                    file_id.write(f'        {app_dir}/tab2vcf.py \\\n')
                    file_id.write(f'            --tab={file_path} \\\n')
                    file_id.write( '            --vcf=$VCF_WMD_FILE \\\n')
                    file_id.write( '            --mdc=$MDC \\\n')
                    file_id.write( '            --verbose=N \\\n')
                    file_id.write( '            --trace=N \n')
                    file_id.write( '    RC=$?\n')
                    file_id.write( '    if [ $RC -ne 0 ]; then manage_error tab2vcf.py $RC; fi\n')
                    file_id.write( '    echo "File is converted."\n')
                    file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function run_naive_imputation_process\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Processing the naive imputation of {os.path.basename(vcf_wmd_file)} ..."\n')
                file_id.write( '    /usr/bin/time \\\n')
                file_id.write(f'        {app_dir}/impute-md-naive.py \\\n')
                file_id.write( '            --threads=$THREADS \\\n')
                file_id.write( '            --input_vcf="$VCF_WMD_FILE" \\\n')
                file_id.write(f'            --output_vcf={vcf_imputed_file} \\\n')
                file_id.write(f'            --impdata={imputation_data_file} \\\n')
                file_id.write( '            --verbose=N \\\n')
                file_id.write( '            --trace=N \\\n')
                file_id.write( '            --tvi=NONE\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error impute-md-naive.py $RC; fi\n')
                file_id.write( '    echo "Naive imputation is ended."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function convert_vcf_to_tab\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Converting VCF file {os.path.basename(vcf_imputed_file)} to a file in tabular format ..."\n')
                file_id.write( '    /usr/bin/time \\\n')
                file_id.write(f'        {app_dir}/vcf2tab.py \\\n')
                file_id.write(f'            --vcf={vcf_imputed_file} \\\n')
                file_id.write(f'            --tab={tab_imputed_file} \\\n')
                file_id.write( '            --mdc=$MDC \\\n')
                file_id.write( '            --verbose=N \\\n')
                file_id.write( '            --trace=N \\\n')
                file_id.write( '            --tvi=NONE\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error vcf2tab.py $RC; fi\n')
                file_id.write( '    echo "File is converted."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function end\n')
                file_id.write( '{\n')
                file_id.write( '    END_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    calculate_duration\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    touch $SCRIPT_STATUS_OK\n')
                file_id.write( '    exit 0\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function manage_error\n')
                file_id.write( '{\n')
                file_id.write( '    END_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    calculate_duration\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "ERROR: $1 returned error $2"\n')
                file_id.write( '    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    touch $SCRIPT_STATUS_WRONG\n')
                file_id.write( '    exit 3\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function calculate_duration\n')
                file_id.write( '{\n')
                file_id.write( '    DURATION=`expr $END_DATETIME - $INIT_DATETIME`\n')
                file_id.write( '    HH=`expr $DURATION / 3600`\n')
                file_id.write( '    MM=`expr $DURATION % 3600 / 60`\n')
                file_id.write( '    SS=`expr $DURATION % 60`\n')
                file_id.write( '    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'init\n')
                file_id.write( 'activate_env_base\n')
                file_id.write( 'save_params\n')
                if file_format == 'tabular':
                    file_id.write('convert_tab_to_vcf\n')
                file_id.write( 'run_naive_imputation_process\n')
                file_id.write( 'convert_vcf_to_tab\n')
                file_id.write( 'end\n')
        except Exception as e:
            error_list.append(f'*** EXCEPTION: "{e}".')
            error_list.append(f'*** ERROR: The file {script_path} is not created.')
            OK = False

        # return the control variable and error list
        return (OK, error_list)

#-------------------------------------------------------------------------------

class FormNaiveImputationReview(QWidget):
    '''
    Class used to review a naive imputation.
    '''

    #---------------

    def __init__(self, parent):
        '''
        Create a class instance.
        '''

        # save parameters in instance variables
        self.parent = parent

        # call the init method of the parent class
        super().__init__()

        # set the dimensions window
        self.window_height = self.parent.WINDOW_HEIGHT - 100
        self.window_width = self.parent.WINDOW_WIDTH - 50

        # set the head and title
        self.head = 'Naive imputation review'
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

        # get the dictionary of application configuration
        self.app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())

        # get the the code list and text list of genotype imputation method
        self.gim_code_list = genlib.get_genotype_imputation_method_code_list()
        self.gim_text_list = genlib.get_genotype_imputation_method_text_list()

        # build the graphic user interface of the window
        self.build_gui()

        # load initial data in inputs
        self.initialize_inputs()

        # check the content of inputs
        self.check_inputs()

        # show the window
        self.show()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        # set the width and height of the window
        self.setFixedSize(self.window_width, self.window_height)

        # move the window at center
        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        # get font metrics information
        fontmetrics = QFontMetrics(QApplication.font())

        # create and configure "label_head"
        label_head = QLabel(self.head, alignment=Qt.AlignCenter)
        label_head.setStyleSheet('font: bold 14px; color: black; background-color: lightGray; max-height: 30px')

        # create and configure "label_naive_process"
        label_naive_process = QLabel()
        label_naive_process.setText('Naive process')
        label_naive_process.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "combobox_naive_process"
        self.combobox_naive_process = QComboBox()
        self.combobox_naive_process.setFixedWidth(fontmetrics.width('9'*20))
        self.combobox_naive_process.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_naive_process.currentIndexChanged.connect(self.check_inputs)

        # create and configure "label_file_format"
        label_file_format = QLabel()
        label_file_format.setText('File format')
        label_file_format.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_file_format"
        self.lineedit_file_format  = QLineEdit()
        self.lineedit_file_format.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_file_format.editingFinished.connect(self.check_inputs)
        self.lineedit_file_format.setReadOnly(True)

        # create and configure "label_mdc"
        label_mdc = QLabel()
        label_mdc.setText('MD char in tabular format')
        label_mdc.setFixedWidth(fontmetrics.width('9'*20))

        # create and configure "lineedit_mdc"
        self.lineedit_mdc  = QLineEdit()
        self.lineedit_mdc.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_mdc.editingFinished.connect(self.check_inputs)
        self.lineedit_mdc.setReadOnly(True)

        # create and configure "label_file_path"
        label_file_path = QLabel()
        label_file_path.setText('File path')
        label_file_path.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_file_path"
        self.lineedit_file_path  = QLineEdit()
        self.lineedit_file_path.editingFinished.connect(self.check_inputs)
        self.lineedit_file_path.setReadOnly(True)

        # create and configure "label_empty"
        label_empty = QLabel()
        label_empty.setFixedWidth(fontmetrics.width('9'*3))

        # create and configure "gridlayout_data"
        gridlayout_data = QGridLayout()
        gridlayout_data.setRowMinimumHeight(0, 60)
        gridlayout_data.setRowMinimumHeight(1, 60)
        gridlayout_data.setRowMinimumHeight(2, 60)
        gridlayout_data.setColumnStretch(0,1)
        gridlayout_data.setColumnStretch(1,1)
        gridlayout_data.setColumnStretch(2,1)
        gridlayout_data.setColumnStretch(3,1)
        gridlayout_data.setColumnStretch(4,1)
        gridlayout_data.setColumnStretch(5,15)
        gridlayout_data.addWidget(label_naive_process, 0, 0)
        gridlayout_data.addWidget(self.combobox_naive_process, 0, 1)
        gridlayout_data.addWidget(label_file_format, 1, 0)
        gridlayout_data.addWidget(self.lineedit_file_format, 1, 1)
        gridlayout_data.addWidget(label_empty, 1, 2)
        gridlayout_data.addWidget(label_mdc, 1, 3)
        gridlayout_data.addWidget(self.lineedit_mdc, 1, 4)
        gridlayout_data.addWidget(label_file_path, 2, 0)
        gridlayout_data.addWidget(self.lineedit_file_path, 2, 1, 1, 5)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        # create and configure "pushbutton_execute"
        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Review the process of the naive imputation.')
        self.pushbutton_execute.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_execute.clicked.connect(self.pushbutton_execute_clicked)

        # create and configure "pushbutton_close"
        pushbutton_close = QPushButton('Close')
        pushbutton_close.setToolTip('Close the window.')
        pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        # create and configure "gridlayout_buttons"
        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 15)
        gridlayout_buttons.setColumnStretch(1, 1)
        gridlayout_buttons.setColumnStretch(2, 1)
        gridlayout_buttons.addWidget(self.pushbutton_execute, 0, 1, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(pushbutton_close, 0, 2, alignment=Qt.AlignCenter)

        # create and configure "groupbox_buttons"
        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)

        # create and configure "gridlayout_central"
        gridlayout_central = QGridLayout()
        gridlayout_central.setRowStretch(0, 1)
        gridlayout_central.setRowStretch(1, 1)
        gridlayout_central.setRowStretch(2, 1)
        gridlayout_central.setRowStretch(3, 1)
        gridlayout_central.setRowStretch(4, 1)
        gridlayout_central.setColumnStretch(0, 0)
        gridlayout_central.setColumnStretch(1, 1)
        gridlayout_central.setColumnStretch(2, 0)
        gridlayout_central.addWidget(label_head, 0, 1)
        gridlayout_central.addWidget(QLabel(), 1, 1)
        gridlayout_central.addWidget(groupbox_data, 2, 1)
        gridlayout_central.addWidget(QLabel(), 3, 1)
        gridlayout_central.addWidget(groupbox_buttons, 4, 1)

        # create and configure "groupbox_central"
        groupbox_central = QGroupBox()
        groupbox_central.setLayout(gridlayout_central)

        # create and configure "vboxlayout"
        vboxlayout = QVBoxLayout(self)
        vboxlayout.addWidget(groupbox_central)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # populate data in "combobox_naive_process"
        self.combobox_naive_process_populate()

        # set initial value in "lineedit_file_format"
        self.lineedit_file_format.setText('')

        # set initial value in "lineedit_mdc"
        self.lineedit_mdc.setText('')

        # set initial value in "lineedit_file_path"
        self.lineedit_file_path.setText('')

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # check "combobox_naive_process" when the index changed
        self.combobox_naive_process_currentIndexChanged()

        # check "lineedit_file_format" when the editing finished
        if not self.lineedit_file_format_editing_finished():
            OK = False

        # check "lineedit_mdc_editing" when the editing finished
        if not self.lineedit_mdc_editing_finished():
            OK = False

        # check "lineedit_file_path" when the editing finished
        if not self.lineedit_file_path_editing_finished():
            OK = False

        # check all inputs are OK
        if OK:
            self.parent.statusBar().showMessage('')
        else:
            self.parent.statusBar().showMessage('There are one or more inputs without data or with wrong values.')

        # enable "pushbutton_execute"
        if OK and self.combobox_naive_process.currentText() != '' and self.combobox_file_format.currentText() != '' and self.lineedit_mdc.text() != '' and self.lineedit_file_path.text() != '':
            self.pushbutton_execute.setEnabled(True)
        else:
            self.pushbutton_execute.setEnabled(False)

        # return the control variable
        return OK

    #---------------

    def combobox_naive_process_populate(self):
        '''
        Populate data in "combobox_naive_process".
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # set the imputation result directory
        imputation_result_subdir = f'{result_dir}/{genlib.get_result_imputation_subdir()}'
        if sys.platform.startswith('win32'):
            imputation_result_subdir = genlib.wsl_path_2_windows_path(imputation_result_subdir)

        # initialize the list of naive processes
        naive_process_dir_list = []

        # build the list of naive processes
        try:
            for entry in os.listdir(imputation_result_subdir):
                if os.path.isdir(f'{imputation_result_subdir}{os.sep}{entry}') and entry.startswith(genlib.get_naive_imputation_code()):
                    status_ok = os.path.isfile(genlib.get_status_ok(f'{imputation_result_subdir}{os.sep}{entry}'))
                    if status_ok:
                        naive_process_dir_list.append(entry)
            naive_process_dir_list.sort()
        except:    # pylint: disable=bare-except
            pass

        # populate data in "combobox_naive_process"
        self.combobox_naive_process.addItems([''] + naive_process_dir_list)

        # simultate "combobox_naive_process" index has changed
        self.combobox_naive_process_currentIndexChanged()

    #---------------

    def combobox_naive_process_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_naive_process" has been selected.
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # if there is a naive process selected
        if self.combobox_naive_process.currentText() != '':

            try:
                # set the naive process directory
                naive_process_dir = f'{result_dir}/{genlib.get_result_imputation_subdir()}/{self.combobox_naive_process.currentText()}'
                # set the parameter file
                params_file = f'{naive_process_dir}/params.txt'
                if sys.platform.startswith('win32'):
                    params_file = genlib.wsl_path_2_windows_path(params_file)
                # get the parameter dictionary
                params_dict = genlib.get_config_dict(params_file)
            except:    # pylint: disable=bare-except
                params_dict = {}

            # if there are items in the pamameter dictionary
            if params_dict:

                self.lineedit_file_format.setText(os.path.basename(params_dict['General parameters']['file_format']))
                self.lineedit_mdc.setText(os.path.basename(params_dict['General parameters']['mdc']))
                file_path = params_dict['General parameters']['file_path']
                if sys.platform.startswith('win32'):
                    file_path = genlib.wsl_path_2_windows_path(file_path)
                self.lineedit_file_path.setText(file_path)

        # if there are not items in the pamameter dictionary
        else:

            self.lineedit_file_format.setText('')
            self.lineedit_mdc.setText('')
            self.lineedit_file_path.setText('')

    #---------------

    def lineedit_file_format_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_file_format"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_mdc_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_mdc"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_file_path_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_file_path"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def pushbutton_execute_clicked(self):
        '''
        Execute the process.
        '''

         # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # set the imputation data file
        imputation_data_file = f'{result_dir}/{genlib.get_result_imputation_subdir()}/{self.combobox_naive_process.currentText()}/imputation_data.csv'
        if sys.platform.startswith('win32'):
            imputation_data_file = genlib.wsl_path_2_windows_path(imputation_data_file)

        # set the head of the imputation plot
        head = f'{self.head}: {self.combobox_naive_process.currentText()}'

        # create and show the imputation plot
        imputation_plot = DialogImputationPlot(self, head, imputation_data_file)
        imputation_plot.show()

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.parent.current_subwindow = None
        self.close()
        self.parent.set_background_image()

#-------------------------------------------------------------------------------

class FormGenotypeDatabase(QWidget):
    '''
    Class used to build a genotype database from a VCF file.
    '''

    #---------------

    def __init__(self, parent):
        '''
        Create a class instance.
        '''

        # save parameters in instance variables
        self.parent = parent

        # call the init method of the parent class
        super().__init__()

        # set the dimensions window
        self.window_height = self.parent.WINDOW_HEIGHT - 100
        self.window_width = self.parent.WINDOW_WIDTH - 50

        # set the head and title
        self.head = genlib.get_gtdb_building_name()
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

        # get the dictionary of application configuration
        self.app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())

        # build the graphic user interface of the window
        self.build_gui()

        # load initial data in inputs
        self.initialize_inputs()

        # check the content of inputs
        self.check_inputs()

        # show the window
        self.show()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        # set the width and height of the window
        self.setFixedSize(self.window_width, self.window_height)

        # move the window at center
        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        # get font metrics information
        fontmetrics = QFontMetrics(QApplication.font())

        # create and configure "label_head"
        label_head = QLabel(self.head, alignment=Qt.AlignCenter)
        label_head.setStyleSheet('font: bold 14px; color: black; background-color: lightGray; max-height: 30px')

        # create and configure "label_threads"
        label_threads = QLabel()
        label_threads.setText('Threads')
        label_threads.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_threads"
        self.lineedit_threads  = QLineEdit()
        self.lineedit_threads.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_threads.editingFinished.connect(self.check_inputs)
        self.lineedit_threads.setReadOnly(True)

        # create and configure "label_file_format"
        label_file_format = QLabel()
        label_file_format.setText('File format')
        label_file_format.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "combobox_file_format"
        self.combobox_file_format = QComboBox()
        self.combobox_file_format.setFixedWidth(fontmetrics.width('9'*10))
        self.combobox_file_format.currentIndexChanged.connect(self.check_inputs)

        # create and configure "label_mdc"
        label_mdc = QLabel()
        label_mdc.setText('MD char in tabular format')
        label_mdc.setFixedWidth(fontmetrics.width('9'*20))

        # create and configure "lineedit_mdc"
        self.lineedit_mdc  = QLineEdit()
        self.lineedit_mdc.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_mdc.editingFinished.connect(self.check_inputs)

        # create and configure "label_file_path"
        label_file_path = QLabel()
        label_file_path.setText('File path')
        label_file_path.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_file_path"
        self.lineedit_file_path  = QLineEdit()
        self.lineedit_file_path.editingFinished.connect(self.check_inputs)

        # create and configure "pushbutton_search"
        pushbutton_search = QPushButton('Search ...')
        pushbutton_search.setToolTip('Search and select the file with missing data in genotypes.')
        pushbutton_search.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_search.clicked.connect(self.pushbutton_search_clicked)

        # create and configure "label_empty"
        label_empty = QLabel()
        label_empty.setFixedWidth(fontmetrics.width('9'*3))

        # create and configure "gridlayout_data"
        gridlayout_data = QGridLayout()
        gridlayout_data.setRowMinimumHeight(0, 60)
        gridlayout_data.setRowMinimumHeight(1, 60)
        gridlayout_data.setRowMinimumHeight(2, 60)
        gridlayout_data.setColumnStretch(0,1)
        gridlayout_data.setColumnStretch(1,1)
        gridlayout_data.setColumnStretch(2,1)
        gridlayout_data.setColumnStretch(3,1)
        gridlayout_data.setColumnStretch(4,1)
        gridlayout_data.setColumnStretch(5,15)
        gridlayout_data.setColumnStretch(6,1)
        gridlayout_data.addWidget(label_threads, 0, 0)
        gridlayout_data.addWidget(self.lineedit_threads, 0, 1)
        gridlayout_data.addWidget(label_file_format, 1, 0)
        gridlayout_data.addWidget(self.combobox_file_format, 1, 1)
        gridlayout_data.addWidget(label_empty, 1, 2)
        gridlayout_data.addWidget(label_mdc, 1, 3)
        gridlayout_data.addWidget(self.lineedit_mdc, 1, 4)
        gridlayout_data.addWidget(label_file_path, 2, 0)
        gridlayout_data.addWidget(self.lineedit_file_path, 2, 1, 1, 5)
        gridlayout_data.addWidget(pushbutton_search, 2, 6)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        # create and configure "pushbutton_execute"
        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Execute the genotype database building.')
        self.pushbutton_execute.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_execute.clicked.connect(self.pushbutton_execute_clicked)

        # create and configure "pushbutton_close"
        button_close = QPushButton('Close')
        button_close.setToolTip('Cancel the genotype database building and close the window.')
        button_close.setCursor(QCursor(Qt.PointingHandCursor))
        button_close.clicked.connect(self.pushbutton_close_clicked)

        # create and configure "gridlayout_buttons"
        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 15)
        gridlayout_buttons.setColumnStretch(1, 1)
        gridlayout_buttons.setColumnStretch(2, 1)
        gridlayout_buttons.addWidget(self.pushbutton_execute, 0, 1, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(button_close, 0, 2, alignment=Qt.AlignCenter)

        # create and configure "groupbox_buttons"
        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)

        # create and configure "gridlayout_central"
        gridlayout_central = QGridLayout()
        gridlayout_central.setRowStretch(0, 1)
        gridlayout_central.setRowStretch(1, 1)
        gridlayout_central.setRowStretch(2, 1)
        gridlayout_central.setRowStretch(3, 1)
        gridlayout_central.setRowStretch(4, 1)
        gridlayout_central.setColumnStretch(0, 0)
        gridlayout_central.setColumnStretch(1, 1)
        gridlayout_central.setColumnStretch(2, 0)
        gridlayout_central.addWidget(label_head, 0, 1)
        gridlayout_central.addWidget(QLabel(), 1, 1)
        gridlayout_central.addWidget(groupbox_data, 2, 1)
        gridlayout_central.addWidget(QLabel(), 3, 1)
        gridlayout_central.addWidget(groupbox_buttons, 4, 1)

        # create and configure "groupbox_central"
        groupbox_central = QGroupBox()
        groupbox_central.setLayout(gridlayout_central)

        # create and configure "vboxlayout"
        vboxlayout = QVBoxLayout(self)
        vboxlayout.addWidget(groupbox_central)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # set initial value in "lineedit_threads"
        self.lineedit_threads.setText('1')

        # populate data in "combobox_file_format"
        self.combobox_file_format_populate()
        self.combobox_file_format.setCurrentIndex(1)

        # set initial value in "lineedit_mdc"
        self.lineedit_mdc.setText('0')

        # set initial value in "lineedit_file_path"
        self.lineedit_file_path.setText('')

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # check "lineedit_threads" when the editing finished
        if not self.lineedit_threads_editing_finished():
            OK = False

        # check "combobox_file_format" when the index changed
        self.combobox_file_format_currentIndexChanged()

        # check "lineedit_mdc_editing" when the editing finished
        if not self.lineedit_mdc_editing_finished():
            OK = False

        # check "lineedit_file_path" when the editing finished
        if not self.lineedit_file_path_editing_finished():
            OK = False

        # check all inputs are OK
        if OK:
            self.parent.statusBar().showMessage('')
        else:
            self.parent.statusBar().showMessage('There are one or more inputs without data or with wrong values.')

        # enable "pushbutton_execute"
        if OK and self.lineedit_threads.text() != '' and self.combobox_file_format.currentText() != '' and self.lineedit_mdc.text() != '' and self.lineedit_file_path.text() != '':
            self.pushbutton_execute.setEnabled(True)
        else:
            self.pushbutton_execute.setEnabled(False)

        # return the control variable
        return OK

    #---------------

    def lineedit_threads_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_threads"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_threads" is empty
        if self.lineedit_threads.text() == '':
            OK = False
            self.lineedit_threads.setStyleSheet('background-color: white')

        # chek if "lineedit_threads" is an integer number between 1 and the CPUs number in the computer
        elif self.lineedit_threads.text() != '' and not genlib.check_int(self.lineedit_threads.text(), minimum=1, maximum=os.cpu_count()):
            OK = False
            self.lineedit_threads.setStyleSheet('background-color: red')
            text = f'The value of threads number has to be an integer number between 1 and {os.cpu_count()} (threads available in the computer).'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_threads.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def combobox_file_format_populate(self):
        '''
        Populate data in "combobox_file_format".
        '''

        # populate data in "combobox_file_format"
        self.combobox_file_format.addItems(genlib.get_format_type_code_list())

        # simultate "combobox_file_format" index has changed
        self.combobox_file_format_currentIndexChanged()

    #---------------

    def combobox_file_format_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_file_format" has been selected.
        '''

        pass

    #---------------

    def lineedit_mdc_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_mcd"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_mcd" is empty
        if self.lineedit_mdc.text() == '':
            OK = False

        # return the control variable
        return OK

    #---------------

    def lineedit_file_path_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_file_path"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_file_path" is empty
        if self.lineedit_file_path.text() == '':
            OK = False
            self.lineedit_file_path.setStyleSheet('background-color: white')

        # chek if "lineedit_file_path" is an integer number between 1 and the CPUs number in the computer
        elif self.lineedit_file_path.text() != '' and not os.path.isfile(self.lineedit_file_path.text()):
            OK = False
            self.lineedit_file_path.setStyleSheet('background-color: red')
            text = 'The file path has to be an existing file.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_file_path.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def pushbutton_search_clicked(self):
        '''
        Search and select a file with missing data.
        '''

        # get the file with missing data
        if self.combobox_file_format.currentText() == 'tabular':
            (file, _) = QFileDialog.getOpenFileName(self, f'{self.head} - Selection of the file', os.path.expanduser('~'), 'Text files (*.txt);;TSV files (*.tsv);;All files (*)')
        elif self.combobox_file_format.currentText() == 'VCF':
            (file, _) = QFileDialog.getOpenFileName(self, f'{self.head} - Selection of the file', os.path.expanduser('~'), 'VCF files (*.vcf);;All files (*)')
        self.lineedit_file_path.setText(file)

        # check the content of inputs
        self.check_inputs()

    #---------------

    def pushbutton_execute_clicked(self):
        '''
        Execute the process.
        '''

        # check the content of inputs
        OK = self.check_inputs()
        if not OK:
            text = 'Some input values are not OK.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        # confirm the process is executed
        if OK:
            text = 'The genotype database building is going to be run.\n\nAre you sure to continue?'
            botton = QMessageBox.question(self, self.title, text, buttons=QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)
            if botton == QMessageBox.No:
                OK = False

        # execute the process
        if OK:
            threads = self.lineedit_threads.text()
            file_format = self.combobox_file_format.currentText()
            mdc = self.lineedit_mdc.text()
            file_path = self.lineedit_file_path.text()
            process = dialogs.DialogProcess(self, self.head, self.run_gtdb_building, threads, file_format, mdc, file_path)
            process.exec()

        # close the windows
        if OK:
            self.pushbutton_close_clicked()

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.parent.current_subwindow = None
        self.close()
        self.parent.set_background_image()

   #---------------

    def run_gtdb_building(self, process, threads, file_format, mdc, file_path):
        '''
        Run a process of genotype database building.
        '''

        # initialize the control variable
        OK = True

        # warn that the log window does not have to be closed
        process.write('This process might take several minutes. Do not close this window, please wait!\n')

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # determine the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write('Determining the temporal directory ...\n')
            temp_dir = genlib.get_temp_dir()
            command = f'mkdir -p {temp_dir}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write(f'The directory path is {temp_dir}.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # determine the run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write('Determining the run directory ...\n')
            current_run_dir = genlib.get_current_run_dir(result_dir, genlib.get_result_imputation_subdir(), genlib.get_gtdb_building_code())
            command = f'mkdir -p {current_run_dir}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write(f'The directory path is {current_run_dir}.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # build the database building script in the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            script_name = f'{genlib.get_gtdb_building_code()}-process.sh'
            process.write(f'Building the script {script_name} ...\n')
            (OK, _) = self.build_gtdb_script(temp_dir, script_name, current_run_dir, threads, file_format, mdc, file_path)
            if OK:
                process.write('The file is built.\n')
            else:
                process.write('*** ERROR: The file could not be built.\n')

        # copy the database building script to the current run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Copying the script {script_name} to the directory {current_run_dir} ...\n')
            command = f'cp {temp_dir}/{script_name} {current_run_dir}; [ $? -eq 0 ] &&  exit 0 || exit 1'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The file is copied.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')

        # set run permision to the database building script
        if OK and not sys.platform.startswith('win32'):
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Setting on the run permision of {script_name} ...\n')
            command = f'chmod u+x {current_run_dir}/{script_name}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The run permision is set.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # build the starter script in the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            starter_name = f'{genlib.get_gtdb_building_code()}-process-starter.sh'
            process.write(f'Building the starter script {starter_name} ...\n')
            (OK, _) = genlib.build_starter(temp_dir, starter_name, script_name, current_run_dir)
            if OK:
                process.write('The file is built.\n')
            if not OK:
                process.write('***ERROR: The file could not be built.\n')

        # copy the starter script to the current run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Copying the starter {starter_name} to the directory {current_run_dir} ...\n')
            command = f'cp {temp_dir}/{starter_name} {current_run_dir}; [ $? -eq 0 ] &&  exit 0 || exit 1'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The file is copied.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')

        # set run permision to the starter script
        if OK and not sys.platform.startswith('win32'):
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Setting on the run permision of {starter_name} ...\n')
            command = f'chmod u+x {current_run_dir}/{starter_name}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The run permision is set.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # submit the starter
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Submitting the starter {starter_name} ...\n')
            command = f'{current_run_dir}/{starter_name} &'
            rc = genlib.run_command(command, process, is_script=True)
            if rc == 0:
                process.write('The script is submitted.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        process.write(f'{genlib.get_separator()}\n')
        process.write('You can close this window now.\n')

        # return the control variable
        return OK

   #---------------

    def build_gtdb_script(self, directory, script_name, current_run_dir, threads, file_format, mdc, file_path):
        '''
        Build the script to run the genotype database building.
        '''

        # initialize the control variable and error list
        OK = True
        error_list = []

        # get items from dictionary of application configuration
        app_dir = self.app_config_dict['Environment parameters']['app_dir']
        miniconda3_bin_dir = self.app_config_dict['Environment parameters']['miniconda3_bin_dir']

        # set the parameters file
        params_file = f'{current_run_dir}/params.txt'

        # set the file path in WSL
        if sys.platform.startswith('win32'):
            file_path = genlib.windows_path_2_wsl_path(file_path)

        # set the files with missing data
        if file_format == 'tabular':
            tab_wmd_file = f'{current_run_dir}/wmd.txt'
            vcf_wmd_file = f'{current_run_dir}/wmd.vcf'
        elif file_format == 'VCF':
            vcf_wmd_file = f'{current_run_dir}/wmd.vcf'

        # set the genotype database file
        genotype_db = f'{current_run_dir}/genotype.db'

        # set the script path
        script_path = f'{directory}/{script_name}'

        # write the script
        try:
            with open(script_path, mode='w', encoding='iso-8859-1', newline='\n') as file_id:
                file_id.write( '#!/bin/bash\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'export PATH={miniconda3_bin_dir}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin\n')
                file_id.write( 'SEP="#########################################"\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'THREADS={threads}\n')
                file_id.write(f'FILE_FORMAT={file_format}\n')
                file_id.write(f'MDC={mdc}\n')
                file_id.write(f'FILE_PATH="{file_path}"\n')
                file_id.write(f'VCF_WMD_FILE="{vcf_wmd_file}"\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'STATUS_DIR={genlib.get_status_dir(current_run_dir)}\n')
                file_id.write(f'SCRIPT_STATUS_OK={genlib.get_status_ok(current_run_dir)}\n')
                file_id.write(f'SCRIPT_STATUS_WRONG={genlib.get_status_wrong(current_run_dir)}\n')
                file_id.write( 'mkdir -p $STATUS_DIR\n')
                file_id.write( 'if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi\n')
                file_id.write( 'if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi\n')
                file_id.write(f'PARAMS_FILE={params_file}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function init\n')
                file_id.write( '{\n')
                file_id.write( '    INIT_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Script started at $FORMATTED_INIT_DATETIME."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function activate_env_base\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Activating environment base ..."\n')
                file_id.write(f'    source {miniconda3_bin_dir}/activate\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "Environment is activated."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function save_params\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Saving parameters ..."\n')
                file_id.write( '    echo "[General parameters]" > $PARAMS_FILE\n')
                file_id.write( '    echo "threads = $THREADS" >> $PARAMS_FILE\n')
                file_id.write( '    echo "file_format = $FILE_FORMAT" >> $PARAMS_FILE\n')
                file_id.write( '    echo "mdc = $MDC" >> $PARAMS_FILE\n')
                file_id.write( '    echo "file_path = $FILE_PATH" >> $PARAMS_FILE\n')
                file_id.write( '    echo "vcf_wmd_file = $VCF_WMD_FILE" >> $PARAMS_FILE\n')
                file_id.write( '    echo "Parameters are saved."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function copy_file\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Coping {os.path.basename(file_path)} to {current_run_dir} ..."\n')
                file_id.write( '    /usr/bin/time \\\n')
                if file_format == 'tabular':
                    file_id.write(f'        cp "{file_path}" "{tab_wmd_file}"\n')
                elif file_format == 'VCF':
                    file_id.write(f'        cp "{file_path}" $VCF_WMD_FILE\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error cp $RC; fi\n')
                file_id.write( '    echo "Genotype database is built."\n')
                file_id.write( '}\n')
                if file_format == 'tabular':
                    file_id.write( '#-------------------------------------------------------------------------------\n')
                    file_id.write( 'function convert_tab_to_vcf\n')
                    file_id.write( '{\n')
                    file_id.write( '    echo "$SEP"\n')
                    file_id.write(f'    echo "Converting file {os.path.basename(file_path)} in tabular format to VCF ..."\n')
                    file_id.write( '    /usr/bin/time \\\n')
                    file_id.write(f'        {app_dir}/tab2vcf.py \\\n')
                    file_id.write(f'            --tab="{tab_wmd_file}" \\\n')
                    file_id.write( '            --vcf=$VCF_WMD_FILE \\\n')
                    file_id.write( '            --mdc=$MDC \\\n')
                    file_id.write( '            --verbose=N \\\n')
                    file_id.write( '            --trace=N \n')
                    file_id.write( '    RC=$?\n')
                    file_id.write( '    if [ $RC -ne 0 ]; then manage_error tab2vcf.py $RC; fi\n')
                    file_id.write( '    echo "File is converted."\n')
                    file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function build_genotype_db\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Building the genotype database from {os.path.basename(file_path)} ..."\n')
                file_id.write( '    /usr/bin/time \\\n')
                file_id.write(f'        {app_dir}/calculate-genotype-data.py \\\n')
                file_id.write(f'            --threads={threads} \\\n')
                file_id.write(f'            --gtdb={genotype_db} \\\n')
                file_id.write( '            --vcf=$VCF_WMD_FILE \\\n')
                file_id.write( '            --verbose=N \\\n')
                file_id.write( '            --trace=N \\\n')
                file_id.write( '            --tvi=NONE\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error calculate-genotype-data.py $RC; fi\n')
                file_id.write( '    echo "Genotype database is built."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function end\n')
                file_id.write( '{\n')
                file_id.write( '    END_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    calculate_duration\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    touch $SCRIPT_STATUS_OK\n')
                file_id.write( '    exit 0\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function manage_error\n')
                file_id.write( '{\n')
                file_id.write( '    END_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    calculate_duration\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "ERROR: $1 returned error $2"\n')
                file_id.write( '    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    touch $SCRIPT_STATUS_WRONG\n')
                file_id.write( '    exit 3\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function calculate_duration\n')
                file_id.write( '{\n')
                file_id.write( '    DURATION=`expr $END_DATETIME - $INIT_DATETIME`\n')
                file_id.write( '    HH=`expr $DURATION / 3600`\n')
                file_id.write( '    MM=`expr $DURATION % 3600 / 60`\n')
                file_id.write( '    SS=`expr $DURATION % 60`\n')
                file_id.write( '    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'init\n')
                file_id.write( 'activate_env_base\n')
                file_id.write( 'save_params\n')
                file_id.write( 'copy_file\n')
                if file_format == 'tabular':
                    file_id.write('convert_tab_to_vcf\n')
                file_id.write( 'build_genotype_db\n')
                file_id.write( 'end\n')
        except Exception as e:
            error_list.append(f'*** EXCEPTION: "{e}".')
            error_list.append(f'*** ERROR: The file {script_path} is not created.')
            OK = False

        # return the control variable and error list
        return (OK, error_list)

#-------------------------------------------------------------------------------

class FormSOMImputation(QWidget):
    '''
    Class used to perform a SOM imputation.
    '''

    #---------------

    def __init__(self, parent):
        '''
        Create a class instance.
        '''

        # save parameters in instance variables
        self.parent = parent

        # call the init method of the parent class
        super().__init__()

        # set the dimensions window
        self.window_height = self.parent.WINDOW_HEIGHT - 100
        self.window_width = self.parent.WINDOW_WIDTH - 50

        # set the head and title
        self.head = genlib.get_som_imputation_name()
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

        # get the dictionary of application configuration
        self.app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())

        # get the the code list and text list of genotype imputation method
        self.gim_code_list = genlib.get_genotype_imputation_method_code_list()
        self.gim_text_list = genlib.get_genotype_imputation_method_text_list()

        # build the graphic user interface of the window
        self.build_gui()

        # load initial data in inputs
        self.initialize_inputs()

        # check the content of inputs
        self.check_inputs()

        # show the window
        self.show()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        # set the width and height of the window
        self.setFixedSize(self.window_width, self.window_height)

        # move the window at center
        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        # get font metrics information
        fontmetrics = QFontMetrics(QApplication.font())

        # create and configure "label_head"
        label_head = QLabel(self.head, alignment=Qt.AlignCenter)
        label_head.setStyleSheet('font: bold 14px; color: black; background-color: lightGray; max-height: 30px')

        # create and configure "label_threads"
        label_threads = QLabel()
        label_threads.setText('Threads')
        label_threads.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_threads"
        self.lineedit_threads  = QLineEdit()
        self.lineedit_threads.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_threads.editingFinished.connect(self.check_inputs)
        self.lineedit_threads.setReadOnly(True)

        # create and configure "label_gtdb"
        label_gtdb = QLabel()
        label_gtdb.setText('Genotype database')
        label_gtdb.setFixedWidth(fontmetrics.width('9'*16))

        # create and configure "combobox_gtdb"
        self.combobox_gtdb = QComboBox()
        self.combobox_gtdb.setFixedWidth(fontmetrics.width('9'*20))
        self.combobox_gtdb.currentIndexChanged.connect(self.check_inputs)

        # create and configure "label_file_format"
        label_file_format = QLabel()
        label_file_format.setText('File format')
        label_file_format.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_file_format"
        self.lineedit_file_format  = QLineEdit()
        self.lineedit_file_format.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_file_format.editingFinished.connect(self.check_inputs)
        self.lineedit_file_format.setReadOnly(True)

        # create and configure "label_mdc"
        label_mdc = QLabel()
        label_mdc.setText('MD char in tabular format')
        label_mdc.setFixedWidth(fontmetrics.width('9'*20))

        # create and configure "lineedit_mdc"
        self.lineedit_mdc  = QLineEdit()
        self.lineedit_mdc.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_mdc.editingFinished.connect(self.check_inputs)
        self.lineedit_mdc.setReadOnly(True)

        # create and configure "label_file_path"
        label_file_path = QLabel()
        label_file_path.setText('File path')
        label_file_path.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_file_path"
        self.lineedit_file_path  = QLineEdit()
        self.lineedit_file_path.editingFinished.connect(self.check_inputs)
        self.lineedit_file_path.setReadOnly(True)

        # create and configure "label_xdim"
        label_xdim = QLabel()
        label_xdim.setText('X dimension')
        label_xdim.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_xdim"
        self.lineedit_xdim  = QLineEdit()
        self.lineedit_xdim.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_xdim.editingFinished.connect(self.check_inputs)

        # create and configure "label_ydim"
        label_ydim = QLabel()
        label_ydim.setText('Y dimension')
        label_ydim.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_ydim"
        self.lineedit_ydim  = QLineEdit()
        self.lineedit_ydim.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_ydim.editingFinished.connect(self.check_inputs)

        # create and configure "label_sigma"
        label_sigma = QLabel()
        label_sigma.setText('Sigma')
        label_sigma.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_sigma"
        self.lineedit_sigma  = QLineEdit()
        self.lineedit_sigma.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_sigma.editingFinished.connect(self.check_inputs)

        # create and configure "label_ilrate"
        label_ilrate = QLabel()
        label_ilrate.setText('Learning rate')
        label_ilrate.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_ilrate"
        self.lineedit_ilrate  = QLineEdit()
        self.lineedit_ilrate.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_ilrate.editingFinished.connect(self.check_inputs)

        # create and configure "label_iterations"
        label_iterations = QLabel()
        label_iterations.setText('Maximum iterations #')
        label_iterations.setFixedWidth(fontmetrics.width('9'*18))

        # create and configure "lineedit_iterations"
        self.lineedit_iterations  = QLineEdit()
        self.lineedit_iterations.setFixedWidth(fontmetrics.width('9'*22))
        self.lineedit_iterations.editingFinished.connect(self.check_inputs)

        # create and configure "label_empty"
        label_empty = QLabel()
        label_empty.setFixedWidth(fontmetrics.width('9'*3))

        # create and configure "gridlayout_somparam"
        gridlayout_somparam = QGridLayout()
        gridlayout_somparam.setRowMinimumHeight(0, 30)
        gridlayout_somparam.setRowMinimumHeight(1, 30)
        gridlayout_somparam.setColumnStretch(0, 1)
        gridlayout_somparam.setColumnStretch(1, 1)
        gridlayout_somparam.setColumnStretch(2, 1)
        gridlayout_somparam.setColumnStretch(3, 1)
        gridlayout_somparam.setColumnStretch(4, 1)
        gridlayout_somparam.setColumnStretch(5, 1)
        gridlayout_somparam.setColumnStretch(6, 2)
        gridlayout_somparam.setColumnStretch(7, 2)
        gridlayout_somparam.addWidget(label_xdim, 0, 0)
        gridlayout_somparam.addWidget(self.lineedit_xdim, 0, 1, alignment=Qt.AlignLeft)
        gridlayout_somparam.addWidget(label_empty, 0, 2)
        gridlayout_somparam.addWidget(label_ydim, 0, 3)
        gridlayout_somparam.addWidget(self.lineedit_ydim, 0, 4, alignment=Qt.AlignLeft)
        gridlayout_somparam.addWidget(label_empty, 0, 5)
        gridlayout_somparam.addWidget(label_sigma, 1, 0)
        gridlayout_somparam.addWidget(self.lineedit_sigma, 1, 1, alignment=Qt.AlignLeft)
        gridlayout_somparam.addWidget(label_ilrate, 1, 3)
        gridlayout_somparam.addWidget(self.lineedit_ilrate, 1, 4, alignment=Qt.AlignLeft)
        gridlayout_somparam.addWidget(label_iterations, 1, 6)
        gridlayout_somparam.addWidget(self.lineedit_iterations, 1, 7, alignment=Qt.AlignLeft)

        # create and configure "groupbox_somparam"
        groupbox_somparam = QGroupBox('SOM parameters')
        groupbox_somparam.setLayout(gridlayout_somparam)

        # create and configure "label_mr2"
        label_mr2 = QLabel()
        label_mr2.setText('Minimum r^2')
        label_mr2.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_mr2"
        self.lineedit_mr2  = QLineEdit()
        self.lineedit_mr2.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_mr2.editingFinished.connect(self.check_inputs)

        # create and configure "label_snps"
        label_snps = QLabel()
        label_snps.setText('SNPs #')
        label_snps.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_snps"
        self.lineedit_snps  = QLineEdit()
        self.lineedit_snps.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_snps.editingFinished.connect(self.check_inputs)

        # create and configure "label_gim"
        label_gim = QLabel()
        label_gim.setText('Imputation method')
        label_gim.setFixedWidth(fontmetrics.width('9'*18))

        # create and configure "combobox_gim"
        self.combobox_gim = QComboBox()
        self.combobox_gim.currentIndexChanged.connect(self.check_inputs)
        self.combobox_gim.setFixedWidth(fontmetrics.width('9'*22))

        # create and configure "gridlayout_snpsparam"
        gridlayout_snpsparam = QGridLayout()
        gridlayout_snpsparam.setColumnStretch(0, 1)
        gridlayout_snpsparam.setColumnStretch(1, 1)
        gridlayout_snpsparam.setColumnStretch(2, 1)
        gridlayout_snpsparam.setColumnStretch(3, 1)
        gridlayout_snpsparam.setColumnStretch(4, 1)
        gridlayout_snpsparam.setColumnStretch(5, 1)
        gridlayout_snpsparam.setColumnStretch(6, 2)
        gridlayout_snpsparam.setColumnStretch(7, 2)
        gridlayout_snpsparam.addWidget(label_mr2, 0, 0)
        gridlayout_snpsparam.addWidget(self.lineedit_mr2, 0, 1, alignment=Qt.AlignLeft)
        gridlayout_snpsparam.addWidget(label_empty, 0, 2)
        gridlayout_snpsparam.addWidget(label_snps, 0, 3)
        gridlayout_snpsparam.addWidget(self.lineedit_snps, 0, 4, alignment=Qt.AlignLeft)
        gridlayout_snpsparam.addWidget(label_empty, 0, 5)
        gridlayout_snpsparam.addWidget(label_gim, 0, 6)
        gridlayout_snpsparam.addWidget(self.combobox_gim, 0, 7, alignment=Qt.AlignLeft)

        # create and configure "groupbox_snpsparam"
        groupbox_snpsparam = QGroupBox('SNPs selection parameters')
        groupbox_snpsparam.setLayout(gridlayout_snpsparam)

        # create and configure "gridlayout_data"
        gridlayout_data = QGridLayout()
        gridlayout_data.setRowMinimumHeight(0, 30)
        gridlayout_data.setRowMinimumHeight(1, 30)
        gridlayout_data.setRowMinimumHeight(2, 30)
        gridlayout_data.setRowMinimumHeight(3, 100)
        gridlayout_data.setRowMinimumHeight(4, 60)
        gridlayout_data.setColumnStretch(0,1)
        gridlayout_data.setColumnStretch(1,1)
        gridlayout_data.setColumnStretch(2,1)
        gridlayout_data.setColumnStretch(3,1)
        gridlayout_data.setColumnStretch(4,1)
        gridlayout_data.setColumnStretch(5,15)
        gridlayout_data.addWidget(label_threads, 0, 0)
        gridlayout_data.addWidget(self.lineedit_threads, 0, 1, alignment=Qt.AlignLeft)
        gridlayout_data.addWidget(label_empty, 0, 2)
        gridlayout_data.addWidget(label_gtdb, 0, 3)
        gridlayout_data.addWidget(self.combobox_gtdb, 0, 4, alignment=Qt.AlignLeft)
        gridlayout_data.addWidget(label_file_format, 1, 0)
        gridlayout_data.addWidget(self.lineedit_file_format, 1, 1)
        gridlayout_data.addWidget(label_empty, 1, 2)
        gridlayout_data.addWidget(label_mdc, 1, 3)
        gridlayout_data.addWidget(self.lineedit_mdc, 1, 4)
        gridlayout_data.addWidget(label_file_path, 2, 0)
        gridlayout_data.addWidget(self.lineedit_file_path, 2, 1, 1, 5)
        gridlayout_data.addWidget(groupbox_somparam, 3, 0, 1, 6)
        gridlayout_data.addWidget(groupbox_snpsparam, 4, 0, 1, 6)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        # create and configure "pushbutton_execute"
        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Execute the process of the SOM imputation.')
        self.pushbutton_execute.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_execute.clicked.connect(self.pushbutton_execute_clicked)

        # create and configure "pushbutton_close"
        pushbutton_close = QPushButton('Close')
        pushbutton_close.setToolTip('Cancel the process of the SOM imputation and close the window.')
        pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        # create and configure "gridlayout_buttons"
        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 15)
        gridlayout_buttons.setColumnStretch(1, 1)
        gridlayout_buttons.setColumnStretch(2, 1)
        gridlayout_buttons.setColumnStretch(3, 0)
        gridlayout_buttons.addWidget(self.pushbutton_execute, 0, 1, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(pushbutton_close, 0, 2, alignment=Qt.AlignCenter)

        # create and configure "groupbox_buttons"
        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)

        # create and configure "gridlayout_central"
        gridlayout_central = QGridLayout()
        gridlayout_central.setRowStretch(0, 1)
        gridlayout_central.setRowStretch(1, 1)
        gridlayout_central.setRowStretch(2, 1)
        gridlayout_central.setRowStretch(3, 1)
        gridlayout_central.setRowStretch(4, 1)
        gridlayout_central.setColumnStretch(0, 0)
        gridlayout_central.setColumnStretch(1, 1)
        gridlayout_central.setColumnStretch(2, 0)
        gridlayout_central.addWidget(label_head, 0, 1)
        gridlayout_central.addWidget(QLabel(), 1, 1)
        gridlayout_central.addWidget(groupbox_data, 2, 1)
        gridlayout_central.addWidget(QLabel(), 3, 1)
        gridlayout_central.addWidget(groupbox_buttons, 4, 1)

        # create and configure "groupbox_central"
        groupbox_central = QGroupBox()
        groupbox_central.setLayout(gridlayout_central)

        # create and configure "vboxlayout"
        vboxlayout = QVBoxLayout(self)
        vboxlayout.addWidget(groupbox_central)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # set initial value in "lineedit_threads"
        self.lineedit_threads.setText('1')

        # populate data in "combobox_gtdb"
        self.combobox_gtdb_populate()

        # set initial value in "lineedit_file_format"
        self.lineedit_file_format.setText('')

        # set initial value in "lineedit_mdc"
        self.lineedit_mdc.setText('')

        # set initial value in "lineedit_file_path"
        self.lineedit_file_path.setText('')

        # set initial value in "lineedit_xdim"
        self.lineedit_xdim.setText('4')

        # set initial value in "lineedit_ydim"
        self.lineedit_ydim.setText('4')

        # set initial value in "lineedit_sigma"
        self.lineedit_sigma.setText('1.0')

        # set initial value in "lineedit_ilrate"
        self.lineedit_ilrate.setText('0.5')

        # set initial value in "lineedit_iterations"
        self.lineedit_iterations.setText('1000')

        # set initial value in "lineedit_mr2"
        self.lineedit_mr2.setText('0.1')

        # set initial value in "lineedit_snps"
        self.lineedit_snps.setText('5')

        # populate data in "combobox_gim_populate"
        self.combobox_gim_populate()

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # check "combobox_gtdb" when the index changed
        self.combobox_gtdb_currentIndexChanged()

        # check "lineedit_threads" when the editing finished
        if not self.lineedit_threads_editing_finished():
            OK = False

        # check "lineedit_file_format" when the editing finished
        if not self.lineedit_file_format_editing_finished():
            OK = False

        # check "lineedit_mdc_editing" when the editing finished
        if not self.lineedit_mdc_editing_finished():
            OK = False

        # check "lineedit_file_path" when the editing finished
        if not self.lineedit_file_path_editing_finished():
            OK = False

        # check "lineedit_xdim" when the editing finished
        if not self.lineedit_xdim_editing_finished():
            OK = False

        # check "lineedit_ydim" when the editing finished
        if not self.lineedit_ydim_editing_finished():
            OK = False

        # check "lineedit_sigma" when the editing finished
        if not self.lineedit_sigma_editing_finished():
            OK = False

        # check "lineedit_ilrate" when the editing finished
        if not self.lineedit_ilrate_editing_finished():
            OK = False

        # check "lineedit_iterations" when the editing finished
        if not self.lineedit_iterations_editing_finished():
            OK = False

        # check "lineedit_mr2" when the editing finished
        if not self.lineedit_mr2_editing_finished():
            OK = False

        # check "lineedit_snps" when the editing finished
        if not self.lineedit_snps_editing_finished():
            OK = False

        # check all inputs are OK
        if OK:
            self.parent.statusBar().showMessage('')
        else:
            self.parent.statusBar().showMessage('There are one or more inputs without data or with wrong values.')

        # enable "pushbutton_execute"
        if OK and self.lineedit_threads.text() != '' and self.combobox_gtdb.currentText() != '' and self.lineedit_file_format.text() != '' and self.lineedit_mdc.text() != '' and self.lineedit_file_path.text() != '' and self.lineedit_xdim.text() !='' and self.lineedit_ydim.text() and self.lineedit_sigma.text() and self.lineedit_ilrate.text() and self.lineedit_iterations.text() and self.lineedit_mr2.text() and self.lineedit_snps.text() and self.combobox_gim.currentText():
            self.pushbutton_execute.setEnabled(True)
        else:
            self.pushbutton_execute.setEnabled(False)

        # return the control variable
        return OK

    #---------------

    def lineedit_threads_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_threads"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_threads" is empty
        if self.lineedit_threads.text() == '':
            OK = False
            self.lineedit_threads.setStyleSheet('background-color: white')

        # chek if "lineedit_threads" is an integer number between 1 and the CPUs number in the computer
        elif self.lineedit_threads.text() != '' and not genlib.check_int(self.lineedit_threads.text(), minimum=1, maximum=os.cpu_count()):
            OK = False
            self.lineedit_threads.setStyleSheet('background-color: red')
            text = f'The value of threads number has to be an integer number between 1 and {os.cpu_count()} (threads available in the computer).'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_threads.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def combobox_gtdb_populate(self):
        '''
        Populate data in "combobox_gtdb".
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # get the imputation result directory
        imputation_result_subdir = f'{result_dir}/{genlib.get_result_imputation_subdir()}'
        if sys.platform.startswith('win32'):
            imputation_result_subdir = genlib.wsl_path_2_windows_path(imputation_result_subdir)

        # initialize the list of genetype database directories
        gtdb_dir_list = []

        # load the list of genetype database directories
        try:
            for entry in os.listdir(imputation_result_subdir):
                if os.path.isdir(f'{imputation_result_subdir}{os.sep}{entry}') and entry.startswith(genlib.get_gtdb_building_code()):
                    status_ok = os.path.isfile(genlib.get_status_ok(f'{imputation_result_subdir}{os.sep}{entry}'))
                    if status_ok:
                        gtdb_dir_list.append(entry)
            gtdb_dir_list.sort()
        except:    # pylint: disable=bare-except
            pass
        self.combobox_gtdb.addItems([''] + gtdb_dir_list)

        # simultate "combobox_gtdb" index has changed
        self.combobox_gtdb_currentIndexChanged()

    #---------------

    def combobox_gtdb_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_gtdb" has been selected.
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # when there is an item selected in "combobox_gtdb"
        if self.combobox_gtdb.currentText() != '':

            # set the genotype database directory
            gtdb_dir = f'{result_dir}/{genlib.get_result_imputation_subdir()}/{self.combobox_gtdb.currentText()}'

            # set the parameter file
            params_file = f'{gtdb_dir}/params.txt'
            if sys.platform.startswith('win32'):
                params_file = genlib.wsl_path_2_windows_path(params_file)

            # set the parameter dictionary
            params_dict = genlib.get_config_dict(params_file)

            # set "lineedit_file_format" value with its parameter value
            self.lineedit_file_format.setText(os.path.basename(params_dict['General parameters']['file_format']))

            # set "lineedit_mdc" value with its parameter value
            self.lineedit_mdc.setText(os.path.basename(params_dict['General parameters']['mdc']))

            # set "lineedit_file_path" value its with parameter value
            file_path = params_dict['General parameters']['file_path']
            if sys.platform.startswith('win32'):
                file_path = genlib.wsl_path_2_windows_path(file_path)
            self.lineedit_file_path.setText(file_path)

        # when there is not an item selected in "combobox_gtdb"
        else:

            # set widget values with null values
            self.lineedit_file_format.setText('')
            self.lineedit_mdc.setText('')
            self.lineedit_file_path.setText('')

    #---------------

    def lineedit_file_format_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_file_format"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_mdc_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_mdc"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_file_path_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_file_path"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_xdim_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_xdim"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_xdim" is empty
        if self.lineedit_xdim.text() == '':
            OK = False
            self.lineedit_xdim.setStyleSheet('background-color: white')

        # chek if "lineedit_xdim" is an integer number greater than or equal to 1
        elif self.lineedit_xdim.text() != '' and not genlib.check_int(self.lineedit_xdim.text(), minimum=1):
            OK = False
            self.lineedit_xdim.setStyleSheet('background-color: red')
            text = 'The value of X dimension has to be an integer number geater than 1.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_xdim.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def lineedit_ydim_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_ydim"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_ydim" is empty
        if self.lineedit_ydim.text() == '':
            OK = False
            self.lineedit_ydim.setStyleSheet('background-color: white')

        # chek if "lineedit_ydim" is an integer number greater than or equal to 1
        elif self.lineedit_ydim.text() != '' and not genlib.check_int(self.lineedit_ydim.text(), minimum=1):
            OK = False
            self.lineedit_ydim.setStyleSheet('background-color: red')
            text = 'The value of Y dimension has to be an integer number geater than 1.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_ydim.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def lineedit_sigma_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_sigma"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_sigma" is empty
        if self.lineedit_sigma.text() == '':
            OK = False
            self.lineedit_sigma.setStyleSheet('background-color: white')

        # chek if "lineedit_sigma" is a float number greater than or equal to 0.1
        elif self.lineedit_sigma.text() != '' and not genlib.check_float(self.lineedit_sigma.text(), minimum=0.1):
            OK = False
            self.lineedit_sigma.setStyleSheet('background-color: red')
            text = 'The value of sigma has to be a float number geater than 0.1.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_sigma.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def lineedit_ilrate_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_ilrate"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_ilrate" is empty
        if self.lineedit_ilrate.text() == '':
            OK = False
            self.lineedit_ilrate.setStyleSheet('background-color: white')

        # chek if "lineedit_ilrate" is a float number greater than or equal to 0.1
        elif self.lineedit_ilrate.text() != '' and not genlib.check_float(self.lineedit_ilrate.text(), minimum=0.1):
            OK = False
            self.lineedit_ilrate.setStyleSheet('background-color: red')
            text = 'The value of learning rate has to be a float number geater than 0.1.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_ilrate.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def lineedit_iterations_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_iterations"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_iterations" is empty
        if self.lineedit_iterations.text() == '':
            OK = False
            self.lineedit_iterations.setStyleSheet('background-color: white')

        # chek if "lineedit_iterations" is an integer number greater than or equal to 1
        elif self.lineedit_iterations.text() != '' and not genlib.check_int(self.lineedit_iterations.text(), minimum=1):
            OK = False
            self.lineedit_iterations.setStyleSheet('background-color: red')
            text = 'The value of maximum iterations # has to be an integer number geater than 1.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_iterations.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def lineedit_mr2_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_mr2"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_mr2" is empty
        if self.lineedit_mr2.text() == '':
            OK = False
            self.lineedit_mr2.setStyleSheet('background-color: white')

        # chek if "lineedit_mr2" is a float number greater than or equal to 0.001
        elif self.lineedit_mr2.text() != '' and not genlib.check_float(self.lineedit_mr2.text(), minimum=0.001):
            OK = False
            self.lineedit_mr2.setStyleSheet('background-color: red')
            text = 'The value of minimum r^2 has to be a float number geater than 0.001.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_mr2.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def lineedit_snps_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_snps"
        '''

        # initialize the control variable
        OK = True

        # chek if "lineedit_snps" is empty
        if self.lineedit_snps.text() == '':
            OK = False
            self.lineedit_snps.setStyleSheet('background-color: white')

        # chek if "lineedit_snps" is an integer number greater than or equal to 2
        elif self.lineedit_snps.text() != '' and not genlib.check_int(self.lineedit_snps.text(), minimum=2):
            OK = False
            self.lineedit_snps.setStyleSheet('background-color: red')
            text = 'The value of SNPs # has to be an integer number geater than 2.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        else:
            self.lineedit_snps.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def combobox_gim_populate(self):
        '''
        Populate data in "combobox_gim".
        '''


        # populate data in "combobox_gim"
        self.combobox_gim.addItems(self.gim_text_list)

        # simultate "combobox_gim" index has changed
        self.combobox_gim_currentIndexChanged()

    #---------------

    def combobox_gim_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_gim" has been selected.
        '''

        # check the content of inputs
        self.check_inputs()

    #---------------

    def pushbutton_search_clicked(self):
        '''
        Search and select a VCF file.
        '''

        # get the VCF file
        (file, _) = QFileDialog.getOpenFileName(self, f'{self.head} - Selection of the VCF file', os.path.expanduser('~'), 'VCF files (*.vcf);;All files (*)')
        self.lineedit_file_path.setText(file)

        # check the content of inputs
        self.check_inputs()

    #---------------

    def pushbutton_execute_clicked(self):
        '''
        Execute the process.
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # check the content of inputs
        OK = self.check_inputs()
        if not OK:
            text = 'Some input values are not OK.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        # confirm the process is executed
        if OK:
            text = 'The SOM imputation process is going to be run.\n\nAre you sure to continue?'
            botton = QMessageBox.question(self, self.title, text, buttons=QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)
            if botton == QMessageBox.No:
                OK = False

        # execute the process
        if OK:
            threads = self.lineedit_threads.text()
            gtdb_dir = f'{result_dir}/{genlib.get_result_imputation_subdir()}/{self.combobox_gtdb.currentText()}'
            file_format = self.lineedit_file_format.text()
            mdc = self.lineedit_mdc.text()
            file_path = self.lineedit_file_path.text()
            xdim = self.lineedit_xdim.text()
            ydim = self.lineedit_ydim.text()
            sigma = self.lineedit_sigma.text()
            ilrate = self.lineedit_ilrate.text()
            iterations = self.lineedit_iterations.text()
            mr2 = self.lineedit_mr2.text()
            snps = self.lineedit_snps.text()
            gim = self.gim_code_list[self.gim_text_list.index(self.combobox_gim.currentText())]
            process = dialogs.DialogProcess(self, self.head, self.run_som_imputation, threads, gtdb_dir, file_format, mdc, file_path, xdim, ydim, sigma, ilrate, iterations, mr2, snps, gim)
            process.exec()

        # close the windows
        if OK:
            self.pushbutton_close_clicked()

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.parent.current_subwindow = None
        self.close()
        self.parent.set_background_image()

   #---------------

    def run_som_imputation(self, process, threads, gtdb_dir, file_format, mdc, file_path, xdim, ydim, sigma, ilrate, iterations, mr2, snps, gim):
        '''
        Run a SOM imputation process.
        '''

        # initialize the control variable
        OK = True

        # warn that the log window does not have to be closed
        process.write('This process might take several minutes. Do not close this window, please wait!\n')

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # determine the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write('Determining the temporal directory ...\n')
            temp_dir = genlib.get_temp_dir()
            command = f'mkdir -p {temp_dir}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write(f'The directory path is {temp_dir}.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # determine the run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n'); process.show()
            process.write('Determining the run directory ...\n'); process.show()
            current_run_dir = genlib.get_current_run_dir(result_dir, genlib.get_result_imputation_subdir(), genlib.get_som_imputation_code())
            command = f'mkdir -p {current_run_dir}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write(f'The directory path is {current_run_dir}.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # build the SOM imputation script in the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            script_name = f'{genlib.get_som_imputation_code()}-process.sh'
            process.write(f'Building the script {script_name} ...\n')
            (OK, _) = self.build_som_imputation_script(temp_dir, script_name, current_run_dir, threads, gtdb_dir, file_format, mdc, file_path, xdim, ydim, sigma, ilrate, iterations, mr2, snps, gim)
            if OK:
                process.write('The file is built.\n')
            else:
                process.write('*** ERROR: The file could not be built.\n')

        # copy the SOM imputation script to the current run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Copying the script {script_name} to the directory {current_run_dir} ...\n')
            command = f'cp {temp_dir}/{script_name} {current_run_dir}; [ $? -eq 0 ] &&  exit 0 || exit 1'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The file is copied.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')

        # set run permision to the imputation script
        if OK and not sys.platform.startswith('win32'):
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Setting on the run permision of {script_name} ...\n')
            command = f'chmod u+x {current_run_dir}/{script_name}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The run permision is set.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # build the starter script in the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            starter_name = f'{genlib.get_som_imputation_code()}-process-starter.sh'
            process.write(f'Building the starter script {starter_name} ...\n')
            (OK, _) = genlib.build_starter(temp_dir, starter_name, script_name, current_run_dir)
            if OK:
                process.write('The file is built.\n')
            if not OK:
                process.write('***ERROR: The file could not be built.\n')

        # copy the starter script to the current run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Copying the starter {starter_name} to the directory {current_run_dir} ...\n')
            command = f'cp {temp_dir}/{starter_name} {current_run_dir}; [ $? -eq 0 ] &&  exit 0 || exit 1'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The file is copied.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')

        # set run permision to the starter script
        if OK and not sys.platform.startswith('win32'):
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Setting on the run permision of {starter_name} ...\n')
            command = f'chmod u+x {current_run_dir}/{starter_name}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The run permision is set.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # submit the starter
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Submitting the starter {starter_name} ...\n')
            command = f'{current_run_dir}/{starter_name} &'
            rc = genlib.run_command(command, process, is_script=True)
            if rc == 0:
                process.write('The script is submitted.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        process.write(f'{genlib.get_separator()}\n')
        process.write('You can close this window now.\n')

        # return the control variable
        return OK

   #---------------

    def build_som_imputation_script(self, directory, script_name, current_run_dir, threads, gtdb_dir, file_format, mdc, file_path, xdim, ydim, sigma, ilrate, iterations, mr2, snps, gim):
        '''
        Build the script to run the SOM imputation process.
        '''

        # initialize the control variable and error list
        OK = True
        error_list = []

        # get items from dictionary of application configuration
        app_dir = self.app_config_dict['Environment parameters']['app_dir']
        miniconda3_bin_dir = self.app_config_dict['Environment parameters']['miniconda3_bin_dir']

        # set the parameters file
        params_file = f'{current_run_dir}/params.txt'

        # set the genotype database file
        genotype_db = f'{gtdb_dir}/genotype.db'

        # set the VCF with missing data
        vcf_wmd_file = f'{gtdb_dir}/wmd.vcf'

        # set the imputed files
        vcf_imputed_file = f'{current_run_dir}/imputed.vcf'
        tab_imputed_file = f'{current_run_dir}/imputed.tsv'

        # set the file with imputation data
        imputation_data_file = f'{current_run_dir}/imputation_data.csv'

        # set the script path
        script_path = f'{directory}/{script_name}'

        # write the script
        try:
            with open(script_path, mode='w', encoding='iso-8859-1', newline='\n') as file_id:
                file_id.write( '#!/bin/bash\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'GTDB_DIR={gtdb_dir}\n')
                file_id.write(f'FILE_FORMAT={file_format}\n')
                file_id.write(f'MDC={mdc}\n')
                file_id.write(f'FILE_PATH="{file_path}"\n')
                file_id.write(f'VCF_WMD_FILE="{vcf_wmd_file}"\n')
                file_id.write(f'THREADS={threads}\n')
                file_id.write(f'XDIM={xdim}\n')
                file_id.write(f'YDIM={ydim}\n')
                file_id.write(f'SIGMA={sigma}\n')
                file_id.write(f'ILRATE={ilrate}\n')
                file_id.write(f'ITER={iterations}\n')
                file_id.write(f'MR2={mr2}\n')
                file_id.write( 'ESTIMATOR=ru\n')
                file_id.write(f'SNPS={snps}\n')
                file_id.write(f'GIM={gim}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'export PATH={miniconda3_bin_dir}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin\n')
                file_id.write( 'SEP="#########################################"\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'STATUS_DIR={genlib.get_status_dir(current_run_dir)}\n')
                file_id.write(f'SCRIPT_STATUS_OK={genlib.get_status_ok(current_run_dir)}\n')
                file_id.write(f'SCRIPT_STATUS_WRONG={genlib.get_status_wrong(current_run_dir)}\n')
                file_id.write( 'mkdir -p $STATUS_DIR\n')
                file_id.write( 'if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi\n')
                file_id.write( 'if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi\n')
                file_id.write(f'PARAMS_FILE={params_file}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function init\n')
                file_id.write( '{\n')
                file_id.write( '    INIT_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Script started at $FORMATTED_INIT_DATETIME."\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Parameters:"\n')
                file_id.write( '    echo "   gtdb_dir: $GTDB_DIR"\n')
                file_id.write( '    echo "   threads: $THREADS"\n')
                file_id.write( '    echo "   xdim: $XDIM - ydim: $YDIM"\n')
                file_id.write( '    echo "   sigma: $SIGMA - ilrate: $ILRATE - iter: $ITER"\n')
                file_id.write( '    echo "   mr2: $MR2 - snps: $SNPS - gim: $GIM"\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function activate_env_base\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Activating environment base ..."\n')
                file_id.write(f'    source {miniconda3_bin_dir}/activate\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "Environment is activated."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function save_params\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Saving parameters ..."\n')
                file_id.write( '    echo "[General parameters]" > $PARAMS_FILE\n')
                file_id.write( '    echo "threads = $THREADS" >> $PARAMS_FILE\n')
                file_id.write( '    echo "gtdb_dir = $GTDB_DIR" >> $PARAMS_FILE\n')
                file_id.write( '    echo "file_format = $FILE_FORMAT" >> $PARAMS_FILE\n')
                file_id.write( '    echo "mdc = $MDC" >> $PARAMS_FILE\n')
                file_id.write( '    echo "file_path = $FILE_PATH" >> $PARAMS_FILE\n')
                file_id.write( '    echo "vcf_wmd_file = $VCF_WMD_FILE" >> $PARAMS_FILE\n')
                file_id.write( '    echo "" >> $PARAMS_FILE\n')
                file_id.write( '    echo "[SOM parameters]" >> $PARAMS_FILE\n')
                file_id.write( '    echo "xdim = $XDIM" >> $PARAMS_FILE\n')
                file_id.write( '    echo "ydim = $YDIM" >> $PARAMS_FILE\n')
                file_id.write( '    echo "sigma = $SIGMA" >> $PARAMS_FILE\n')
                file_id.write( '    echo "ilrate = $ILRATE" >> $PARAMS_FILE\n')
                file_id.write( '    echo "iter = $ITER" >> $PARAMS_FILE\n')
                file_id.write( '    echo "" >> $PARAMS_FILE\n')
                file_id.write( '    echo "[SNPs selection parameters]" >> $PARAMS_FILE\n')
                file_id.write( '    echo "mr2 = $MR2" >> $PARAMS_FILE\n')
                file_id.write( '    echo "snps = $SNPS" >> $PARAMS_FILE\n')
                file_id.write( '    echo "gim = $GIM" >> $PARAMS_FILE\n')
                file_id.write( '    echo "Parameters are saved."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function run_som_imputation_process\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Processing the SOM imputation of {os.path.basename(vcf_wmd_file)} ..."\n')
                file_id.write( '    /usr/bin/time \\\n')
                file_id.write(f'        {app_dir}/impute-md-som.py \\\n')
                file_id.write( '            --threads=$THREADS \\\n')
                file_id.write(f'            --gtdb={genotype_db} \\\n')
                file_id.write(f'            --input_vcf={vcf_wmd_file} \\\n')
                file_id.write(f'            --output_vcf={vcf_imputed_file} \\\n')
                file_id.write(f'            --impdata={imputation_data_file} \\\n')
                file_id.write( '            --xdim=$XDIM \\\n')
                file_id.write( '            --ydim=$YDIM \\\n')
                file_id.write( '            --sigma=$SIGMA \\\n')
                file_id.write( '            --ilrate=$ILRATE \\\n')
                file_id.write( '            --iter=$ITER \\\n')
                file_id.write( '            --mr2=$MR2 \\\n')
                file_id.write( '            --estimator=$ESTIMATOR \\\n')
                file_id.write( '            --snps=$SNPS \\\n')
                file_id.write( '            --gim=$GIM \\\n')
                file_id.write( '            --verbose=N \\\n')
                file_id.write( '            --trace=N \\\n')
                file_id.write( '            --tvi=NONE\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error impute-md-som.py $RC; fi\n')
                file_id.write( '    echo "SOM imputation is ended."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function convert_vcf_to_tab\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Converting VCF file {os.path.basename(vcf_imputed_file)} to a file in tabular format ..."\n')
                file_id.write( '    /usr/bin/time \\\n')
                file_id.write(f'        {app_dir}/vcf2tab.py \\\n')
                file_id.write(f'            --vcf={vcf_imputed_file} \\\n')
                file_id.write(f'            --tab={tab_imputed_file} \\\n')
                file_id.write( '            --mdc=$MDC \\\n')
                file_id.write( '            --verbose=N \\\n')
                file_id.write( '            --trace=N \\\n')
                file_id.write( '            --tvi=NONE\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error vcf2tab.py $RC; fi\n')
                file_id.write( '    echo "File is converted."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function end\n')
                file_id.write( '{\n')
                file_id.write( '    END_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    calculate_duration\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    touch $SCRIPT_STATUS_OK\n')
                file_id.write( '    exit 0\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function manage_error\n')
                file_id.write( '{\n')
                file_id.write( '    END_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    calculate_duration\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "ERROR: $1 returned error $2"\n')
                file_id.write( '    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    touch $SCRIPT_STATUS_WRONG\n')
                file_id.write( '    exit 3\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function calculate_duration\n')
                file_id.write( '{\n')
                file_id.write( '    DURATION=`expr $END_DATETIME - $INIT_DATETIME`\n')
                file_id.write( '    HH=`expr $DURATION / 3600`\n')
                file_id.write( '    MM=`expr $DURATION % 3600 / 60`\n')
                file_id.write( '    SS=`expr $DURATION % 60`\n')
                file_id.write( '    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'init\n')
                file_id.write( 'activate_env_base\n')
                file_id.write( 'save_params\n')
                file_id.write( 'run_som_imputation_process\n')
                file_id.write( 'convert_vcf_to_tab\n')
                file_id.write( 'end\n')
        except Exception as e:
            error_list.append(f'*** EXCEPTION: "{e}".')
            error_list.append(f'*** ERROR: The file {script_path} is not created.')
            OK = False

        # return the control variable and error list
        return (OK, error_list)

#-------------------------------------------------------------------------------

class FormSOMImputationReview(QWidget):
    '''
    Class used to review a SOM imputation.
    '''

    #---------------

    def __init__(self, parent):
        '''
        Create a class instance.
        '''

        # save parameters in instance variables
        self.parent = parent

        # call the init method of the parent class
        super().__init__()

        # set the dimensions window
        self.window_height = self.parent.WINDOW_HEIGHT - 100
        self.window_width = self.parent.WINDOW_WIDTH - 50

        # set the head and title
        self.head = 'SOM imputation review'
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

        # get the dictionary of application configuration
        self.app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())

        # get the the code list and text list of genotype imputation method
        self.gim_code_list = genlib.get_genotype_imputation_method_code_list()
        self.gim_text_list = genlib.get_genotype_imputation_method_text_list()

        # build the graphic user interface of the window
        self.build_gui()

        # load initial data in inputs
        self.initialize_inputs()

        # check the content of inputs
        self.check_inputs()

        # show the window
        self.show()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        # set the width and height of the window
        self.setFixedSize(self.window_width, self.window_height)

        # move the window at center
        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        # get font metrics information
        fontmetrics = QFontMetrics(QApplication.font())

        # create and configure "label_head"
        label_head = QLabel(self.head, alignment=Qt.AlignCenter)
        label_head.setStyleSheet('font: bold 14px; color: black; background-color: lightGray; max-height: 30px')

        # create and configure "label_som_process"
        label_som_process = QLabel()
        label_som_process.setText('SOM process')
        label_som_process.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "combobox_som_process"
        self.combobox_som_process = QComboBox()
        self.combobox_som_process.setFixedWidth(fontmetrics.width('9'*20))
        self.combobox_som_process.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_som_process.currentIndexChanged.connect(self.check_inputs)

        # create and configure "label_gtdb"
        label_gtdb = QLabel()
        label_gtdb.setText('Genotype database')
        label_gtdb.setFixedWidth(fontmetrics.width('9'*16))

        # create and configure "lineedit_gtdb"
        self.lineedit_gtdb  = QLineEdit()
        self.lineedit_gtdb.setFixedWidth(fontmetrics.width('9'*20))
        self.lineedit_gtdb.editingFinished.connect(self.check_inputs)
        self.lineedit_gtdb.setReadOnly(True)

        # create and configure "label_file_format"
        label_file_format = QLabel()
        label_file_format.setText('File format')
        label_file_format.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_file_format"
        self.lineedit_file_format  = QLineEdit()
        self.lineedit_file_format.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_file_format.editingFinished.connect(self.check_inputs)
        self.lineedit_file_format.setReadOnly(True)

        # create and configure "label_mdc"
        label_mdc = QLabel()
        label_mdc.setText('MD char in tabular format')
        label_mdc.setFixedWidth(fontmetrics.width('9'*20))

        # create and configure "lineedit_mdc"
        self.lineedit_mdc  = QLineEdit()
        self.lineedit_mdc.setFixedWidth(fontmetrics.width('9'*10))
        self.lineedit_mdc.editingFinished.connect(self.check_inputs)
        self.lineedit_mdc.setReadOnly(True)

        # create and configure "label_file_path"
        label_file_path = QLabel()
        label_file_path.setText('File path')
        label_file_path.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "lineedit_file_path"
        self.lineedit_file_path  = QLineEdit()
        self.lineedit_file_path.editingFinished.connect(self.check_inputs)
        self.lineedit_file_path.setReadOnly(True)

        # create and configure "label_xdim"
        label_xdim = QLabel()
        label_xdim.setText('X dimension')
        label_xdim.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_xdim"
        self.lineedit_xdim  = QLineEdit()
        self.lineedit_xdim.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_xdim.editingFinished.connect(self.check_inputs)
        self.lineedit_xdim.setReadOnly(True)

        # create and configure "label_ydim"
        label_ydim = QLabel()
        label_ydim.setText('Y dimension')
        label_ydim.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_ydim"
        self.lineedit_ydim  = QLineEdit()
        self.lineedit_ydim.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_ydim.editingFinished.connect(self.check_inputs)
        self.lineedit_ydim.setReadOnly(True)

        # create and configure "label_sigma"
        label_sigma = QLabel()
        label_sigma.setText('Sigma')
        label_sigma.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_sigma"
        self.lineedit_sigma  = QLineEdit()
        self.lineedit_sigma.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_sigma.editingFinished.connect(self.check_inputs)
        self.lineedit_sigma.setReadOnly(True)

        # create and configure "label_ilrate"
        label_ilrate = QLabel()
        label_ilrate.setText('Learning rate')
        label_ilrate.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_ilrate"
        self.lineedit_ilrate  = QLineEdit()
        self.lineedit_ilrate.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_ilrate.editingFinished.connect(self.check_inputs)
        self.lineedit_ilrate.setReadOnly(True)

        # create and configure "label_iterations"
        label_iterations = QLabel()
        label_iterations.setText('Maximum iterations #')
        label_iterations.setFixedWidth(fontmetrics.width('9'*18))

        # create and configure "lineedit_iterations"
        self.lineedit_iterations  = QLineEdit()
        self.lineedit_iterations.setFixedWidth(fontmetrics.width('9'*22))
        self.lineedit_iterations.editingFinished.connect(self.check_inputs)
        self.lineedit_iterations.setReadOnly(True)

        # create and configure "label_empty"
        label_empty = QLabel()
        label_empty.setFixedWidth(fontmetrics.width('9'*3))

        # create and configure "gridlayout_somparam"
        gridlayout_somparam = QGridLayout()
        gridlayout_somparam.setRowMinimumHeight(0, 30)
        gridlayout_somparam.setRowMinimumHeight(1, 30)
        gridlayout_somparam.setColumnStretch(0, 1)
        gridlayout_somparam.setColumnStretch(1, 1)
        gridlayout_somparam.setColumnStretch(2, 1)
        gridlayout_somparam.setColumnStretch(3, 1)
        gridlayout_somparam.setColumnStretch(4, 1)
        gridlayout_somparam.setColumnStretch(5, 1)
        gridlayout_somparam.setColumnStretch(6, 2)
        gridlayout_somparam.setColumnStretch(7, 2)
        gridlayout_somparam.addWidget(label_xdim, 0, 0)
        gridlayout_somparam.addWidget(self.lineedit_xdim, 0, 1, alignment=Qt.AlignLeft)
        gridlayout_somparam.addWidget(label_empty, 0, 2)
        gridlayout_somparam.addWidget(label_ydim, 0, 3)
        gridlayout_somparam.addWidget(self.lineedit_ydim, 0, 4, alignment=Qt.AlignLeft)
        gridlayout_somparam.addWidget(label_empty, 0, 5)
        gridlayout_somparam.addWidget(label_sigma, 1, 0)
        gridlayout_somparam.addWidget(self.lineedit_sigma, 1, 1, alignment=Qt.AlignLeft)
        gridlayout_somparam.addWidget(label_ilrate, 1, 3)
        gridlayout_somparam.addWidget(self.lineedit_ilrate, 1, 4, alignment=Qt.AlignLeft)
        gridlayout_somparam.addWidget(label_iterations, 1, 6)
        gridlayout_somparam.addWidget(self.lineedit_iterations, 1, 7, alignment=Qt.AlignLeft)

        # create and configure "groupbox_somparam"
        groupbox_somparam = QGroupBox('SOM parameters')
        groupbox_somparam.setLayout(gridlayout_somparam)

        # create and configure "label_mr2"
        label_mr2 = QLabel()
        label_mr2.setText('Minimum r^2')
        label_mr2.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_mr2"
        self.lineedit_mr2  = QLineEdit()
        self.lineedit_mr2.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_mr2.editingFinished.connect(self.check_inputs)
        self.lineedit_mr2.setReadOnly(True)

        # create and configure "label_snps"
        label_snps = QLabel()
        label_snps.setText('SNPs #')
        label_snps.setFixedWidth(fontmetrics.width('9'*12))

        # create and configure "lineedit_snps"
        self.lineedit_snps  = QLineEdit()
        self.lineedit_snps.setFixedWidth(fontmetrics.width('9'*6))
        self.lineedit_snps.editingFinished.connect(self.check_inputs)
        self.lineedit_snps.setReadOnly(True)

        # create and configure "label_gim"
        label_gim = QLabel()
        label_gim.setText('Imputation method')
        label_gim.setFixedWidth(fontmetrics.width('9'*18))

        # create and configure "lineedit_gim"
        self.lineedit_gim = QLineEdit()
        self.lineedit_gim.setFixedWidth(fontmetrics.width('9'*22))
        self.lineedit_gim.editingFinished.connect(self.check_inputs)
        self.lineedit_gim.setReadOnly(True)

        # create and configure "gridlayout_snpsparam"
        gridlayout_snpsparam = QGridLayout()
        gridlayout_snpsparam.setColumnStretch(0, 1)
        gridlayout_snpsparam.setColumnStretch(1, 1)
        gridlayout_snpsparam.setColumnStretch(2, 1)
        gridlayout_snpsparam.setColumnStretch(3, 1)
        gridlayout_snpsparam.setColumnStretch(4, 1)
        gridlayout_snpsparam.setColumnStretch(5, 1)
        gridlayout_snpsparam.setColumnStretch(6, 2)
        gridlayout_snpsparam.setColumnStretch(7, 2)
        gridlayout_snpsparam.addWidget(label_mr2, 0, 0)
        gridlayout_snpsparam.addWidget(self.lineedit_mr2, 0, 1, alignment=Qt.AlignLeft)
        gridlayout_snpsparam.addWidget(label_empty, 0, 2)
        gridlayout_snpsparam.addWidget(label_snps, 0, 3)
        gridlayout_snpsparam.addWidget(self.lineedit_snps, 0, 4, alignment=Qt.AlignLeft)
        gridlayout_snpsparam.addWidget(label_empty, 0, 5)
        gridlayout_snpsparam.addWidget(label_gim, 0, 6)
        gridlayout_snpsparam.addWidget(self.lineedit_gim, 0, 7, alignment=Qt.AlignLeft)

        # create and configure "groupbox_snpsparam"
        groupbox_snpsparam = QGroupBox('SNPs selection parameters')
        groupbox_snpsparam.setLayout(gridlayout_snpsparam)

        # create and configure "gridlayout_data"
        gridlayout_data = QGridLayout()
        gridlayout_data.setRowMinimumHeight(0, 30)
        gridlayout_data.setRowMinimumHeight(1, 30)
        gridlayout_data.setRowMinimumHeight(2, 30)
        gridlayout_data.setRowMinimumHeight(3, 100)
        gridlayout_data.setRowMinimumHeight(4, 60)
        gridlayout_data.setColumnStretch(0,1)
        gridlayout_data.setColumnStretch(1,1)
        gridlayout_data.setColumnStretch(2,1)
        gridlayout_data.setColumnStretch(3,1)
        gridlayout_data.setColumnStretch(4,1)
        gridlayout_data.setColumnStretch(5,15)
        gridlayout_data.addWidget(label_som_process, 0, 0)
        gridlayout_data.addWidget(self.combobox_som_process, 0, 1, alignment=Qt.AlignLeft)
        gridlayout_data.addWidget(label_empty, 0, 2)
        gridlayout_data.addWidget(label_gtdb, 0, 3)
        gridlayout_data.addWidget(self.lineedit_gtdb, 0, 4, alignment=Qt.AlignLeft)
        gridlayout_data.addWidget(label_file_format, 1, 0)
        gridlayout_data.addWidget(self.lineedit_file_format, 1, 1)
        gridlayout_data.addWidget(label_empty, 1, 2)
        gridlayout_data.addWidget(label_mdc, 1, 3)
        gridlayout_data.addWidget(self.lineedit_mdc, 1, 4)
        gridlayout_data.addWidget(label_file_path, 2, 0)
        gridlayout_data.addWidget(self.lineedit_file_path, 2, 1, 1, 5)
        gridlayout_data.addWidget(groupbox_somparam, 3, 0, 1, 6)
        gridlayout_data.addWidget(groupbox_snpsparam, 4, 0, 1, 6)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        # create and configure "pushbutton_execute"
        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Review the process of the SOM imputation.')
        self.pushbutton_execute.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_execute.clicked.connect(self.pushbutton_execute_clicked)

        # create and configure "pushbutton_close"
        pushbutton_close = QPushButton('Close')
        pushbutton_close.setToolTip('Close the window.')
        pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        # create and configure "gridlayout_buttons"
        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 15)
        gridlayout_buttons.setColumnStretch(1, 1)
        gridlayout_buttons.setColumnStretch(2, 1)
        gridlayout_buttons.setColumnStretch(3, 0)
        gridlayout_buttons.addWidget(self.pushbutton_execute, 0, 1, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(pushbutton_close, 0, 2, alignment=Qt.AlignCenter)

        # create and configure "groupbox_buttons"
        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)

        # create and configure "gridlayout_central"
        gridlayout_central = QGridLayout()
        gridlayout_central.setRowStretch(0, 1)
        gridlayout_central.setRowStretch(1, 1)
        gridlayout_central.setRowStretch(2, 1)
        gridlayout_central.setRowStretch(3, 1)
        gridlayout_central.setRowStretch(4, 1)
        gridlayout_central.setColumnStretch(0, 0)
        gridlayout_central.setColumnStretch(1, 1)
        gridlayout_central.setColumnStretch(2, 0)
        gridlayout_central.addWidget(label_head, 0, 1)
        gridlayout_central.addWidget(QLabel(), 1, 1)
        gridlayout_central.addWidget(groupbox_data, 2, 1)
        gridlayout_central.addWidget(QLabel(), 3, 1)
        gridlayout_central.addWidget(groupbox_buttons, 4, 1)

        # create and configure "groupbox_central"
        groupbox_central = QGroupBox()
        groupbox_central.setLayout(gridlayout_central)

        # create and configure "vboxlayout"
        vboxlayout = QVBoxLayout(self)
        vboxlayout.addWidget(groupbox_central)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # populate data in "combobox_som_process"
        self.combobox_som_process_populate()

        # set initial value in "lineedit_gtdb"
        self.lineedit_gtdb.setText('')

        # set initial value in "lineedit_file_format"
        self.lineedit_file_format.setText('')

        # set initial value in "lineedit_mdc"
        self.lineedit_mdc.setText('')

        # set initial value in "lineedit_file_path"
        self.lineedit_file_path.setText('')

        # set initial value in "lineedit_xdim"
        self.lineedit_xdim.setText('')

        # set initial value in "lineedit_ydim"
        self.lineedit_ydim.setText('')

        # set initial value in "lineedit_sigma"
        self.lineedit_sigma.setText('')

        # set initial value in "lineedit_ilrate"
        self.lineedit_ilrate.setText('')

        # set initial value in "lineedit_iterations"
        self.lineedit_iterations.setText('')

        # set initial value in "lineedit_mr2"
        self.lineedit_mr2.setText('')

        # set initial value in "lineedit_snps"
        self.lineedit_snps.setText('')

        # set initial value in "lineedit_gim"
        self.lineedit_gim.setText('')

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # check "combobox_som_process" when the index changed
        self.combobox_som_process_currentIndexChanged()

        # check "lineedit_gtdb" when the editing finished
        if not self.lineedit_gtdb_editing_finished():
            OK = False

        # check "lineedit_file_format" when the editing finished
        if not self.lineedit_file_format_editing_finished():
            OK = False

        # check "lineedit_mdc" when the editing finished
        if not self.lineedit_mdc_editing_finished():
            OK = False

        # check "lineedit_file_path" when the editing finished
        if not self.lineedit_file_path_editing_finished():
            OK = False

        # check "lineedit_xdim" when the editing finished
        if not self.lineedit_xdim_editing_finished():
            OK = False

        # check "lineedit_ydim" when the editing finished
        if not self.lineedit_ydim_editing_finished():
            OK = False

        # check "lineedit_sigma" when the editing finished
        if not self.lineedit_sigma_editing_finished():
            OK = False

        # check "lineedit_ilrate" when the editing finished
        if not self.lineedit_ilrate_editing_finished():
            OK = False

        # check "lineedit_iterations" when the editing finished
        if not self.lineedit_iterations_editing_finished():
            OK = False

        # check "lineedit_mr2" when the editing finished
        if not self.lineedit_mr2_editing_finished():
            OK = False

        # check "lineedit_snps" when the editing finished
        if not self.lineedit_snps_editing_finished():
            OK = False

        # check "lineedit_gim" when the editing finished
        if not self.lineedit_gim_editing_finished():
            OK = False

        # check all inputs are OK
        if OK:
            self.parent.statusBar().showMessage('')
        else:
            self.parent.statusBar().showMessage('There are one or more inputs without data or with wrong values.')

        # enable "pushbutton_execute"
        if self.combobox_som_process.currentText() != '':
            self.pushbutton_execute.setEnabled(True)
        else:
            self.pushbutton_execute.setEnabled(False)

        # return the control variable
        return OK

    #---------------

    def combobox_som_process_populate(self):
        '''
        Populate data in "combobox_som_process".
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # get the imputation result directory
        imputation_result_subdir = f'{result_dir}/{genlib.get_result_imputation_subdir()}'
        if sys.platform.startswith('win32'):
            imputation_result_subdir = genlib.wsl_path_2_windows_path(imputation_result_subdir)

        # initialize the list of SOM process directories
        som_process_dir_list = []
        try:
            for entry in os.listdir(imputation_result_subdir):
                if os.path.isdir(f'{imputation_result_subdir}{os.sep}{entry}') and entry.startswith(genlib.get_som_imputation_code()):
                    status_ok = os.path.isfile(genlib.get_status_ok(f'{imputation_result_subdir}{os.sep}{entry}'))
                    if status_ok:
                        som_process_dir_list.append(entry)
            som_process_dir_list.sort()
        except:    # pylint: disable=bare-except
            pass
        self.combobox_som_process.addItems([''] + som_process_dir_list)

        # simultate "combobox_som_process" index has changed
        self.combobox_som_process_currentIndexChanged()

    #---------------

    def combobox_som_process_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_som_process" has been selected.
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # when there is an item selected in "combobox_som_process"
        if self.combobox_som_process.currentText() != '':

            # set the SOM process directory
            som_process_dir = f'{result_dir}/{genlib.get_result_imputation_subdir()}/{self.combobox_som_process.currentText()}'

            # set the parameter file
            params_file = f'{som_process_dir}/params.txt'
            if sys.platform.startswith('win32'):
                params_file = genlib.wsl_path_2_windows_path(params_file)

            # set the parameter dictionary
            params_dict = genlib.get_config_dict(params_file)

            # set "lineedit_gtdb" value with its parameter value
            gtdb_dir = params_dict['General parameters']['gtdb_dir']
            if sys.platform.startswith('win32'):
                gtdb_dir = genlib.wsl_path_2_windows_path(gtdb_dir)
            self.lineedit_gtdb.setText(os.path.basename(gtdb_dir))

            # set "lineedit_file_format" value with its parameter value
            file_format = params_dict['General parameters']['file_format']
            self.lineedit_file_format.setText(file_format)

            # set "lineedit_mdc" value with its parameter value
            mdc = params_dict['General parameters']['mdc']
            self.lineedit_mdc.setText(mdc)

            # set "lineedit_file_path" value with its parameter value
            file_path = params_dict['General parameters']['file_path']
            self.lineedit_file_path.setText(file_path)

            # set "lineedit_xdim" value with its parameter value
            xdim = params_dict['SOM parameters']['xdim']
            self.lineedit_xdim.setText(xdim)

            # set "lineedit_ydim" value with its parameter value
            ydim = params_dict['SOM parameters']['ydim']
            self.lineedit_ydim.setText(ydim)

            # set "lineedit_sigma" value with its parameter value
            sigma = params_dict['SOM parameters']['sigma']
            self.lineedit_sigma.setText(sigma)

            # set "lineedit_ilrate" value with its parameter value
            ilrate = params_dict['SOM parameters']['ilrate']
            self.lineedit_ilrate.setText(ilrate)

            # set "lineedit_iterations" value with its parameter value
            iterations = params_dict['SOM parameters']['iter']
            self.lineedit_iterations.setText(iterations)

            # set "lineedit_mr2" value with its parameter value
            mr2 = params_dict['SNPs selection parameters']['mr2']
            self.lineedit_mr2.setText(mr2)

            # set "lineedit_snps" value with its parameter value
            snps = params_dict['SNPs selection parameters']['snps']
            self.lineedit_snps.setText(snps)

            # set "lineedit_gim" value with its parameter value
            gim = self.gim_text_list[self.gim_code_list.index(params_dict['SNPs selection parameters']['gim'])]
            self.lineedit_gim.setText(gim)

        # when there is not an item selected in "combobox_som_process"
        else:

            # set widget values with null values
            self.lineedit_gtdb.setText('')
            self.lineedit_file_path.setText('')
            self.lineedit_file_format.setText('')
            self.lineedit_mdc.setText('')
            self.lineedit_xdim.setText('')
            self.lineedit_ydim.setText('')
            self.lineedit_sigma.setText('')
            self.lineedit_ilrate.setText('')
            self.lineedit_iterations.setText('')
            self.lineedit_mr2.setText('')
            self.lineedit_snps.setText('')
            self.lineedit_gim.setText('')

    #---------------

    def lineedit_gtdb_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_gtdb"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_file_format_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_file_format"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_mdc_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_mdc"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_file_path_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_file_path"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_xdim_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_xdim"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_ydim_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_ydim"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_sigma_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_sigma"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_ilrate_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_ilrate"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_iterations_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_iterations"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_mr2_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_mr2"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_snps_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_snps"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def lineedit_gim_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_gim"
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def pushbutton_execute_clicked(self):
        '''
        Execute the process.
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # set the file with imputation data
        imputation_data_file = f'{result_dir}/{genlib.get_result_imputation_subdir()}/{self.combobox_som_process.currentText()}/imputation_data.csv'
        if sys.platform.startswith('win32'):
            imputation_data_file = genlib.wsl_path_2_windows_path(imputation_data_file)

        # show de dialog with imputation
        head = f'{self.head}: {self.combobox_som_process.currentText()}'
        imputation_plot = DialogImputationPlot(self, head, imputation_data_file)
        imputation_plot.show()

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.parent.current_subwindow = None
        self.close()
        self.parent.set_background_image()

#-------------------------------------------------------------------------------

class DialogImputationPlot(QWidget):
    '''
    The class of the dialog to plot the result of an imputation process.
    '''

    #---------------

    # set the window dimensions
    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 800

    #---------------

    def __init__(self, parent, head, imputation_data_file):
        '''
        Create a class instance.
        '''

        # save parameters in instance variables
        self.parent = parent
        self.head = head
        self.imputation_data_file = imputation_data_file
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

        # call the init method of the parent class
        super().__init__()

        # get imputation data
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        (self.imputation_data_dict, self.seq_id_dict, self.sample_number) = self.get_imputation_data(self.imputation_data_file)
        self.seq_id_list = ['all'] + sorted(self.seq_id_dict.keys())
        QGuiApplication.restoreOverrideCursor()

        # build the graphic user interface of the window
        self.build_gui()

        # load initial data in inputs
        self.initialize_inputs()

        # check the content of inputs
        self.check_inputs()

        # show the window in maximized size
        self.showMaximized()

    #---------------

    @staticmethod
    def get_imputation_data(imputation_data_file):
        '''
        Get the imputation data.
        '''

        # initialize the dictionaries of imputation data and sequence identifications
        imputation_data_dict = {}
        seq_id_dict = {}

        # initialize the sample number
        sample_number = 0

        # open the file with imputation data
        try:
            imputation_data_file_id = open(imputation_data_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise genlib.ProgramException(e, 'F001', imputation_data_file)

        # initialize the record counter
        record_counter = 0

        # read the firt record of the file with imputation data
        record = imputation_data_file_id.readline()

        # while there are records in the file with imputation data
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # extract data
            # record format: seq_id;pos;reference_allele;alternative_alleles;sample_withmd_list_text;symbolic_sample_gt_list_text
            data_list = []
            begin = 0
            for end in [i for i, chr in enumerate(record) if chr == ';']:
                data_list.append(record[begin:end].strip())
                begin = end + 1
            data_list.append(record[begin:].strip('\n').strip())
            try:
                seq_id = data_list[0]
                pos = int(data_list[1])
                reference_allele = data_list[2]
                alternative_alleles = data_list[3]
                sample_withmd_list_text = data_list[4]
                symbolic_sample_gt_list_text = data_list[5]
            except Exception as e:
                raise genlib.ProgramException(e, 'F009', os.path.basename(imputation_data_file), record_counter)

            # add 1 to the occurrence counter of sequence identification
            seq_id_dict[seq_id] = seq_id_dict.get(seq_id, 0) + 1

            # set the list of samples with misssing data
            sample_withmd_list = [int(x) for x in sample_withmd_list_text.split('_')]

            # set the list of symbolic sample genotypes
            symbolic_sample_gt_list = list(symbolic_sample_gt_list_text)

            # add imputation data to the imputation data dictionary
            key = f'{seq_id}-{pos:0>10d}'
            imputation_data_dict[key] = {'seq_id': seq_id, 'pos': pos, 'reference_allele': reference_allele, 'alternative_alleles': alternative_alleles, 'sample_withmd_list': sample_withmd_list, 'symbolic_sample_gt_list': symbolic_sample_gt_list}

            # set the sample number
            if record_counter == 1:
                sample_number = len(symbolic_sample_gt_list)

            # read the next record of the imputation data
            record = imputation_data_file_id.readline()

        # clse the file of imputation data
        imputation_data_file_id.close()

        # return the dictionaries of imputation data and sequence identifications, and the sample number
        return imputation_data_dict, seq_id_dict, sample_number

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        # set the window title and icon
        self.setWindowTitle(f'{genlib.get_app_short_name()} - {self.head}')
        self.setWindowIcon(QIcon(genlib.get_app_image_file()))

        # set the window size
        # -- self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setMinimumSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # set the window flags
        # -- self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        # -- self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # move the window at center
        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        # get font metrics information
        fontmetrics = QFontMetrics(QApplication.font())

        # create and configure "label_head"
        label_head = QLabel(self.head, alignment=Qt.AlignCenter)
        label_head.setStyleSheet('font: bold 14px; color: black; background-color: lightGray; max-height: 30px')

        # create and configure "label_seq_id"
        label_seq_id = QLabel()
        label_seq_id.setText('Sequence')
        label_seq_id.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "combobox_seq_id"
        self.combobox_seq_id = QComboBox()
        self.combobox_seq_id.setFixedWidth(fontmetrics.width('9'*20))
        self.combobox_seq_id.setMaxVisibleItems(10)
        self.combobox_seq_id.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_seq_id.currentIndexChanged.connect(self.check_inputs)

        # create and configure "lineedit_seq_id"
        self.lineedit_seq_id  = QLineEdit()
        self.lineedit_seq_id.setFixedWidth(fontmetrics.width('9'*20))
        self.lineedit_seq_id.editingFinished.connect(self.check_inputs)

        # create and configure "pushbutton_locate"
        self.pushbutton_locate = QPushButton()
        self.pushbutton_locate.setIcon(QIcon(QPixmap('./image-magnifingglass.png')))
        self.pushbutton_locate.setToolTip('Locate the sequence.')
        self.pushbutton_locate.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_locate.clicked.connect(self.pushbutton_locate_clicked)

        # create and configure "gridlayout_data"
        gridlayout_data = QGridLayout()
        gridlayout_data.setColumnStretch(0, 1)
        gridlayout_data.setColumnStretch(1, 2)
        gridlayout_data.setColumnStretch(2, 2)
        gridlayout_data.setColumnStretch(3, 1)
        gridlayout_data.setColumnStretch(4, 15)
        gridlayout_data.addWidget(label_seq_id, 0, 0)
        gridlayout_data.addWidget(self.combobox_seq_id, 0, 1, alignment=Qt.AlignLeft)
        gridlayout_data.addWidget(self.lineedit_seq_id, 0, 2)
        gridlayout_data.addWidget(self.pushbutton_locate, 0, 3, alignment=Qt.AlignLeft)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        # create and configure "tablewidget_map"
        self.tablewidget_map = QTableWidget()
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            factor = int(0.8 * self.sample_number)
        elif  sys.platform.startswith('win32'):
            factor = int(0.4 * self.sample_number)
        self.tablewidget_map.setFixedWidth(fontmetrics.width('9'*factor))
        self.tablewidget_map.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablewidget_map.setStyleSheet('font: 1px')
        self.tablewidget_map.horizontalHeader().setVisible(False)
        self.tablewidget_map.verticalHeader().setVisible(False)
        self.tablewidget_map.setColumnCount(self.sample_number)
        for i in range(self.sample_number):
            self.tablewidget_map.setColumnWidth(i, 2)
        self.tablewidget_map.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.tablewidget_map.clicked.connect(self.tablewidget_map_clicked)

        # create and configure "tablewidget_detail"
        self.tablewidget_detail = QTableWidget()
        self.tablewidget_detail.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablewidget_detail.setStyleSheet('font: 10px')
        self.tablewidget_detail.horizontalHeader().setVisible(True)
        self.tablewidget_detail.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.column_name_list = ['Sequence', 'Position', 'Ref', 'Alt'] + [f'{i + 1}' for i in range(self.sample_number)]
        self.tablewidget_detail.setColumnCount(len(self.column_name_list))
        self.tablewidget_detail.setHorizontalHeaderLabels(self.column_name_list)
        self.tablewidget_detail.setColumnWidth(0, 125)
        self.tablewidget_detail.setColumnWidth(1, 60)
        self.tablewidget_detail.setColumnWidth(2, 25)
        self.tablewidget_detail.setColumnWidth(3, 25)
        for i in range(self.sample_number):
            self.tablewidget_detail.setColumnWidth(i + 4, 25)
        self.tablewidget_detail.verticalHeader().setVisible(True)
        self.tablewidget_detail.doubleClicked.connect(self.tablewidget_detail_doubleClicked)

        # create and configure "gridlayout_map"
        self.gridlayout_map = QGridLayout()
        self.gridlayout_map.setColumnStretch(0, 1)
        self.gridlayout_map.setColumnStretch(1, 15)
        self.gridlayout_map.addWidget(self.tablewidget_map, 0, 0)
        self.gridlayout_map.addWidget(self.tablewidget_detail, 0, 1)

        # create and configure "groupbox_map"
        groupbox_map = QGroupBox()
        groupbox_map.setObjectName('groupbox_data')
        groupbox_map.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_map.setLayout(self.gridlayout_map)

        # create and configure "label_genotype_imputed"
        label_genotype_imputed = QLabel()
        label_genotype_imputed.setText('genotype imputed')
        label_genotype_imputed.setFixedWidth(fontmetrics.width('9'*12))
        label_genotype_imputed.setStyleSheet('font: 10px; color: black; border: 1px solid gray; background-color: yellow; max-height: 15px')

        # create and configure "pushbutton_hide_show_map"
        self.pushbutton_hide_show_map = QPushButton('Hide map')
        self.pushbutton_hide_show_map.setToolTip('Hide the summary map of imputation.')
        self.pushbutton_hide_show_map.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_hide_show_map.clicked.connect(self.pushbutton_hide_show_map_clicked)

        # create and configure "pushbutton_prev_seq"
        self.pushbutton_prev_seq = QPushButton('Prev sequence')
        self.pushbutton_prev_seq.setToolTip('Show the next sequence.')
        self.pushbutton_prev_seq.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_prev_seq.clicked.connect(self.pushbutton_prev_seq_clicked)

        # create and configure "pushbutton_next_seq"
        self.pushbutton_next_seq = QPushButton('Next sequence')
        self.pushbutton_next_seq.setToolTip('Show the next sequence.')
        self.pushbutton_next_seq.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_next_seq.clicked.connect(self.pushbutton_next_seq_clicked)

        # create and configure "pushbutton_all_seqs"
        self.pushbutton_all_seqs = QPushButton('All sequences')
        self.pushbutton_all_seqs.setToolTip('Show all sequences.')
        self.pushbutton_all_seqs.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_all_seqs.clicked.connect(self.pushbutton_all_seqs_clicked)

        # create and configure "pushbutton_close"
        self.pushbutton_close = QPushButton('Close')
        self.pushbutton_close.setToolTip('Close the window.')
        self.pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        # create and configure "gridlayout_buttons"
        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 2)
        gridlayout_buttons.setColumnStretch(1, 15)
        gridlayout_buttons.setColumnStretch(2, 1)
        gridlayout_buttons.setColumnStretch(3, 1)
        gridlayout_buttons.setColumnStretch(4, 1)
        gridlayout_buttons.setColumnStretch(5, 1)
        gridlayout_buttons.setColumnStretch(6, 1)
        gridlayout_buttons.addWidget(label_genotype_imputed, 0, 0)
        gridlayout_buttons.addWidget(self.pushbutton_hide_show_map, 0, 2, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(self.pushbutton_prev_seq, 0, 3, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(self.pushbutton_next_seq, 0, 4, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(self.pushbutton_all_seqs, 0, 5, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(self.pushbutton_close, 0, 6, alignment=Qt.AlignCenter)

        # create and configure "groupbox_buttons"
        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)
        gridlayout_central = QGridLayout()
        gridlayout_central.setRowStretch(0, 1)
        gridlayout_central.setRowStretch(1, 10)
        gridlayout_central.setRowStretch(2, 1)
        gridlayout_central.setColumnStretch(0, 0)
        gridlayout_central.setColumnStretch(1, 1)
        gridlayout_central.setColumnStretch(2, 0)
        gridlayout_central.addWidget(groupbox_data, 0, 1)
        gridlayout_central.addWidget(groupbox_map, 1, 1)
        gridlayout_central.addWidget(groupbox_buttons, 2, 1)

        # create and configure "groupbox_central"
        groupbox_central = QGroupBox()
        groupbox_central.setLayout(gridlayout_central)

        # create and configure "vboxlayout"
        vboxlayout = QVBoxLayout(self)
        vboxlayout.addWidget(groupbox_central)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # populate data in "combobox_seq_id_populate"
        self.combobox_seq_id_populate()

        # load data in "tablewidget_map"
        self.tablewidget_map_load()

        # hide "tablewidget_map"
        self.tablewidget_map_hidden = False

        # simulate to click "pushbutton_hide_show_map"
        self.pushbutton_hide_show_map_clicked()
        if sys.platform.startswith('win32'):
            self.pushbutton_hide_show_map.setEnabled(False)


    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # load data in "tablewidget_detai"
        self.tablewidget_detail_load()

        # return the control variable
        return OK

    #---------------

    def combobox_seq_id_populate(self):
        '''
        Populate data in "combobox_seq_id".
        '''

        # populate data in "combobox_seq_id"
        self.combobox_seq_id.addItems(self.seq_id_list)

        # simultate "combobox_seq_id" index has changed
        self.combobox_seq_id_currentIndexChanged()

    #---------------

    def combobox_seq_id_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_combobox_seq_id" has been selected.
        '''

        # load data in "tablewidget_detail"
        self.tablewidget_detail_load()

    #---------------

    def pushbutton_locate_clicked(self):
        '''
        Locate the row of the first occurrence of a sequence in "tablewidget".
        '''

        # set 0 as the new index in "combobox_seq_id" (item "all")
        self.combobox_seq_id.setCurrentIndex(0)

        # process pending events and update the GUI
        QApplication.processEvents()

        # initialize the row number
        row = 0

        # initialize the control variable
        found = False

        # find the sequence identification in the sequence identification dictionary
        for seq_id in sorted(self.seq_id_dict.keys()):
            if seq_id == self.lineedit_seq_id.text():
                found = True
                break
            else:
                row += self.seq_id_dict[seq_id]

        # when the sequence identification is found
        if found:
            # move to the row number found
            self.tablewidget_detail.item(row, 0).setSelected(True)
            self.tablewidget_detail.scrollToItem(self.tablewidget_detail.item(row, 0))
        # when the sequence identification is not found
        else:
            # show an error message
            title = f'{self.head} - Locate a sequence'
            text = f'{self.lineedit_seq_id.text()} is not located.'
            QMessageBox.critical(self, title, text, buttons=QMessageBox.Ok)

    #---------------

    def tablewidget_map_load(self):
        '''
        Load the variant data in "tablewidget_map".
        '''

        # set the item counter of imputation data dictionary as the rows number of "tablewidget_map"
        self.tablewidget_map.setRowCount(len(self.imputation_data_dict))

        # move to top in "tablewidget_map"
        self.tablewidget_map.scrollToTop()

        # load data in "tablewidget_map"
        row = 0
        for key in sorted(self.imputation_data_dict.keys()):
            sample_withmd_list = self.imputation_data_dict[key]['sample_withmd_list']
            for col in range(self.sample_number):
                self.tablewidget_map.setItem(row, col, QTableWidgetItem())
                self.tablewidget_map.setRowHeight(row, 2)
                if col in sample_withmd_list:
                    self.tablewidget_map.item(row, col).setBackground(Qt.yellow)
                else:
                    self.tablewidget_map.item(row, col).setBackground(Qt.darkYellow)
            row += 1

        # resize "tablewidget_map" columns to their contents 
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            for col in range(self.sample_number):
                self.tablewidget_map.resizeColumnToContents(col)

    #---------------

    def tablewidget_map_clicked(self):
        '''
        Browse the variants corresponding to the sequence identification selected by a click.
        '''

        # get the row clicked
        for idx in self.tablewidget_map.selectionModel().selectedIndexes():
            row = idx.row()

        # set 0 as the new index in "combobox_seq_id" (item "all")
        self.combobox_seq_id.setCurrentIndex(0)

        # process pending events and update the GUI
        QApplication.processEvents()

        # find the index of "combobox_seq_id" corresponding to the sequence indentification in the row selected
        new_index = self.combobox_seq_id.findText(self.tablewidget_detail.item(row, 0).text())

        # set index of the sequence indentification in the row selected to the current index in "combobox_seq_id"
        self.combobox_seq_id.setCurrentIndex(new_index)

    #---------------

    def tablewidget_detail_load(self):
        '''
        Load the variant data in "tablewidget_detail".
        '''

        # when "all" in "combobox_seq_id" is selected
        if self.combobox_seq_id.currentText() == 'all':
            # disable "pushbutton_prev_seq" and "pushbutton_next_seq"
            self.pushbutton_prev_seq.setEnabled(False)
            self.pushbutton_next_seq.setEnabled(False)
        # when a specific sequence identification in "combobox_seq_id" is selected
        else:
            # enable "pushbutton_prev_seq" and "pushbutton_next_seq"
            self.pushbutton_prev_seq.setEnabled(True)
            self.pushbutton_next_seq.setEnabled(True)

        # clear previous data in "tablewidget_detail"
        self.tablewidget_detail.clearContents()

        # when "all" in "combobox_seq_id" is selected
        if self.combobox_seq_id.currentText() == 'all':
            # set the item counter of imputation data dictionary as the rows number of "tablewidget_detail"
            self.tablewidget_detail.setRowCount(len(self.imputation_data_dict))
        # when a specific sequence identification in "combobox_seq_id" is selected
        else:
            # set the item counter of the current sequence identification as the rows number of "tablewidget_detail"
            counter = self.seq_id_dict[self.combobox_seq_id.currentText()]
            self.tablewidget_detail.setRowCount(counter)

        # move to top in "tablewidget_detail"
        self.tablewidget_detail.scrollToTop()

        # load data in "tablewidget_detail"
        row = 0
        for key in sorted(self.imputation_data_dict.keys()):
            seq_id = self.imputation_data_dict[key]['seq_id']
            if self.combobox_seq_id.currentText() == 'all' or self.combobox_seq_id.currentText() == seq_id:
                self.tablewidget_detail.setItem(row, 0, QTableWidgetItem(seq_id))
                self.tablewidget_detail.item(row, 0).setBackground(QColor(245, 245, 245))
                pos = self.imputation_data_dict[key]['pos']
                self.tablewidget_detail.setItem(row, 1, QTableWidgetItem(str(pos)))
                self.tablewidget_detail.item(row, 1).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.tablewidget_detail.item(row, 1).setBackground(QColor(245, 245, 245))
                ref = self.imputation_data_dict[key]['reference_allele']
                self.tablewidget_detail.setItem(row, 2, QTableWidgetItem(ref))
                self.tablewidget_detail.item(row, 2).setTextAlignment(Qt.AlignCenter)
                self.tablewidget_detail.item(row, 2).setBackground(QColor(245, 245, 245))
                alt = self.imputation_data_dict[key]['alternative_alleles']
                self.tablewidget_detail.setItem(row, 3, QTableWidgetItem(alt))
                self.tablewidget_detail.item(row, 3).setTextAlignment(Qt.AlignCenter)
                self.tablewidget_detail.item(row, 3).setBackground(QColor(245, 245, 245))
                symbolic_sample_gt_list = self.imputation_data_dict[key]['symbolic_sample_gt_list']
                sample_withmd_list = self.imputation_data_dict[key]['sample_withmd_list']
                for col in range(self.sample_number):
                    self.tablewidget_detail.setItem(row, col + 4, QTableWidgetItem(symbolic_sample_gt_list[col]))
                    self.tablewidget_detail.item(row, col + 4).setTextAlignment(Qt.AlignCenter)
                    if col in sample_withmd_list:
                        self.tablewidget_detail.item(row, col + 4).setBackground(Qt.yellow)
                    else:
                        self.tablewidget_detail.item(row, col + 4).setBackground(Qt.darkYellow)
                row += 1

    #---------------

    def tablewidget_detail_doubleClicked(self):
        '''
        Browse the variants corresponding to the sequence identification selected by a double-click.
        '''

        # get the row and column double clicked
        for idx in self.tablewidget_detail.selectionModel().selectedIndexes():
            row = idx.row()
            col = idx.column()

        # when the column is the first one
        if col == 0:

            # find the index corresponding to the sequence identification double clicked
            index = self.combobox_seq_id.findText(self.tablewidget_detail.item(row, col).text())

            # the index corresponding to the sequence identification double clicked as current index
            self.combobox_seq_id.setCurrentIndex(index)

    #---------------

    def pushbutton_hide_show_map_clicked(self):
        '''
        Show or hide the summary map of imputation.
        '''

        # when "tablewidget_map" is hidden
        if self.tablewidget_map_hidden:

            # set the stretch factor to the first column of "gridlayout_map"
            self.gridlayout_map.setColumnStretch(0, 1)

            # show "tablewidget_map"
            self.tablewidget_map.show()
            self.tablewidget_map_hidden = False

            # set text in "pushbutton_hide_show_map"
            self.pushbutton_hide_show_map.setText('Hide map')
            self.pushbutton_hide_show_map.setToolTip('Hide the summary map of imputation.')

        # when "tablewidget_map" is shown
        else:

            # set the stretch factor to the first column of "gridlayout_map"
            self.gridlayout_map.setColumnStretch(0, 0)

            # hide "tablewidget_map"
            self.tablewidget_map.hide()
            self.tablewidget_map_hidden = True

            # set text in "pushbutton_hide_show_map"
            self.pushbutton_hide_show_map.setText('Show map')
            self.pushbutton_hide_show_map.setToolTip('Show the summary map of imputation.')

    #---------------

    def pushbutton_prev_seq_clicked(self):
        '''
        Show the variant data of previous sequence.
        '''

        # get the current index in "combobox_seq_id"
        index = self.combobox_seq_id.currentIndex()

        # get the new index
        min_index = 1
        new_index = index - 1 if index > min_index else min_index

        # set the new index in "combobox_seq_id"
        self.combobox_seq_id.setCurrentIndex(new_index)

    #---------------

    def pushbutton_next_seq_clicked(self):
        '''
        Show the variant data of next sequence.
        '''

        # get the current index in "combobox_seq_id"
        index = self.combobox_seq_id.currentIndex()

        # get the new index
        max_index = len(self.seq_id_list) - 1
        new_index = index + 1 if index < max_index else max_index

        # set the new index in "combobox_seq_id"
        self.combobox_seq_id.setCurrentIndex(new_index)

    #---------------

    def pushbutton_all_seqs_clicked(self):
        '''
        Show the variant data of all sequences.
        '''

        # set 0 as the new index in "combobox_seq_id" (item "all")
        self.combobox_seq_id.setCurrentIndex(0)

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.close()

    #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print(f'This file contains the classes related to imputation processes used in {genlib.get_app_long_name()}.')
    sys.exit(0)

#-------------------------------------------------------------------------------
