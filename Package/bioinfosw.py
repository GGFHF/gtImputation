#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=multiple-statements
# pylint: disable=too-many-lines

#-------------------------------------------------------------------------------

'''
This file contains the classes related to the bioninfo software installation of
Genotype Imputation (gtImputation).

This software has been developed by:

    Dpto. Sistemas y Recursos Naturales
    ETSI Montes, Forestal y del Medio Natural
    Universidad Politecnica de Madrid
    https://github.com/ggfhf/

Licence: GNU General Public Licence Version 3.
'''

#-------------------------------------------------------------------------------

import os
import sys

from PyQt5.QtCore import Qt                # pylint: disable=no-name-in-module
from PyQt5.QtGui import QCursor            # pylint: disable=no-name-in-module
from PyQt5.QtGui import QGuiApplication    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QComboBox      # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGroupBox      # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel         # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLineEdit      # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMessageBox    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QPushButton    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QVBoxLayout    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget        # pylint: disable=no-name-in-module

import genlib
import dialogs

#-------------------------------------------------------------------------------

class InstallBioinfoSoftware(QWidget):
    '''
    Class used to install bioinfo software.
    '''

    #---------------

    def __init__(self, parent, software_code):
        '''
        Create a class instance.
        '''

        self.parent = parent
        self.software_code = software_code

        super().__init__()

        if self.software_code == genlib.get_miniconda3_code():
            self.software_name = genlib.get_miniconda3_name()

        self.window_height = self.parent.WINDOW_HEIGHT - 100
        self.window_width = self.parent.WINDOW_WIDTH - 50

        self.head = f'Install {self.software_name} software'
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

        self.build_gui()
        self.initialize_inputs()
        self.check_inputs()

        self.show()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        self.setFixedSize(self.window_width, self.window_height)

        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        label_head = QLabel(self.head, alignment=Qt.AlignCenter)
        label_head.setStyleSheet('font: bold 14px; color: black; background-color: lightGray; max-height: 30px')

        label_version = QLabel()
        label_version.setText('Version')

        self.combobox_version_type = QComboBox()
        self.combobox_version_type.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_version_type.currentIndexChanged.connect(self.check_inputs)

        self.lineedit_version_id  = QLineEdit()
        self.lineedit_version_id.editingFinished.connect(self.check_inputs)

        gridlayout = QGridLayout()
        gridlayout.setColumnStretch(0,1)
        gridlayout.setColumnStretch(1,3)
        gridlayout.setColumnStretch(2,3)
        gridlayout.setColumnStretch(3,5)
        gridlayout.addWidget(label_version, 0, 0)
        gridlayout.addWidget(self.combobox_version_type, 0, 1)
        gridlayout.addWidget(self.lineedit_version_id, 0, 2)

        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout)

        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Execute the software installation.')
        self.pushbutton_execute.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_execute.clicked.connect(self.pushbutton_execute_clicked)

        pushbutton_close = QPushButton('Close')
        pushbutton_close.setToolTip('Cancel the software installation and close the window.')
        pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 10)
        gridlayout_buttons.setColumnStretch(1, 1)
        gridlayout_buttons.setColumnStretch(2, 1)
        gridlayout_buttons.addWidget(self.pushbutton_execute, 0, 1, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(pushbutton_close, 0, 2, alignment=Qt.AlignCenter)

        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)

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

        groupbox_central = QGroupBox()
        groupbox_central.setLayout(gridlayout_central)

        vboxlayout = QVBoxLayout(self)
        vboxlayout.addWidget(groupbox_central)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        self.combobox_version_type_populate()

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        OK = True

        if self.combobox_version_type.currentText() == 'last':
            self.lineedit_version_id.setText('')
            self.lineedit_version_id.setEnabled(False)
        elif self.combobox_version_type.currentText() == 'specific':
            self.lineedit_version_id.setEnabled(True)

        if self.combobox_version_type.currentText() == 'specific' and self.lineedit_version_id.text() == '':
            self.pushbutton_execute.setEnabled(False)
        else:
            self.pushbutton_execute.setEnabled(True)

        return OK

    #---------------

    def combobox_version_type_populate(self):
        '''
        Populate data in "combobox_version_type".
        '''

        version_type_list = ['last', 'specific']
        self.combobox_version_type.addItems(version_type_list)
        if self.software_code == genlib.get_miniconda3_code():
            self.combobox_version_type.setEnabled(False)

        self.combobox_version_type_currentIndexChanged()

    #---------------

    def combobox_version_type_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_version_type" has been selected.
        '''

        self.lineedit_version_id.setText('')
        if self.software_code == genlib.get_miniconda3_code():
            self.lineedit_version_id.setEnabled(False)

        self.check_inputs()

    #---------------

    def lineedit_version_id_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_version_id"
        '''

        OK = True

        return OK

    #---------------

    def pushbutton_execute_clicked(self):
        '''
        Execute the process.
        '''

        OK = self.check_inputs()
        if not OK:
            text = 'Some input values are not OK.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

        if self.software_code == genlib.get_miniconda3_code():
            text = f'{self.software_name} (Conda infrastructure) is going to be installed. All Conda packages previously installed will be lost and they have to be reinstalled.\n\nAre you sure to continue?'
        else:
            text = f'The {self.software_name} Conda package is going to be installed. The previous version will be lost, if it exists.\n\nAre you sure to continue?'
        botton = QMessageBox.question(self, self.title, text, buttons=QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)
        if botton == QMessageBox.No:
            OK = False

        if OK:

            if self.combobox_version_type.currentText() == 'last':
                version = 'last'
            elif self.combobox_version_type.currentText() == 'specific':
                version = self.lineedit_version_id.text()

            if self.software_code == genlib.get_miniconda3_code():
                process = dialogs.Process(self, self.head, self.install_miniconda3)
                process.exec()

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

    def install_miniconda3(self, process):
        '''
        Install the Miniconda3.
        '''

        OK = True

        app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())
        result_dir = app_config_dict['Environment parameters']['result_dir']

        process.write('This process might take several minutes. Do not close this window, please wait!\n')

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
            current_run_dir = genlib.get_current_run_dir(result_dir, genlib.get_result_installation_subdir(), genlib.get_miniconda3_code())
            command = f'mkdir -p {current_run_dir}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write(f'The directory path is {current_run_dir}.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # build the installation script in the temporal directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            script_name = f'{genlib.get_miniconda3_code()}-installation.sh'
            process.write(f'Building the installation script {script_name} ...\n')
            (OK, _) = self.build_miniconda3_installation_script(temp_dir, script_name, current_run_dir)
            if OK:
                process.write('The file is built.\n')
            else:
                process.write('*** ERROR: The file could not be built.\n')

        # copy the installation script to the current run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Copying the script {script_name} to the directory {current_run_dir} ...\n')
            command = f'cp {temp_dir}/{script_name} {current_run_dir}; [ $? -eq 0 ] &&  exit 0 || exit 1'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The file is copied.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')

        # set run permision to the installation script
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
            starter_name = f'{genlib.get_miniconda3_code()}-installation-starter.sh'
            process.write(f'Building the process starter {starter_name} ...\n')
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
            process.write(f'Submitting the process script {starter_name} ...\n')
            command = f'{current_run_dir}/{starter_name} &'
            rc = genlib.run_command(command, process, is_script=True)
            if rc == 0:
                process.write('The script is submitted.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        process.write(f'{genlib.get_separator()}\n')
        process.write('You can close this window now.\n')

        return OK

   #---------------

    def is_installed_miniconda3(self):
        '''
        Check if Miniconda3 is installed.
        '''

        OK = True
        error_list = []

        app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())

        if sys.platform.startswith('win32'):
            user = genlib.get_wsl_envvar('USER')
            wsl_distro_name = genlib.get_wsl_envvar('WSL_DISTRO_NAME')
            if user == genlib.get_na() or wsl_distro_name == genlib.get_na():
                error_list.append('*** ERROR: Miniconda 3 is not installed.\n')
                OK = False
            else:
                miniconda3_bin_dir = f'\\\\wsl$\\{wsl_distro_name}\\home\\{user}\\{genlib.get_miniconda_dir_in_wsl()[2:]}'
        else:
            miniconda3_bin_dir = app_config_dict['Environment parameters']['miniconda3_bin_dir']

        if OK:
            if not os.path.isdir(miniconda3_bin_dir):
                error_list.append('*** ERROR: Miniconda 3 is not installed.\n')
                OK = False

        return (OK, error_list)

   #---------------

    def build_miniconda3_installation_script(self, directory, script_name, current_run_dir):
        '''
        Build the Miniconda3 installation script.
        '''

        OK = True
        error_list = []

        app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())
        miniconda3_dir = app_config_dict['Environment parameters']['miniconda3_dir']
        miniconda3_bin_dir = app_config_dict['Environment parameters']['miniconda3_bin_dir']

        script_path = f'{directory}/{script_name}'
        try:
            with open(script_path, mode='w', encoding='iso-8859-1', newline='\n') as file_id:
                file_id.write( '#!/bin/bash\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin\n')
                file_id.write( 'SEP="#########################################"\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'STATUS_DIR={genlib.get_status_dir(current_run_dir)}\n')
                file_id.write(f'SCRIPT_STATUS_OK={genlib.get_status_ok(current_run_dir)}\n')
                file_id.write(f'SCRIPT_STATUS_WRONG={genlib.get_status_wrong(current_run_dir)}\n')
                file_id.write( 'mkdir -p $STATUS_DIR\n')
                file_id.write( 'if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi\n')
                file_id.write( 'if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function init\n')
                file_id.write( '{\n')
                file_id.write( '    INIT_DATETIME=`date +%s`\n')
                file_id.write( '    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Script started at $FORMATTED_INIT_DATETIME."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function remove_miniconda3_directory\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Removing {genlib.get_miniconda3_name()} directory ..."\n')
                file_id.write(f'    if [ -d {miniconda3_dir} ]; then\n')
                file_id.write(f'        rm -rf {miniconda3_dir}\n')
                file_id.write( '        echo "The directory is removed."\n')
                file_id.write( '    else\n')
                file_id.write( '        echo "The directory is not found."\n')
                file_id.write( '    fi\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function download_miniconda3_installation_file\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Downloading the {genlib.get_miniconda3_name()} installation file ..."\n')
                file_id.write( '    cd ~\n')
                file_id.write(f'    wget --quiet --output-document {genlib.get_miniconda3_name()}.sh {genlib.get_miniconda3_url()}\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error wget $RC; fi\n')
                file_id.write( '    echo\n')
                file_id.write( '    echo "The file is downloaded."\n')
                file_id.write(f'    chmod u+x {genlib.get_miniconda3_name()}.sh\n')
                file_id.write( '    echo "The run permision is set on."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_miniconda3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Installing {genlib.get_miniconda3_name()} to create Python 3 environment ..."\n')
                file_id.write( '    cd ~\n')
                file_id.write(f'    ./{genlib.get_miniconda3_name()}.sh -b -u -p {miniconda3_dir}\n')
                file_id.write( '    RC=$?\n')
                file_id.write(f'    if [ $RC -ne 0 ]; then manage_error {genlib.get_miniconda3_name()} $RC; fi\n')
                file_id.write( '    echo "Python 3 environment is created."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function remove_miniconda3_installation_file\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Removing the {genlib.get_miniconda3_name()} installation file ..."\n')
                file_id.write( '    cd ~\n')
                file_id.write(f'    rm -f {genlib.get_miniconda3_name()}.sh\n')
                file_id.write( '    echo "The file is removed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function add_channels\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Adding the channel defaults ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda config --add channels defaults\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The channel is added."\n')
                file_id.write( '    echo "Adding the channel bioconda ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda config --add channels bioconda\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The channel is added."\n')
                file_id.write( '    echo "Adding the channel conda-forge ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda config --add channels conda-forge\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The channel is added."\n')
                file_id.write( '    echo "Setting priority strict ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda config --set channel_priority strict\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The priority is set."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_numpy_python3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Installing package numpy in Python 3 environment ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda install --quiet --yes numpy\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The package is installed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_scipy_python3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Installing package scipy in Python 3 environment ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda install --quiet --yes scipy\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The package is installed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_sympy_python3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Installing package sympy in Python 3 environment ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda install --quiet --yes sympy\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The package is installed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_pandas_python3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Installing package pandas in Python 3 environment ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda install --quiet --yes sympy\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The package is installed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_matplotlib_python3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Installing package matplotlib in Python 3 environment ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda install --quiet --yes matplotlib\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The package is installed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_biopython_python3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Installing package biopython in Python 3 environment ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda install --quiet --yes biopython\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The package is installed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_requests_python3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Installing package requests in Python 3 environment ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda install --quiet --yes requests\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The package is installed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_mamba\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Installing mamba package ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda install --quiet --yes --channel conda-forge mamba\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The package is installed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_minisom\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Installing MiniSom ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/pip3 install MiniSom\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error pip3 $RC; fi\n')
                file_id.write( '    echo "The package is installed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function update_miniconda3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write( '    echo "Updating Python 3 environment ..."\n')
                file_id.write(f'    {miniconda3_bin_dir}/conda update --quiet --yes conda\n')
                file_id.write( '    RC=$?\n')
                file_id.write(f'    if [ $RC -ne 0 ]; then manage_error {genlib.get_miniconda3_name()} $RC; fi\n')
                file_id.write( '    echo "Python 3 environment is updated."\n')
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
                file_id.write( 'remove_miniconda3_directory\n')
                file_id.write( 'download_miniconda3_installation_file\n')
                file_id.write( 'install_miniconda3\n')
                file_id.write( 'remove_miniconda3_installation_file\n')
                file_id.write( 'add_channels\n')
                file_id.write( 'install_numpy_python3\n')
                file_id.write( 'install_scipy_python3\n')
                file_id.write( 'install_sympy_python3\n')
                file_id.write( 'install_pandas_python3\n')
                file_id.write( 'install_matplotlib_python3\n')
                file_id.write( 'install_biopython_python3\n')
                file_id.write( 'install_requests_python3\n')
                file_id.write( 'install_mamba\n')
                file_id.write( 'install_minisom\n')
                file_id.write( 'update_miniconda3\n')
                file_id.write( 'end\n')
        except Exception as e:
            error_list.append(f'*** EXCEPTION: "{e}".')
            error_list.append(f'*** ERROR: The file {script_path} can not be created.')
            OK = False

        return (OK, error_list)

   #---------------

    def install_bioconda_package_list(self, process, software_code, package_list):
        '''
        Install the Bioconda package list.
        '''

        OK = True

        app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())
        result_dir = app_config_dict['Environment parameters']['result_dir']

        process.write('This process might take several minutes. Do not close this window, please wait!\n')

        if OK:
            process.write(f'{genlib.get_separator()}\n')
            package_list_text = str(package_list).strip('[]').replace('\'','')
            process.write(f'Checking the Conda package list ({package_list_text}) installation requirements ...\n')

        # check if Miniconda3 is installed
        if OK:
            (OK, _) = self.is_installed_miniconda3()
            if not OK:
                process.write(f'*** ERROR: {genlib.get_miniconda3_name()} is not installed.\n')

        if OK:
            process.write('Installation requirements are OK.\n')

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
            current_run_dir = genlib.get_current_run_dir(result_dir, genlib.get_result_installation_subdir(), software_code)
            command = f'mkdir -p {current_run_dir}'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write(f'The directory path is {current_run_dir}.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        # build the installation script of bioconda package
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            script_name = f'{genlib.get_bioconda_code()}-installation.sh'
            process.write(f'Building the installation script {script_name} ...\n')
            (OK, _) = self.build_bioconda_package_installation_script(temp_dir, script_name, current_run_dir, package_list)
            if OK:
                process.write('The file is built.\n')
            if not OK:
                process.write('*** ERROR: The file could not be built.\n')

        # copy the installation script of bioconda package to the current run directory
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Copying the script {script_name} to the directory {current_run_dir} ...\n')
            command = f'cp {temp_dir}/{script_name} {current_run_dir}; [ $? -eq 0 ] &&  exit 0 || exit 1'
            rc = genlib.run_command(command, process, is_script=False)
            if rc == 0:
                process.write('The file is copied.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')

        # set run permision to the installation script of bioconda package
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

        # build the starter script
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            starter_name = f'{genlib.get_bioconda_code()}-installation-starter.sh'
            process.write(f'Building the process starter {starter_name} ...\n')
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

        # submit the script
        if OK:
            process.write(f'{genlib.get_separator()}\n')
            process.write(f'Submitting the process script {starter_name} ...\n')
            command = f'{current_run_dir}/{starter_name} &'
            rc = genlib.run_command(command, process, is_script=True)
            if rc == 0:
                process.write('The script is submitted.\n')
            else:
                process.write(f'*** ERROR: RC {rc} in command -> {command}\n')
                OK = False

        process.write(f'{genlib.get_separator()}\n')
        process.write('You can close this window now.\n')

        return OK

   #---------------

    def build_bioconda_package_installation_script(self, directory, script_name, current_run_dir, package_list):
        '''
        Build the Bioconda package installation script.
        '''

        OK = True
        error_list = []

        app_config_dict = genlib.get_config_dict(genlib.get_app_config_file())
        miniconda3_bin_dir = app_config_dict['Environment parameters']['miniconda3_bin_dir']

        script_path = f'{directory}/{script_name}'
        try:
            with open(script_path, mode='w', encoding='iso-8859-1', newline='\n') as script_file_id:
                script_file_id.write( '#!/bin/bash\n')
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write(f'export PATH={miniconda3_bin_dir}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin\n')
                script_file_id.write( 'SEP="#########################################"\n')
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write(f'STATUS_DIR={genlib.get_status_dir(current_run_dir)}\n')
                script_file_id.write(f'SCRIPT_STATUS_OK={genlib.get_status_ok(current_run_dir)}\n')
                script_file_id.write(f'SCRIPT_STATUS_WRONG={genlib.get_status_wrong(current_run_dir)}\n')
                script_file_id.write( 'mkdir -p $STATUS_DIR\n')
                script_file_id.write( 'if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi\n')
                script_file_id.write( 'if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi\n')
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write( 'function init\n')
                script_file_id.write( '{\n')
                script_file_id.write( '    INIT_DATETIME=`date +%s`\n')
                script_file_id.write( '    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                script_file_id.write( '    echo "$SEP"\n')
                script_file_id.write( '    echo "Script started at $FORMATTED_INIT_DATETIME."\n')
                script_file_id.write( '}\n')
                for package in package_list:
                    script_file_id.write( '#-------------------------------------------------------------------------------\n')
                    script_file_id.write(f'function remove_bioconda_package_{package[0]}\n')
                    script_file_id.write( '{\n')
                    script_file_id.write( '    echo "$SEP"\n')
                    script_file_id.write(f'    echo "Removing {genlib.get_bioconda_name()} package {package[0]} ..."\n')
                    script_file_id.write(f'    cd {miniconda3_bin_dir}\n')
                    script_file_id.write(f'    ./conda env remove --yes --quiet --name {package[0]}\n')
                    script_file_id.write( '    RC=$?\n')
                    script_file_id.write( '    if [ $RC -eq 0 ]; then\n')
                    script_file_id.write( '      echo "The old package is removed."\n')
                    script_file_id.write( '    else\n')
                    script_file_id.write( '      echo "The old package is not found."\n')
                    script_file_id.write( '    fi\n')
                    script_file_id.write( '}\n')
                    script_file_id.write( '#-------------------------------------------------------------------------------\n')
                    script_file_id.write(f'function install_bioconda_package_{package[0]}\n')
                    script_file_id.write( '{\n')
                    script_file_id.write( '    echo "$SEP"\n')
                    if package[1] == 'last':
                        script_file_id.write(f'    echo "Installing {genlib.get_bioconda_name()} package {package[0]} - last version ..."\n')
                        script_file_id.write(f'    cd {miniconda3_bin_dir}\n')
                        script_file_id.write(f'    ./mamba create --yes --quiet --name {package[0]} {package[0]}\n')
                        script_file_id.write( '    RC=$?\n')
                        script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                        script_file_id.write( '    echo "The package is installed."\n')
                    else:
                        script_file_id.write(f'    echo "Installing {genlib.get_bioconda_name()} package {package[0]} - version {package[1]} ..."\n')
                        script_file_id.write(f'    cd {miniconda3_bin_dir}\n')
                        script_file_id.write(f'    ./mamba create --yes --quiet --name {package[0]} {package[0]}={package[1]}\n')
                        script_file_id.write( '    RC=$?\n')
                        script_file_id.write( '    if [ $RC -ne 0 ]; then\n')
                        script_file_id.write(f'        echo "Installing {genlib.get_bioconda_name()} package {package[0]} - last version ..."\n')
                        script_file_id.write(f'        cd {miniconda3_bin_dir}\n')
                        script_file_id.write(f'        ./mamba create --yes --quiet --name {package[0]} {package[0]}\n')
                        script_file_id.write( '        RC=$?\n')
                        script_file_id.write( '        if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                        script_file_id.write( '    fi\n')
                        script_file_id.write( '    echo "The package is installed."\n')
                    script_file_id.write( '}\n')
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write( 'function end\n')
                script_file_id.write( '{\n')
                script_file_id.write( '    END_DATETIME=`date +%s`\n')
                script_file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                script_file_id.write( '    calculate_duration\n')
                script_file_id.write( '    echo "$SEP"\n')
                script_file_id.write( '    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
                script_file_id.write( '    echo "$SEP"\n')
                script_file_id.write( '    touch $SCRIPT_STATUS_OK\n')
                script_file_id.write( '    exit 0\n')
                script_file_id.write( '}\n')
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write( 'function manage_error\n')
                script_file_id.write( '{\n')
                script_file_id.write( '    END_DATETIME=`date +%s`\n')
                script_file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
                script_file_id.write( '    calculate_duration\n')
                script_file_id.write( '    echo "$SEP"\n')
                script_file_id.write( '    echo "ERROR: $1 returned error $2"\n')
                script_file_id.write( '    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
                script_file_id.write( '    echo "$SEP"\n')
                script_file_id.write( '    touch $SCRIPT_STATUS_WRONG\n')
                script_file_id.write( '    exit 3\n')
                script_file_id.write( '}\n')
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write( 'function calculate_duration\n')
                script_file_id.write( '{\n')
                script_file_id.write( '    DURATION=`expr $END_DATETIME - $INIT_DATETIME`\n')
                script_file_id.write( '    HH=`expr $DURATION / 3600`\n')
                script_file_id.write( '    MM=`expr $DURATION % 3600 / 60`\n')
                script_file_id.write( '    SS=`expr $DURATION % 60`\n')
                script_file_id.write( '    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`\n')
                script_file_id.write( '}\n')
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write( 'init\n')
                for package in package_list:
                    script_file_id.write(f'remove_bioconda_package_{package[0]}\n')
                    script_file_id.write(f'install_bioconda_package_{package[0]}\n')
                script_file_id.write( 'end\n')
        except Exception as e:
            error_list.append(f'*** EXCEPTION: "{e}".')
            error_list.append(f'*** ERROR: The file {script_path} can not be created.')
            OK = False

        return (OK, error_list)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print(f'This file contains the classes related to the bioninfo software installation of {genlib.get_app_long_name()}')
    sys.exit(0)

#-------------------------------------------------------------------------------
