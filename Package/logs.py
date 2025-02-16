#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=multiple-statements
# pylint: disable=too-many-lines

#-------------------------------------------------------------------------------

'''
This file contains the classes related to the logs of
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
import re
import subprocess
import sys

from PyQt5.QtCore import Qt                      # pylint: disable=no-name-in-module
from PyQt5.QtGui import QCursor                  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QFontMetrics             # pylint: disable=no-name-in-module
from PyQt5.QtGui import QGuiApplication          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QAbstractItemView    # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QApplication         # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QComboBox            # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGroupBox            # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QHeaderView          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel               # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMessageBox          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QPushButton          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QTableWidget         # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QTableWidgetItem     # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QVBoxLayout          # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget              # pylint: disable=no-name-in-module

import dialogs
import genlib

#-------------------------------------------------------------------------------

class FormBrowseSubmittingLogs(QWidget):
    '''
    Class used to browse the submitting logs.
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
        self.head = 'Browse submitting logs'
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

        # get font metrics information
        fontmetrics = QFontMetrics(QApplication.font())

        # create and configure "label_head"
        label_head = QLabel(self.head, alignment=Qt.AlignCenter)
        label_head.setStyleSheet('font: bold 14px; color: black; background-color: lightGray; max-height: 30px')

        # create and configure "label_process"
        label_process = QLabel()
        label_process.setText('Process')
        label_process.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "combobox_process"
        self.combobox_process = QComboBox()
        self.combobox_process.setFixedWidth(fontmetrics.width('9'*30))
        self.combobox_process.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_process.currentIndexChanged.connect(self.combobox_process_currentIndexChanged)

        # create and configure "tablewidget"
        self.tablewidget = QTableWidget()
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablewidget.horizontalHeader().setVisible(True)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.column_name_list = ['Process', 'Run id', 'Date', 'Time']
        self.tablewidget.setColumnCount(len(self.column_name_list))
        self.tablewidget.setHorizontalHeaderLabels(self.column_name_list)
        self.tablewidget.setColumnWidth(0, 240)
        self.tablewidget.setColumnWidth(1, 340)
        self.tablewidget.setColumnWidth(2, 90)
        self.tablewidget.setColumnWidth(3, 70)
        self.tablewidget.verticalHeader().setVisible(True)
        self.tablewidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablewidget.doubleClicked.connect(self.tablewidget_doubleClicked)

        # create and configure "gridlayout_data"
        gridlayout_data = QGridLayout()
        gridlayout_data.setColumnStretch(0, 1)
        gridlayout_data.setColumnStretch(1, 3)
        gridlayout_data.setColumnStretch(2, 10)
        gridlayout_data.addWidget(label_process, 0, 0)
        gridlayout_data.addWidget(self.combobox_process, 0, 1, alignment=Qt.AlignLeft)
        gridlayout_data.addWidget(self.tablewidget, 1, 0, 1, 3)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        # create and configure "pushbutton_refresh"
        self.pushbutton_refresh = QPushButton('Refresh')
        self.pushbutton_refresh.setToolTip('Update the process list.')
        self.pushbutton_refresh.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_refresh.clicked.connect(self.pushbutton_refresh_clicked)

        # create and configure "pushbutton_execute"
        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Browse the log file corresponding to the process selected.')
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
        gridlayout_buttons.setColumnStretch(3, 1)
        gridlayout_buttons.addWidget(self.pushbutton_refresh, 0, 1, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(self.pushbutton_execute, 0, 2, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(pushbutton_close, 0, 3, alignment=Qt.AlignCenter)

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
        gridlayout_central.setColumnStretch(0, 1)
        gridlayout_central.addWidget(label_head, 0, 0)
        gridlayout_central.addWidget(QLabel(), 1, 0)
        gridlayout_central.addWidget(groupbox_data, 2, 0)
        gridlayout_central.addWidget(groupbox_buttons, 3, 0)

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

        # populate data in "combobox_process"
        self.combobox_process_populate()

        # load data in "tablewidget"
        self.load_tablewidget()

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        if self.combobox_process.currentText() != '' and self.tablewidget.rowCount() > 0:
            self.pushbutton_execute.setEnabled(True)
        else:
            self.pushbutton_execute.setEnabled(False)

        # return the control variable
        return OK

    #---------------

    def combobox_process_populate(self):
        '''
        Populate data in "combobox_process".
        '''

        # get the process submitting dictionary
        submitting_dict = genlib.get_submitting_dict()

        # set the list of process submitting texts
        submitting_text_list = []
        for _, value in submitting_dict.items():
            submitting_text_list.append(value['text'])
        submitting_text_list.sort()

        # add items in "combobox_process" including "all"
        process_list = ['all'] + submitting_text_list
        self.combobox_process.addItems(process_list)

        # simultate "combobox_process" index has changed
        self.combobox_process_currentIndexChanged()

    #---------------

    def combobox_process_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_process" has been selected.
        '''

        # reload data in "tablewidget"
        self.load_tablewidget()

        # check the content of inputs
        self.check_inputs()

    #---------------

    def tablewidget_doubleClicked(self):
        '''
        Perform necessary actions after double clicking on "tablewidget".
        '''

        # all selected item indexes
        for idx in self.tablewidget.selectionModel().selectedIndexes():
            row = idx.row()

        # browse the log file corresponding to the row selected
        self.browse_file(row)

    #---------------

    def pushbutton_refresh_clicked(self):
        '''
        Refresh "tablewidget".
        '''

        # reload data in "tablewidget"
        self.load_tablewidget()

    #---------------

    def pushbutton_execute_clicked(self):
        '''
        Browse the log file corresponding to the process selected.
        '''

        # get the list of rows selected
        row_list = []
        for idx in self.tablewidget.selectionModel().selectedIndexes():
            row_list.append(idx.row())
        row_list = list(set(row_list))

        # browse the log file
        if len(row_list) == 1:
            self.browse_file(row_list[0])
        else:
            title = f'{genlib.get_app_short_name()} - {self.head}'
            text = 'One row has to be selected.'
            QMessageBox.critical(self, title, text, buttons=QMessageBox.Ok)

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.parent.current_subwindow = None
        self.close()
        self.parent.set_background_image()

    #---------------

    def load_tablewidget(self):
        '''
        Load data in "tablewidget".
        '''

        # get the process
        process = self.combobox_process.currentText()

        # get the process submitting dictionary
        submitting_dict = genlib.get_submitting_dict()

        # get the log directory
        log_dir = genlib.get_log_dir()

        # set the command to get the log files in log directory
        command = ''
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            if process == 'all':
                command = f'ls {log_dir}/*.txt'
            else:
                submitting_id = genlib.get_submitting_id(process)
                command = f'ls {log_dir}/{submitting_id}-*.txt'
        elif sys.platform.startswith('win32'):
            log_dir = log_dir.replace('/', '\\')
            if process == 'all':
                command = f'dir /B {log_dir}\\*.txt'
            else:
                submitting_id = genlib.get_submitting_id(process)
                command = f'dir /B {log_dir}\\{submitting_id}-*.txt'

        # run the command to get the log files in log directory
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=False)

        # initialize the log dictionary
        log_dict = {}

        # build the log dictionary
        for line in output.stdout.split('\n'):
            if line != '':
                line = os.path.basename(line)
                run_id = line
                try:
                    pattern = r'^(.+)\-(.+)\-(.+).txt$'
                    mo = re.search(pattern, line)
                    submission_process_id = mo.group(1).strip()
                    yymmdd = mo.group(2)
                    hhmmss = mo.group(3)
                    process_text = submitting_dict[submission_process_id]['text']
                    date = f'20{yymmdd[:2]}-{yymmdd[2:4]}-{yymmdd[4:]}'
                    time = f'{hhmmss[:2]}:{hhmmss[2:4]}:{hhmmss[4:]}'
                except:    # pylint: disable=bare-except
                    process_text = 'unknown process'
                    date = '0000-00-00'
                    time = '00:00:00'
                key = f'{process_text}-{run_id}'
                log_dict[key] = {'process_text': process_text, 'run_id': run_id, 'date': date, 'time': time}

        # initialize "tablewidget"
        self.tablewidget.clearContents()

        # set the rows number of "tablewidget"
        self.tablewidget.setRowCount(len(log_dict))

        # load data in "tablewidget"
        if log_dict:
            row = 0
            for key in sorted(log_dict.keys()):
                self.tablewidget.setItem(row, 0, QTableWidgetItem(log_dict[key]['process_text']))
                self.tablewidget.setItem(row, 1, QTableWidgetItem(log_dict[key]['run_id']))
                self.tablewidget.setItem(row, 2, QTableWidgetItem(log_dict[key]['date']))
                self.tablewidget.setItem(row, 3, QTableWidgetItem(log_dict[key]['time']))
                row += 1

    #---------------

    def browse_file(self, row):
        '''
        Browse the log file.
        '''

        # get the run identification
        run_id = self.tablewidget.item(row, 1).text()

        # set the log file path
        file_path = f'{genlib.get_log_dir()}/{run_id}'

        # create and execute "DialogFileBrowser"
        head = f'Browse {file_path}'
        file_browser = dialogs.DialogFileBrowser(self, head, file_path)
        file_browser.exec()

    #---------------

#-------------------------------------------------------------------------------

class FormBrowseResultLogs(QWidget):
    '''
    Class used to browse the result logs.
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
        self.head = 'Browse result logs'
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

        # create and configure "label_process_type"
        label_process_type = QLabel()
        label_process_type.setText('Process type')
        label_process_type.setFixedWidth(fontmetrics.width('9'*13))

        # create and configure "combobox_process_type"
        self.combobox_process_type = QComboBox()
        self.combobox_process_type.setFixedWidth(fontmetrics.width('9'*16))
        self.combobox_process_type.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_process_type.currentIndexChanged.connect(self.combobox_process_type_currentIndexChanged)

        # create and configure "label_process"
        label_process = QLabel()
        label_process.setText('Process')
        label_process.setFixedWidth(fontmetrics.width('9'*10))

        # create and configure "combobox_process"
        self.combobox_process = QComboBox()
        self.combobox_process.setFixedWidth(fontmetrics.width('9'*30))
        self.combobox_process.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_process.currentIndexChanged.connect(self.combobox_process_currentIndexChanged)

        # create and configure "tablewidget"
        self.tablewidget = QTableWidget()
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.column_name_list = ['Process', 'Result dataset', 'Date', 'Time', 'Status']
        self.tablewidget.setColumnCount(len(self.column_name_list))
        self.tablewidget.setHorizontalHeaderLabels(self.column_name_list)
        self.tablewidget.setColumnWidth(0, 230)
        self.tablewidget.setColumnWidth(1, 280)
        self.tablewidget.setColumnWidth(2, 85)
        self.tablewidget.setColumnWidth(3, 70)
        self.tablewidget.setColumnWidth(4, 90)
        self.tablewidget.verticalHeader().setVisible(True)
        self.tablewidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablewidget.doubleClicked.connect(self.tablewidget_doubleClicked)

        # create and configure "gridlayout_data"
        gridlayout_data = QGridLayout()
        gridlayout_data.setColumnStretch(0, 1)
        gridlayout_data.setColumnStretch(1, 2)
        gridlayout_data.setColumnStretch(2, 1)
        gridlayout_data.setColumnStretch(3, 5)
        gridlayout_data.addWidget(label_process_type, 0, 0)
        gridlayout_data.addWidget(self.combobox_process_type, 0, 1, alignment=Qt.AlignLeft)
        gridlayout_data.addWidget(label_process, 0, 2)
        gridlayout_data.addWidget(self.combobox_process, 0, 3, alignment=Qt.AlignLeft)
        gridlayout_data.addWidget(self.tablewidget, 1, 0, 1, 4)

        # create and configure "groupbox_data"
        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        # create and configure "pushbutton_refresh"
        self.pushbutton_refresh = QPushButton('Refresh')
        self.pushbutton_refresh.setToolTip('Update the process list.')
        self.pushbutton_refresh.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_refresh.clicked.connect(self.pushbutton_refresh_clicked)

        # create and configure "pushbutton_execute"
        self.pushbutton_execute = QPushButton('Execute')
        self.pushbutton_execute.setToolTip('Browse the log file corresponding to the process selected.')
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
        gridlayout_buttons.setColumnStretch(3, 1)
        gridlayout_buttons.addWidget(self.pushbutton_refresh, 0, 1, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(self.pushbutton_execute, 0, 2, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(pushbutton_close, 0, 3, alignment=Qt.AlignCenter)

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
        gridlayout_central.setColumnStretch(0, 1)
        gridlayout_central.addWidget(label_head, 0, 0)
        gridlayout_central.addWidget(QLabel(), 1, 0)
        gridlayout_central.addWidget(groupbox_data, 2, 0)
        gridlayout_central.addWidget(groupbox_buttons, 3, 0)

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

        # populate data in "combobox_process_type"
        self.combobox_process_type_populate()

    #---------------

    def check_inputs(self):
        '''
        Check the content of each input and do the actions linked to its value.
        '''

        # initialize the control variable
        OK = True

        # enable "pushbutton_refresh" and"pushbutton_execute"
        if self.combobox_process_type.currentText() != '' and self.combobox_process.currentText() != '' and self.tablewidget.rowCount() > 0:
            self.pushbutton_refresh.setEnabled(True)
            self.pushbutton_execute.setEnabled(True)
        elif self.combobox_process_type.currentText() != '' and self.combobox_process.currentText() != '' and self.tablewidget.rowCount() == 0:
            self.pushbutton_refresh.setEnabled(True)
            self.pushbutton_execute.setEnabled(False)
        else:
            self.pushbutton_refresh.setEnabled(False)
            self.pushbutton_execute.setEnabled(False)

        # return the control variable
        return OK

    #---------------

    def combobox_process_type_populate(self):
        '''
        Populate data in "combobox_process_type".
        '''

        # set the process type list
        process_type_list = ['', genlib.get_result_imputation_subdir(), genlib.get_result_installation_subdir()]

        # add items in "combobox_process_type"
        self.combobox_process_type.addItems(process_type_list)

        # simultate "combobox_process_type" index has changed
        self.combobox_process_type_currentIndexChanged()

    #---------------

    def combobox_process_type_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_process_type" has been selected.
        '''

        # initialize "tablewidget"
        self.tablewidget.clearContents()

        # initialize the rows number of "tableswdget"
        self.tablewidget.setRowCount(0)

        # populate data in "combobox_process"
        self.combobox_process_populate()

        # check the content of inputs
        self.check_inputs()

    #---------------

    def combobox_process_populate(self):
        '''
        Populate data in "combobox_process".
        '''

        # initialize "combo_process"
        self.combobox_process.clear()

        # set the process list
        if self.combobox_process_type.currentText() == genlib.get_result_imputation_subdir():
            process_list = ['all'] + genlib.get_process_name_list(genlib.get_result_imputation_subdir())
        elif self.combobox_process_type.currentText() == genlib.get_result_installation_subdir():
            process_list = ['all'] + genlib.get_process_name_list(genlib.get_result_installation_subdir())
        else:
            process_list = ['']

        # add items in "combobox_process"
        self.combobox_process.addItems(process_list)

        # simultate "combobox_process" index has changed
        self.combobox_process_currentIndexChanged()

    #---------------

    def combobox_process_currentIndexChanged(self):
        '''
        Process the event when an item of "combobox_process" has been selected.
        '''

        # load data in "tablewidget"
        self.load_tablewidget()

        # check the content of inputs
        self.check_inputs()

    #---------------

    def tablewidget_doubleClicked(self):
        '''
        Perform necessary actions after double clicking on "tablewidget".
        '''

        # all selected item indexes
        for idx in self.tablewidget.selectionModel().selectedIndexes():
            row = idx.row()

        # browse the log file corresponding to the row selected
        self.browse_file(row)

    #---------------

    def pushbutton_refresh_clicked(self):
        '''
        Refresh "tablewidget".
        '''

        # reload data in "tablewidget"
        self.load_tablewidget()

    #---------------

    def pushbutton_execute_clicked(self):
        '''
        Browse the log file corresponding to the process selected.
        '''

        # get the list of rows selected
        row_list = []
        for idx in self.tablewidget.selectionModel().selectedIndexes():
            row_list.append(idx.row())
        row_list = list(set(row_list))

        # browse the log file
        if len(row_list) == 1:
            self.browse_file(row_list[0])
        else:
            title = f'{genlib.get_app_short_name()} - {self.head}'
            text = 'One row has to be selected.'
            QMessageBox.critical(self, title, text, buttons=QMessageBox.Ok)

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.parent.current_subwindow = None
        self.close()
        self.parent.set_background_image()

    #---------------

    def load_tablewidget(self):
        '''
        Load data in "tablewidget".
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # set the type, name and code of the annotation pipeline datasets
        process_type = self.combobox_process_type.currentText()
        process_name = self.combobox_process.currentText()
        process_code = genlib.get_process_id(process_name)

        # get the process dictionary
        process_dict = genlib.get_process_dict()

        # get the log directory
        log_dir = f'{result_dir}/{process_type}'
        if sys.platform.startswith('win32'):
            log_dir = genlib.wsl_path_2_windows_path(log_dir)

        # set the command to get the result datasets of annotation pipeline in the log directory
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            if process_name == 'all':
                command = f'ls -d {log_dir}/*  | xargs -n 1 basename'
            else:
                command = f'ls -d {log_dir}/{process_code}-*  | xargs -n 1 basename'
        elif sys.platform.startswith('win32'):
            log_dir = log_dir.replace('/', '\\')
            if process_name == 'all':
                command = f'dir /a:d /b {log_dir}\\*'
            else:
                command = f'dir /a:d /b {log_dir}\\{process_code}-*'

        # run the command to get the result datasets of enrichment analysis in the log directory
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=False)

        # initialize the result dataset dictionary
        result_dataset_dict = {}

        # build the result dataset dictionary
        for line in output.stdout.split('\n'):
            if line != '':

                # get data
                result_dataset_id = line.strip()
                try:
                    pattern = r'^(.+)\-(.+)\-(.+)$'
                    mo = re.search(pattern, result_dataset_id)
                    process_code = mo.group(1).strip()
                    process_name = process_dict[process_code]['name']
                    yymmdd = mo.group(2)
                    hhmmss = mo.group(3)
                    date = f'20{yymmdd[:2]}-{yymmdd[2:4]}-{yymmdd[4:]}'
                    time = f'{hhmmss[:2]}:{hhmmss[2:4]}:{hhmmss[4:]}'
                except:    # pylint: disable=bare-except
                    process_name = 'unknown process'
                    date = '0000-00-00'
                    time = '00:00:00'

                # determine the status
                status_ok = os.path.isfile(genlib.get_status_ok(os.path.join(log_dir, result_dataset_id)))
                status_wrong = os.path.isfile(genlib.get_status_wrong(os.path.join(log_dir, result_dataset_id)))
                if status_ok and not status_wrong:
                    status = 'OK'
                elif not status_ok and status_wrong:
                    status = 'wrong'
                elif not status_ok and not status_wrong:
                    status = 'not finished'
                elif status_ok and status_wrong:
                    status = 'undetermined'

                # insert data in the dictionary
                key = f'{process_name}-{result_dataset_id}'
                result_dataset_dict[key] = {'process': process_name, 'result_dataset_id': result_dataset_id, 'date': date, 'time': time, 'status': status}

        # initialize "tablewidget"
        self.tablewidget.clearContents()

        # set the rows number of "tableswdget"
        self.tablewidget.setRowCount(len(result_dataset_dict))

        # load data in "tablewidget"
        if result_dataset_dict:
            row = 0
            for key in sorted(result_dataset_dict.keys()):
                self.tablewidget.setItem(row, 0, QTableWidgetItem(result_dataset_dict[key]['process']))
                self.tablewidget.setItem(row, 1, QTableWidgetItem(result_dataset_dict[key]['result_dataset_id']))
                self.tablewidget.setItem(row, 2, QTableWidgetItem(result_dataset_dict[key]['date']))
                self.tablewidget.setItem(row, 3, QTableWidgetItem(result_dataset_dict[key]['time']))
                self.tablewidget.setItem(row, 4, QTableWidgetItem(result_dataset_dict[key]['status']))
                row += 1

    #---------------

    def browse_file(self, row):
        '''
        Browse the log file.
        '''

        # get the result directory
        result_dir = self.app_config_dict['Environment parameters']['result_dir']

        # get the result dataset
        result_dataset = self.tablewidget.item(row, 1).text()

        # set the log file path
        file_path = f'{result_dir}/{self.combobox_process_type.currentText()}/{result_dataset}/{genlib.get_run_log_file()}'
        if sys.platform.startswith('win32'):
            file_path = genlib.wsl_path_2_windows_path(file_path)

        # create and execute "DialogFileBrowser"
        head = f'Browse .../{self.combobox_process_type.currentText()}/{result_dataset}/{genlib.get_run_log_file()}'
        file_browser = dialogs.DialogFileBrowser(self, head, file_path)
        file_browser.exec()

    #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print(f'This file contains the classes related to the configuration used in {genlib.get_app_long_name()}')
    sys.exit(0)

#-------------------------------------------------------------------------------
