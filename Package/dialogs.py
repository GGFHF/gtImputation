#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=multiple-statements
# pylint: disable=too-many-lines

#-------------------------------------------------------------------------------

'''
This source contains the classes related to dialogs of
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

from PyQt5.QtCore import Qt                     # pylint: disable=no-name-in-module
from PyQt5.QtGui import QCursor                 # pylint: disable=no-name-in-module
from PyQt5.QtGui import QFont                   # pylint: disable=no-name-in-module
from PyQt5.QtGui import QGuiApplication         # pylint: disable=no-name-in-module
from PyQt5.QtGui import QIcon                   # pylint: disable=no-name-in-module
from PyQt5.QtGui import QPixmap                 # pylint: disable=no-name-in-module
from PyQt5.QtGui import QTextCursor             # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QApplication        # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog             # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout         # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGroupBox           # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel              # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMessageBox         # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QPushButton         # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QTextEdit           # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QVBoxLayout         # pylint: disable=no-name-in-module


import genlib

#-------------------------------------------------------------------------------

class Process(QDialog):
    '''
    The class of the dialog "Process".
    '''

    #---------------

    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 800

    #---------------

    def __init__(self, parent, head, calling_function, *args):
        '''
        Create a class instance.
        '''

        self.parent = parent
        self.head = head
        self.calling_function = calling_function
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

        super().__init__()

        self.build_gui()
        self.initialize_inputs()

        self.create_log_file()
        self.calling_function(self, *args)
        self.enable_pushbutton_close()

        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        self.setWindowTitle(f'{genlib.get_app_short_name()} - {self.head}')
        self.setWindowIcon(QIcon(genlib.get_app_image_file()))

        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # -- self.setMinimumSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # -- self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # -- self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        # -- self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        self.textedit = QTextEdit(self)
        self.textedit.setFont(QFont('Consolas', 10))
        self.textedit.setReadOnly(True)

        gridlayout_data = QGridLayout()
        gridlayout_data.addWidget(self.textedit, 0, 0)

        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        self.pushbutton_close = QPushButton('Close')
        self.pushbutton_close.setToolTip('Close the window.')
        self.pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 10)
        gridlayout_buttons.setColumnStretch(1, 1)
        gridlayout_buttons.addWidget(self.pushbutton_close, 0, 1, alignment=Qt.AlignCenter)

        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)
        gridlayout_central = QGridLayout()
        gridlayout_central.setRowStretch(0, 10)
        gridlayout_central.setRowStretch(1, 1)
        gridlayout_central.setColumnStretch(0, 0)
        gridlayout_central.setColumnStretch(1, 1)
        gridlayout_central.setColumnStretch(2, 0)
        gridlayout_central.addWidget(groupbox_data, 0, 1)
        gridlayout_central.addWidget(groupbox_buttons, 1, 1)

        groupbox_central = QGroupBox()
        groupbox_central.setLayout(gridlayout_central)

        vboxlayout = QVBoxLayout(self)
        vboxlayout.addWidget(groupbox_central)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        self.pushbutton_close.setEnabled(False)

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the log file and window.
        '''

        self.log_file_id.close()

        self.close()

    #---------------

    def enable_pushbutton_close(self):
        '''
        Enable "pushbutton_close".
        '''

        QGuiApplication.restoreOverrideCursor()

        self.pushbutton_close.setEnabled(True)

    #---------------

    def create_log_file(self):
        '''
        Create a log file with submission information.
        '''

        self.log_file = genlib.get_submission_log_file(self.calling_function.__name__)
        try:
            if not os.path.exists(os.path.dirname(self.log_file)):
                os.makedirs(os.path.dirname(self.log_file))
            self.log_file_id = open(self.log_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception:
            text = f'*** ERROR: The file {self.log_file} can not be created.'
            QMessageBox.critical(self, self.title, text, buttons=QMessageBox.Ok)
            self.pushbutton_close_clicked()

    #---------------

    def write(self, text=''):
        '''
        Add a message text in the widget "textedit" and in the log file.
        '''

        self.textedit.insertPlainText(text)
        QApplication.processEvents()

        self.log_file_id.write(text)
        self.log_file_id.flush()
        os.fsync(self.log_file_id.fileno())

#-------------------------------------------------------------------------------

class FileBrowser(QDialog):
    '''
    The class of the dialog "FileBrowser".
    '''

    #---------------

    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 800

    #---------------

    def __init__(self, parent, head, file_path):
        '''
        Create a class instance.
        '''

        self.parent = parent
        self.head = head
        self.file_path = file_path
        self.title = f'{genlib.get_app_short_name()} - {self.head}'

        super().__init__()

        self.build_gui()
        self.initialize_inputs()

        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        # -- self.showMaximized()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        self.setWindowTitle(f'{genlib.get_app_short_name()} - {self.head}')
        self.setWindowIcon(QIcon(genlib.get_app_image_file()))

        # -- self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setMinimumSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # -- self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        self.textedit = QTextEdit()
        self.textedit.setFont(QFont('Consolas', 10))
        self.textedit.setReadOnly(True)

        gridlayout_data = QGridLayout()
        gridlayout_data.addWidget(self.textedit, 0, 0)

        groupbox_data = QGroupBox()
        groupbox_data.setObjectName('groupbox_data')
        groupbox_data.setStyleSheet('QGroupBox#groupbox_data {border: 0px;}')
        groupbox_data.setLayout(gridlayout_data)

        self.pushbutton_refresh = QPushButton('Refresh')
        self.pushbutton_refresh.setToolTip('Reload the file content.')
        self.pushbutton_refresh.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_refresh.clicked.connect(self.pushbutton_refresh_clicked)

        self.pushbutton_close = QPushButton('Close')
        self.pushbutton_close.setToolTip('Close the window.')
        self.pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        gridlayout_buttons = QGridLayout()
        gridlayout_buttons.setColumnStretch(0, 15)
        gridlayout_buttons.setColumnStretch(1, 1)
        gridlayout_buttons.setColumnStretch(2, 1)
        gridlayout_buttons.addWidget(self.pushbutton_refresh, 0, 1, alignment=Qt.AlignCenter)
        gridlayout_buttons.addWidget(self.pushbutton_close, 0, 2, alignment=Qt.AlignCenter)

        groupbox_buttons = QGroupBox()
        groupbox_buttons.setObjectName('groupbox_buttons')
        groupbox_buttons.setStyleSheet('QGroupBox#groupbox_buttons {border: 0px;}')
        groupbox_buttons.setLayout(gridlayout_buttons)
        gridlayout_central = QGridLayout()
        gridlayout_central.setRowStretch(0, 10)
        gridlayout_central.setRowStretch(1, 1)
        gridlayout_central.setColumnStretch(0, 0)
        gridlayout_central.setColumnStretch(1, 1)
        gridlayout_central.setColumnStretch(2, 0)
        gridlayout_central.addWidget(groupbox_data, 0, 1)
        gridlayout_central.addWidget(groupbox_buttons, 1, 1)

        groupbox_central = QGroupBox()
        groupbox_central.setLayout(gridlayout_central)

        vboxlayout = QVBoxLayout(self)
        vboxlayout.addWidget(groupbox_central)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        self.load_file_content()

    #---------------

    def pushbutton_refresh_clicked(self):
        '''
        Reload the file content.
        '''

        self.load_file_content()

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the log file and window.
        '''

        self.close()

    #---------------

    def enable_pushbutton_close(self):
        '''
        Enable "pushbutton_close".
        '''

        QGuiApplication.restoreOverrideCursor()

        self.pushbutton_close.setEnabled(True)

    #---------------

    def load_file_content(self):
        '''
        Load the file content in the widget "textedit".
        '''

        self.textedit.clear()
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file_id:
                self.textedit.insertPlainText(file_id.read())
        except Exception:
            title = f'{genlib.get_app_short_name()} - {self.head}'
            text = f'The file\n\n{self.file_path}\n\ncan not be opened.'
            QMessageBox.critical(self, title, text, buttons=QMessageBox.Ok)
        # text_cursor = QTextCursor(self.textedit.document())
        # text_cursor.movePosition(QTextCursor.Start)
        text_cursor = QTextCursor(self.textedit.document().findBlockByLineNumber(0))
        self.textedit.setTextCursor(text_cursor)

        # QApplication.processEvents()

#-------------------------------------------------------------------------------

class About(QDialog):
    '''
    The class of the dialog "About".
    '''

    #---------------

    WINDOW_HEIGHT = 300
    WINDOW_WIDTH = 675

    #---------------

    def __init__(self, parent):
        '''
        Create a class instance.
        '''

        self.parent = parent

        super().__init__()

        self.build_gui()
        self.setWindowModality(Qt.ApplicationModal)

        self.show()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        self.setWindowTitle(f'{genlib.get_app_short_name()} - About')
        self.setWindowIcon(QIcon(genlib.get_app_image_file()))

        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # -- self.setMinimumSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # -- self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # -- self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        # -- self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        label_image = QLabel()
        label_image.setPixmap(QPixmap(genlib.get_app_image_file()))

        label_proyecto = QLabel()
        label_proyecto.setText(f'{genlib.get_app_long_name()} v{genlib.get_app_version()}')
        label_proyecto.setStyleSheet('font-weight: bold')

        label_department = QLabel()
        label_department.setText('Dpto. Sistemas y Recursos Naturales')

        label_college = QLabel()
        label_college.setText('ETSI Montes, Forestal y del Medio Natural')

        label_university = QLabel()
        label_university.setText('Universidad Politécnica de Madrid')

        label_url = QLabel()
        label_url.setText('https://github.com/ggfhf/')

        pushbutton_close =QPushButton('Close')
        pushbutton_close.setToolTip('Close the window.')
        pushbutton_close.setCursor(QCursor(Qt.PointingHandCursor))
        pushbutton_close.clicked.connect(self.pushbutton_close_clicked)

        gridlayout = QGridLayout()
        gridlayout.setRowStretch(0, 2)
        gridlayout.setRowStretch(1, 1)
        gridlayout.setRowStretch(2, 1)
        gridlayout.setRowStretch(3, 1)
        gridlayout.setRowStretch(4, 1)
        gridlayout.setRowStretch(5, 1)
        gridlayout.setColumnStretch(0, 1)
        gridlayout.setColumnStretch(1, 1)
        gridlayout.setColumnStretch(2, 1)
        gridlayout.addWidget(label_image, 1, 0, 4, 1, alignment=Qt.AlignCenter)
        gridlayout.addWidget(label_proyecto, 0, 1, alignment=Qt.AlignCenter)
        gridlayout.addWidget(label_department, 1, 1, alignment=Qt.AlignCenter)
        gridlayout.addWidget(label_college, 2, 1, alignment=Qt.AlignCenter)
        gridlayout.addWidget(label_university, 3, 1, alignment=Qt.AlignCenter)
        gridlayout.addWidget(label_url, 4, 1, alignment=Qt.AlignCenter)
        gridlayout.addWidget(pushbutton_close, 5, 2, alignment=Qt.AlignCenter)

        groupbox = QGroupBox()
        groupbox.setLayout(gridlayout)

        vboxlayout = QVBoxLayout()
        vboxlayout.addWidget(groupbox)

        self.setLayout(vboxlayout)

    #---------------

    def pushbutton_close_clicked(self):
        '''
        Close the window.
        '''

        self.close()

   #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print(f'This file contains the classes related to dialogs used in {genlib.get_app_long_name()}.')
    sys.exit(1)

#-------------------------------------------------------------------------------
