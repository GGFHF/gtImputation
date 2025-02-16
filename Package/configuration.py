#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=multiple-statements
# pylint: disable=too-many-lines

#-------------------------------------------------------------------------------

'''
This file contains the classes related to the configuration of
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
import pathlib
import sys

from PyQt5.QtCore import Qt                # pylint: disable=no-name-in-module
from PyQt5.QtGui import QCursor            # pylint: disable=no-name-in-module
from PyQt5.QtGui import QFont              # pylint: disable=no-name-in-module
from PyQt5.QtGui import QGuiApplication    # pylint: disable=no-name-in-module
from PyQt5.QtGui import QTextCursor        # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QFileDialog    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGroupBox      # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel         # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLineEdit      # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMessageBox    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QPushButton    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QTextEdit      # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QVBoxLayout    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget        # pylint: disable=no-name-in-module

import genlib

#-------------------------------------------------------------------------------

class FormRecreateConfigFile(QWidget):
    '''
    Class used to recreate the gtImputation config file.
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
        self.head = f'Recreate {genlib.get_app_short_name()} config file'
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

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

        # create and configure "label_gtdb_dir"
        label_gtdb_dir = QLabel()
        label_gtdb_dir.setText('Genotype database directory')

        # create and configure "lineedit_gtdb_dir"
        self.lineedit_gtdb_dir  = QLineEdit()
        self.lineedit_gtdb_dir.editingFinished.connect(self.check_inputs)

        # create and configure "pushbutton_search_gtdb_dir"
        pushbutton_search_gtdb_dir = QPushButton('Search ...')
        pushbutton_search_gtdb_dir.setToolTip('Search and select the genotype database directory.')
        pushbutton_search_gtdb_dir.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_search_gtdb_dir.clicked.connect(self.pushbutton_search_gtdb_dir_clicked)

        # create and configure "label_result_dir"
        label_result_dir = QLabel()
        label_result_dir.setText('Result directory')

        # create and configure "lineedit_result_dir"
        self.lineedit_result_dir = QLineEdit()
        self.lineedit_result_dir.editingFinished.connect(self.check_inputs)

        # create and configure "pushbutton_search_result_dir"
        pushbutton_search_result_dir = QPushButton('Search ...')
        pushbutton_search_result_dir.setToolTip('Search and select the result directory.')
        pushbutton_search_result_dir.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_search_result_dir.clicked.connect(self.pushbutton_search_result_dir_clicked)

        # create and configure "gridlayout_data"
        gridlayout_data = QGridLayout()
        gridlayout_data.setRowMinimumHeight(0, 60)
        gridlayout_data.setRowMinimumHeight(1, 60)
        gridlayout_data.setRowMinimumHeight(2, 60)
        gridlayout_data.setColumnStretch(0,1)
        gridlayout_data.setColumnStretch(1,15)
        gridlayout_data.setColumnStretch(2,2)
        gridlayout_data.setColumnStretch(3,0)
        gridlayout_data.addWidget(label_gtdb_dir, 0, 0)
        gridlayout_data.addWidget(self.lineedit_gtdb_dir, 0, 1)
        gridlayout_data.addWidget(pushbutton_search_gtdb_dir, 0, 2)
        gridlayout_data.addWidget(label_result_dir, 1, 0)
        gridlayout_data.addWidget(self.lineedit_result_dir, 1, 1)
        gridlayout_data.addWidget(pushbutton_search_result_dir, 1, 2)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        # create and configure "pushbutton_execute"
        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Execute the creation of the config file.')
        self.pushbutton_execute.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_execute.clicked.connect(self.pushbutton_execute_clicked)

        # create and configure "pushbutton_close"
        pushbutton_close = QPushButton('Close')
        pushbutton_close.setToolTip('Cancel the creation of the config file and close the window.')
        pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        # create and configure "pushbutton_close"
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

        # get home directory
        home_dir = str(pathlib.Path.home())

        # set initial value in "lineedit_gtdb_dir"
        self.lineedit_gtdb_dir.setText(f'{home_dir}{os.sep}{genlib.get_gtdb_dir()}')

        # set initial value in "lineedit_result_dir"
        self.lineedit_result_dir.setText(f'{home_dir}{os.sep}{genlib.get_result_dir()}')

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # check "lineedit_gtdb_dir" when the editing finished
        if not self.lineedit_gtdb_dir_editing_finished():
            OK = False

        # check "lineedit_result_dir" when the editing finished
        if not self.lineedit_result_dir_editing_finished():
            OK = False

        # check all inputs are OK
        if OK:
            self.parent.statusBar().showMessage('')
        else:
            self.parent.statusBar().showMessage('ERROR: One or more input values are wrong.')

        # enable "pushbutton_execute"
        if OK and  self.lineedit_gtdb_dir.text() != '' and self.lineedit_result_dir.text() != '':
            self.pushbutton_execute.setEnabled(True)
        else:
            self.pushbutton_execute.setEnabled(False)

        # return the control variable
        return OK

    #---------------

    def lineedit_gtdb_dir_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_gtdb_dir"
        '''

        # initialize the control variable
        OK = True

        # chek "lineedit_gtdb_dir" is empty
        if self.lineedit_gtdb_dir.text() == '':
            OK = False
            self.lineedit_gtdb_dir.setStyleSheet('background-color: white')

        # chek "lineedit_gtdb_dir" is an absolute path
        elif not genlib.is_absolute_path(self.lineedit_gtdb_dir.text()):
            self.lineedit_gtdb_dir.setStyleSheet('background-color: red')
            OK = False

        else:
            self.lineedit_gtdb_dir.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def pushbutton_search_gtdb_dir_clicked(self):
        '''
        Search and select the genotype database directory.
        '''

        # get the genotype database directory
        directory = QFileDialog.getExistingDirectory(self, f'{self.head} - Selection of the genotype database directory', os.path.expanduser('~'), QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)

        # set the genotype database directory in "lineedit_gtdb_dir"
        if directory != '':
            self.lineedit_gtdb_dir.setText(directory)

        # check the content of inputs
        self.check_inputs()

    #---------------

    def lineedit_result_dir_editing_finished(self):
        '''
        Perform necessary actions after finishing editing "lineedit_result_dir"
        '''

        # initialize the control variable
        OK = True

        # chek "lineedit_result_dir" is empty
        if self.lineedit_result_dir.text() == '':
            OK = False
            self.lineedit_result_dir.setStyleSheet('background-color: white')

        # chek "lineedit_result_dir" is an absolute path
        elif not genlib.is_absolute_path(self.lineedit_result_dir.text()):
            self.lineedit_result_dir.setStyleSheet('background-color: red')
            OK = False

        else:
            self.lineedit_result_dir.setStyleSheet('background-color: white')

        # return the control variable
        return OK

    #---------------

    def pushbutton_search_result_dir_clicked(self):
        '''
        Search and select the result directory.
        '''

        # get the result directory
        directory = QFileDialog.getExistingDirectory(self, f'{self.head} - Selection of the result directory', os.path.expanduser('~'), QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)

        # set the result directory in "lineedit_result_dir"
        if directory != '':
            self.lineedit_result_dir.setText(directory)

        # check the content of inputs
        self.check_inputs()

    #---------------

    def pushbutton_execute_clicked(self):
        '''
        Execute the process.
        '''

        # initialize the control variable
        OK = True

        # confirm the process is executed
        text = f'The file\n\n{genlib.get_app_config_file()}\n\nis going to be recreated. The previous file will be lost.\n\nAre you sure to continue?'
        botton = QMessageBox.question(self, self.title, text, buttons=QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)
        if botton == QMessageBox.No:
            OK = False

        # execute the process
        if OK:

            # get the application directory
            app_dir = os.path.dirname(os.path.abspath(__file__))

            # create the application config file
            (OK, error_list) = self.create_app_config_file(app_dir, self.lineedit_gtdb_dir.text(), self.lineedit_result_dir.text())
            if OK:
                text = f'The file\n\n{genlib.get_app_config_file()}\n\nis recreated.'
                QMessageBox.information(self, self.title, text, buttons=QMessageBox.Ok)
            else:
                text = ''
                for error in error_list:
                    text = f'{text}{error}\n'
                QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)
                OK = False

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

    @staticmethod
    def create_app_config_file(app_dir=None, gtdb_dir=None, result_dir=None):
        '''
        Create the application config file.
        '''

        # initialize the control variable and error list
        OK = True
        error_list = []

        # get he home directory
        home_dir = str(pathlib.Path.home())

        # set the application directory
        if app_dir is None:
            app_dir = os.path.dirname(os.path.abspath(__file__))
        if sys.platform.startswith('win32'):
            app_dir = genlib.windows_path_2_wsl_path(app_dir)

        # set the genotype database directory
        if gtdb_dir is None:
            gtdb_dir = f'{home_dir}/{genlib.get_gtdb_dir()}'
        if sys.platform.startswith('win32'):
            gtdb_dir = genlib.windows_path_2_wsl_path(gtdb_dir)

        # set the result directory
        if result_dir is None:
            result_dir = f'{home_dir}{os.sep}{genlib.get_result_dir()}'
        if sys.platform.startswith('win32'):
            result_dir = genlib.windows_path_2_wsl_path(result_dir)

        # get the application config file path
        app_config_file = genlib.get_app_config_file()

        # write the application config file path
        try:
            if not os.path.exists(os.path.dirname(app_config_file)):
                os.makedirs(os.path.dirname(app_config_file))
            with open(app_config_file, mode='w', encoding='iso-8859-1', newline='\n') as file_id:
                file_id.write( '[Environment parameters]\n')
                file_id.write(f'app_dir = {app_dir}\n')
                file_id.write(f'gtdb_dir = {gtdb_dir}\n')
                file_id.write(f'result_dir = {result_dir}\n')
        except Exception as e:
            error_list.append(f'*** EXCEPTION: "{e}".')
            error_list.append(f'*** ERROR: The file {app_config_file} can not be created.')
            OK = False

        # return the control variable and the error list
        return (OK, error_list)

    #---------------

#-------------------------------------------------------------------------------

class FormBrowseConfigFile(QWidget):
    '''
    Class used to browse the gtImputation config file.
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
        self.head = f'Browse {genlib.get_app_short_name()} config file'
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

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

        # create and configure "textedit"
        self.textedit = QTextEdit()
        self.textedit.setFont(QFont('Consolas', 10))

        # create and configure "gridlayout"
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.textedit, 0, 0)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout)

        # create and configure "pushbutton_close"
        pushbutton_close = QPushButton('Close')
        pushbutton_close.setToolTip('Close the browser.')
        pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        # create and configure "gridlayout_buttons"
        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 10)
        gridlayout_buttons.setColumnStretch(1, 1)
        gridlayout_buttons.addWidget(pushbutton_close, 0, 1, alignment=Qt.AlignCenter)

        # create and configure "groupbox_buttons"
        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)

        # create and configure "gridlayout_central"
        gridlayout_central = QGridLayout()
        gridlayout_central.setRowStretch(0, 1)
        gridlayout_central.setRowStretch(1, 1)
        gridlayout_central.setRowStretch(2, 10)
        gridlayout_central.setRowStretch(3, 1)
        gridlayout_central.setColumnStretch(0, 0)
        gridlayout_central.setColumnStretch(1, 1)
        gridlayout_central.setColumnStretch(2, 0)
        gridlayout_central.addWidget(label_head, 0, 1)
        gridlayout_central.addWidget(QLabel(), 1, 1)
        gridlayout_central.addWidget(groupbox_data, 2, 1)
        gridlayout_central.addWidget(groupbox_buttons, 3, 1)

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

        # load the application config file
        self.textedit_load()

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def textedit_load(self):
        '''
        Load the file data in "textedit".
        '''

        # load the file and move the cursor at start
        try:
            with open(genlib.get_app_config_file(), mode='r', encoding='iso-8859-1') as file_id:
                self.textedit.insertPlainText(file_id.read())
            text_cursor = QTextCursor(self.textedit.document())
            text_cursor.movePosition(QTextCursor.Start)
            self.textedit.setReadOnly(True)
        except Exception as e:
            print(e)
            text = f'ERROR {e}.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.parent.current_subwindow = None
        self.close()
        self.parent.set_background_image()

    #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print(f'This file contains the classes related to the configuration used in {genlib.get_app_long_name()}')
    sys.exit(0)

#-------------------------------------------------------------------------------
