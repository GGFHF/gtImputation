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

    GI en Desarrollo de Especies y Comunidades Leñosas (WooSp)
    Dpto. Sistemas y Recursos Naturales
    ETSI Montes, Forestal y del Medio Natural
    Universidad Politecnica de Madrid
    https://github.com/ggfhf/

Licence: GNU General Public Licence Version 3.
'''

#-------------------------------------------------------------------------------

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

class FormInstallBioinfoSoftware(QWidget):
    '''
    Class used to install bioinfo software.
    '''

    #---------------

    def __init__(self, parent, software_code, software_name):
        '''
        Create a class instance.
        '''

        # save parameters in instance variables
        self.parent = parent
        self.software_code = software_code
        self.software_name = software_name

        # call the init method of the parent class
        super().__init__()

        # set the dimensions window
        self.window_height = self.parent.WINDOW_HEIGHT - 100
        self.window_width = self.parent.WINDOW_WIDTH - 50

        # set the head and title
        self.head = f'Install {self.software_name} software'
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

        # create and configure "label_head"
        label_head = QLabel(self.head, alignment=Qt.AlignCenter)
        label_head.setStyleSheet('font: bold 14px; color: black; background-color: lightGray; max-height: 30px')

        # create and configure "label_version"
        label_version = QLabel()
        label_version.setText('Version')

        # create and configure "combobox_version_type"
        self.combobox_version_type = QComboBox()
        self.combobox_version_type.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_version_type.currentIndexChanged.connect(self.check_inputs)

        # create and configure "lineedit_version_id"
        self.lineedit_version_id  = QLineEdit()
        self.lineedit_version_id.editingFinished.connect(self.check_inputs)

        # create and configure "gridlayout"
        gridlayout = QGridLayout()
        gridlayout.setColumnStretch(0,1)
        gridlayout.setColumnStretch(1,3)
        gridlayout.setColumnStretch(2,3)
        gridlayout.setColumnStretch(3,5)
        gridlayout.addWidget(label_version, 0, 0)
        gridlayout.addWidget(self.combobox_version_type, 0, 1)
        gridlayout.addWidget(self.lineedit_version_id, 0, 2)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout)

        # create and configure "pushbutton_execute"
        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Execute the software installation.')
        self.pushbutton_execute.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_execute.clicked.connect(self.pushbutton_execute_clicked)

        # create and configure "pushbutton_close"
        pushbutton_close = QPushButton('Close')
        pushbutton_close.setToolTip('Cancel the software installation and close the window.')
        pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        # create and configure "gridlayout_buttons"
        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 10)
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

        # populate data in "combobox_version_type"
        self.combobox_version_type_populate()

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # check "combobox_version_type" and "lineedit_version_id"
        if self.combobox_version_type.currentText() == 'last':
            self.lineedit_version_id.setText('')
            self.lineedit_version_id.setEnabled(False)
        elif self.combobox_version_type.currentText() == 'specific':
            self.lineedit_version_id.setEnabled(True)

        # enable "pushbutton_execute"
        if self.combobox_version_type.currentText() == 'specific' and self.lineedit_version_id.text() == '':
            self.pushbutton_execute.setEnabled(False)
        else:
            self.pushbutton_execute.setEnabled(True)

        # return the control variable
        return OK

    #---------------

    def combobox_version_type_populate(self):
        '''
        Populate data in "combobox_version_type".
        '''

        # set the version type list
        version_type_list = ['last', 'specific']

        # load the version type list in "combobox_version_type"
        self.combobox_version_type.addItems(version_type_list)
        if self.software_code in [genlib.get_miniforge3_code(), genlib.get_gtimputation_env_code()]:
            self.combobox_version_type.setEnabled(False)

        # simultate "combobox_version_type" index has changed
        self.combobox_version_type_currentIndexChanged()

    #---------------

    def combobox_version_type_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_version_type" has been selected.
        '''

        # initialize "lineedit_version_id"
        self.lineedit_version_id.setText('')

        # disable "lineedit_version_id" when the item is Miniforge3
        if self.software_code in [genlib.get_miniforge3_code(), genlib.get_gtimputation_env_code()]:
            self.lineedit_version_id.setEnabled(False)

        # check the content of inputs
        self.check_inputs()

    #---------------

    def lineedit_version_id_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_version_id"
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

        # initialize the control variable
        OK = True

        # confirm the process is executed
        if self.software_code == genlib.get_miniforge3_code():
            text = f'{self.software_name} (Conda infrastructure) is going to be installed. All Conda packages previously installed will be lost and they have to be reinstalled.\n\nAre you sure to continue?'
        elif self.software_code == genlib.get_gtimputation_env_code():
            text = f'{self.software_name} is going to be installed. The previous version will be lost, if it exists.\n\nAre you sure to continue?'
        else:
            text = f'The {self.software_name} Conda package is going to be installed. The previous version will be lost, if it exists.\n\nAre you sure to continue?'
        botton = QMessageBox.question(self, self.title, text, buttons=QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)
        if botton == QMessageBox.No:
            OK = False

        # execute the process
        if OK:

            # get the version
            version = ''
            if self.combobox_version_type.currentText() == 'last':
                version = 'last'
            elif self.combobox_version_type.currentText() == 'specific':
                version = self.lineedit_version_id.text()

            # create and execute "DialogProcess" depending on the software code
            if self.software_code == genlib.get_miniforge3_code():
                process = dialogs.DialogProcess(self, self.head, self.install_miniforge3)
                process.exec()
            elif self.software_code == genlib.get_gtimputation_env_code():
                process = dialogs.DialogProcess(self, self.head, self.install_gtimputation_env)
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

    def install_miniforge3(self, process):
        '''
        Install the Miniforge3 on WSL.
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
            current_run_dir = genlib.get_current_run_dir(result_dir, genlib.get_result_installation_subdir(), genlib.get_miniforge3_code())
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
            script_name = f'{genlib.get_miniforge3_code()}-installation.sh'
            process.write(f'Building the installation script {script_name} ...\n')
            (OK, _) = self.build_miniforge3_installation_script(temp_dir, script_name, current_run_dir)
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
            starter_name = f'{genlib.get_miniforge3_code()}-installation-starter.sh'
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

        # warn that the log window can be closed
        process.write(f'{genlib.get_separator()}\n')
        process.write('You can close this window now.\n')

        # return the control variable
        return OK

   #---------------

    def build_miniforge3_installation_script(self, directory, script_name, current_run_dir):
        '''
        Build the Miniforge3 installation script on WSL.
        '''

        # initialize the control variable and error list
        OK = True
        error_list = []

        # get items from dictionary of application configuration
        app_dir = self.app_config_dict['Environment parameters']['app_dir']

        # get the Miniforge3 directory and its bin and condabin subdirectories
        miniforge3_dir = genlib.get_miniforge3_dir_in_wsl()
        miniforge3_condabin_dir = f'{miniforge3_dir}/condabin'

        # get the Conda environment data directory
        conda_environment_dir = '$HOME/.conda'

        # set the script path
        script_path = f'{directory}/{script_name}'

        # write the script
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
                file_id.write( 'function remove_miniforge3_dir\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Removing {genlib.get_miniforge3_name()} directory ..."\n')
                file_id.write(f'    if [ -d {miniforge3_dir} ]; then\n')
                file_id.write(f'        rm -rf {miniforge3_dir}\n')
                file_id.write( '        echo "The directory is removed."\n')
                file_id.write( '    else\n')
                file_id.write( '        echo "The directory is not found."\n')
                file_id.write( '    fi\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function remove_conda_environment_dir\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Removing {conda_environment_dir} directory ..."\n')
                file_id.write(f'    if [ -d {conda_environment_dir} ]; then\n')
                file_id.write(f'        rm -rf {conda_environment_dir}\n')
                file_id.write( '        echo "The directory is removed."\n')
                file_id.write( '    else\n')
                file_id.write( '        echo "The directory is not found."\n')
                file_id.write( '    fi\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function download_miniforge3_installation_file\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Downloading the {genlib.get_miniforge3_name()} installation file ..."\n')
                file_id.write( '    cd ~\n')
                file_id.write(f'    wget --quiet --output-document {genlib.get_miniforge3_name()}.sh {genlib.get_miniforge3_url()}\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error wget $RC; fi\n')
                file_id.write( '    echo\n')
                file_id.write( '    echo "The file is downloaded."\n')
                file_id.write(f'    chmod u+x {genlib.get_miniforge3_name()}.sh\n')
                file_id.write( '    echo "The run permision is set on."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function install_miniforge3\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Installing {genlib.get_miniforge3_name()} to create environment base ..."\n')
                file_id.write( '    cd ~\n')
                file_id.write(f'    ./{genlib.get_miniforge3_name()}.sh -b -u -p {miniforge3_dir}\n')
                file_id.write( '    RC=$?\n')
                file_id.write(f'    if [ $RC -ne 0 ]; then manage_error {genlib.get_miniforge3_name()} $RC; fi\n')
                file_id.write( '    echo "Environment is created."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function remove_miniforge3_installation_file\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Removing the {genlib.get_miniforge3_name()} installation file ..."\n')
                file_id.write( '    cd ~\n')
                file_id.write(f'    rm -f {genlib.get_miniforge3_name()}.sh\n')
                file_id.write( '    echo "The file is removed."\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function add_channels\n')
                file_id.write( '{\n')
                file_id.write( '    echo "Adding the channel bioconda ..."\n')
                file_id.write(f'    {miniforge3_condabin_dir}/conda config --add channels bioconda\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The channel is added."\n')
                file_id.write( '    echo "Adding the channel conda-forge ..."\n')
                file_id.write(f'    {miniforge3_condabin_dir}/conda config --add channels conda-forge\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The channel is added."\n')
                file_id.write( '    echo "Setting priority strict ..."\n')
                file_id.write(f'    {miniforge3_condabin_dir}/conda config --set channel_priority strict\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The priority is set."\n')
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
                file_id.write( 'remove_miniforge3_dir\n')
                file_id.write( 'remove_conda_environment_dir\n')
                file_id.write( 'download_miniforge3_installation_file\n')
                file_id.write( 'install_miniforge3\n')
                file_id.write( 'remove_miniforge3_installation_file\n')
                file_id.write( 'add_channels\n')
                file_id.write( 'end\n')
        except Exception as e:
            error_list.append(f'*** EXCEPTION: "{e}".')
            error_list.append(f'*** ERROR: The file {script_path} can not be created.')
            OK = False

        # return the control variable and error list
        return (OK, error_list)

   #---------------

    def install_gtimputation_env(self, process):
        '''
        Install the gtImputation environment on WSL.
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
            current_run_dir = genlib.get_current_run_dir(result_dir, genlib.get_result_installation_subdir(), genlib.get_gtimputation_env_code())
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
            script_name = f'{genlib.get_gtimputation_env_code()}-installation.sh'
            process.write(f'Building the installation script {script_name} ...\n')
            (OK, _) = self.build_gtimputation_env_installation_script(temp_dir, script_name, current_run_dir)
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
            starter_name = f'{genlib.get_gtimputation_env_code()}-installation-starter.sh'
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

        # warn that the log window can be closed
        process.write(f'{genlib.get_separator()}\n')
        process.write('You can close this window now.\n')

        # return the control variable
        return OK

   #---------------

    def build_gtimputation_env_installation_script(self, directory, script_name, current_run_dir):
        '''
        Build the gtImputation environment creation script on WSL.
        '''

        # initialize the control variable and error list
        OK = True
        error_list = []

        # get items from dictionary of application configuration
        app_dir = self.app_config_dict['Environment parameters']['app_dir']

        # get the Miniforge3 directory and its bin and condabin subdirectories
        miniforge3_dir = genlib.get_miniforge3_dir_in_wsl()
        miniforge3_condabin_dir = f'{miniforge3_dir}/condabin'

        # get the YML file to create the gtImputation environment
        gtimputation_yml_file = f'{app_dir}/{genlib.get_yml_dir()}/{genlib.get_gtimputation_yml_file()}'

        # set the script path
        script_path = f'{directory}/{script_name}'

        # write the script
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
                file_id.write( 'function remove_gtimputation_env\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Removing the {genlib.get_app_short_name()} environment ..."\n')
                file_id.write(f'    {miniforge3_condabin_dir}/conda env remove --yes --quiet --name {genlib.get_gtimputation_env_code()}\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -eq 0 ]; then\n')
                file_id.write( '      echo "The old environment is removed."\n')
                file_id.write( '    else\n')
                file_id.write( '      echo "The old environment is not found."\n')
                file_id.write( '    fi\n')
                file_id.write( '}\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write( 'function create_gtimputation_env\n')
                file_id.write( '{\n')
                file_id.write( '    echo "$SEP"\n')
                file_id.write(f'    echo "Creating the {genlib.get_app_short_name()} environment ..."\n')
                file_id.write(f'    {miniforge3_condabin_dir}/conda env create --yes --quiet --name {genlib.get_gtimputation_env_code()} --file {gtimputation_yml_file}\n')
                file_id.write( '    RC=$?\n')
                file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                file_id.write( '    echo "The environment is created."\n')
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
                file_id.write( 'remove_gtimputation_env\n')
                file_id.write( 'create_gtimputation_env\n')
                file_id.write( 'end\n')
        except Exception as e:
            error_list.append(f'*** EXCEPTION: "{e}".')
            error_list.append(f'*** ERROR: The file {script_path} can not be created.')
            OK = False

        # return the control variable and error list
        return (OK, error_list)

   #---------------

    def install_bioconda_package_list(self, process, software_code, package_list):
        '''
        Install the Bioconda package list.
        '''

        # initialize the control variable
        OK = True

        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        process.write('This process might take several minutes. Do not close this window, please wait!\n')

        if OK:
            process.write(f'{genlib.get_separator()}\n')
            package_list_text = str(package_list).strip('[]').replace('\'', '')
            process.write(f'Checking the Conda package list ({package_list_text}) installation requirements ...\n')

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

        # return the control variable
        return OK

   #---------------

    def build_bioconda_package_installation_script(self, directory, script_name, current_run_dir, package_list):
        '''
        Build the Bioconda package installation script.
        '''

        # initialize the control variable and error list
        OK = True
        error_list = []

        # get the Miniforge3 directory and its bin and condabin subdirectories
        miniforge3_dir = ''
        if sys.platform.startswith('win32'):
            miniforge3_dir = genlib.get_miniforge3_dir_in_wsl()
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            miniforge3_dir = genlib.get_miniforge3_current_dir()
        miniforge3_bin_dir = f'{miniforge3_dir}/bin'
        miniforge3_condabin_dir = f'{miniforge3_dir}/condabin'

        # set the script path
        script_path = f'{directory}/{script_name}'

        # write the script
        try:
            with open(script_path, mode='w', encoding='iso-8859-1', newline='\n') as file_id:
                file_id.write( '#!/bin/bash\n')
                file_id.write( '#-------------------------------------------------------------------------------\n')
                file_id.write(f'export PATH={miniforge3_bin_dir}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin\n')
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
                for package in package_list:
                    file_id.write( '#-------------------------------------------------------------------------------\n')
                    file_id.write(f'function remove_bioconda_package_{package[0]}\n')
                    file_id.write( '{\n')
                    file_id.write( '    echo "$SEP"\n')
                    file_id.write(f'    echo "Removing {genlib.get_bioconda_name()} package {package[0]} ..."\n')
                    file_id.write(f'    {miniforge3_condabin_dir}/conda env remove --yes --quiet --name {package[1]}\n')
                    file_id.write( '    RC=$?\n')
                    file_id.write( '    if [ $RC -eq 0 ]; then\n')
                    file_id.write( '      echo "The old package is removed."\n')
                    file_id.write( '    else\n')
                    file_id.write( '      echo "The old package is not found."\n')
                    file_id.write( '    fi\n')
                    file_id.write( '}\n')
                    file_id.write( '#-------------------------------------------------------------------------------\n')
                    file_id.write(f'function install_bioconda_package_{package[0]}\n')
                    file_id.write( '{\n')
                    file_id.write( '    echo "$SEP"\n')
                    if package[2] == 'last':
                        file_id.write(f'    echo "Installing {genlib.get_bioconda_name()} package {package[0]} - last version ..."\n')
                        file_id.write(f'    {miniforge3_condabin_dir}/conda create --yes --quiet --name {package[1]} {package[0]}\n')
                        file_id.write( '    RC=$?\n')
                        file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                        file_id.write( '    echo "The package is installed."\n')
                    else:
                        file_id.write(f'    echo "Installing {genlib.get_bioconda_name()} package {package[0]} - version {package[2]} ..."\n')
                        file_id.write(f'    {miniforge3_condabin_dir}/conda create --yes --quiet --name {package[1]} {package[0]}={package[2]}\n')
                        file_id.write( '    RC=$?\n')
                        file_id.write( '    if [ $RC -ne 0 ]; then\n')
                        file_id.write(f'        echo "Installing {genlib.get_bioconda_name()} package {package[0]} - last version ..."\n')
                        file_id.write(f'        {miniforge3_condabin_dir}/conda create --yes --quiet --name {package[1]} {package[0]}\n')
                        file_id.write( '        RC=$?\n')
                        file_id.write( '        if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                        file_id.write( '    fi\n')
                        file_id.write( '    echo "The package is installed."\n')
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
                for package in package_list:
                    file_id.write(f'remove_bioconda_package_{package[0]}\n')
                    file_id.write(f'install_bioconda_package_{package[0]}\n')
                file_id.write( 'end\n')
        except Exception as e:
            error_list.append(f'*** EXCEPTION: "{e}".')
            error_list.append(f'*** ERROR: The file {script_path} can not be created.')
            OK = False

        # return the control variable and error list
        return (OK, error_list)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print(f'This file contains the classes related to the bioninfo software installation of {genlib.get_app_long_name()}')
    sys.exit(0)

#-------------------------------------------------------------------------------
