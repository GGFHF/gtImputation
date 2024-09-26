#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=multiple-statements
# pylint: disable=too-many-lines

#-------------------------------------------------------------------------------

'''
This source define the main class of Genotype Imputation (gtImputation) and starts
the application.

This software has been developed by:

    GI en Especies Leñosas (WooSp)
    Dpto. Sistemas y Recursos Naturales
    ETSI Montes, Forestal y del Medio Natural
    Universidad Politecnica de Madrid
    https://github.com/ggfhf/

Licence: GNU General Public Licence Version 3.
'''

#-------------------------------------------------------------------------------

import os
import sys
import webbrowser

import genlib

try:
    from PyQt5.QtCore import Qt                  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QCursor              # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QFont                # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QGuiApplication      # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon                # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QAction          # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QApplication     # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel           # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QMainWindow      # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QMenuBar         # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QMessageBox      # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QVBoxLayout      # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget          # pylint: disable=no-name-in-module
except Exception as e:
    raise genlib.ProgramException('', 'S002', 'PyQt5')

import bioinfosw
import configuration
import dialogs
import imputations
import logs

#-------------------------------------------------------------------------------

class MainWindow(QMainWindow):
    '''
    the main class of the application.
    '''

    #---------------

    # set the window dimensions
    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 900

    #---------------

    def __init__(self):

        # call the init method of the parent class
        super().__init__()

        # initialize the current subwindow
        self.current_subwindow = None

        # build the graphic user interface of the window
        self.build_gui()

        # show the window
        self.show()

    #---------------

    def build_gui(self):
        '''
        Build the graphic user interface of the window.
        '''

        # set the window title and icon
        self.setWindowTitle(genlib.get_app_short_name())
        self.setWindowIcon(QIcon(genlib.get_app_image_file()))

        # set the window size
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # -- self.setMinimumSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # -- self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # set the window flags
        # -- self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        # -- self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # move the window at center
        rectangle = self.frameGeometry()
        central_point = QGuiApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(central_point)
        self.move(rectangle.topLeft())

        # create and configure "action_exit"
        action_exit = QAction(QIcon('./image-exit.png'),'&Exit', self)
        action_exit.setShortcut('Alt+F4')
        action_exit.setStatusTip(f'Exit {genlib.get_app_long_name()}.')
        action_exit.triggered.connect(self.action_exit_clicked)

        # create and configure "action_recreate_config_file"
        action_recreate_config_file = QAction(f'Recreate {genlib.get_app_short_name()} config file', self)
        action_recreate_config_file.setStatusTip(f'Recreate the {genlib.get_app_short_name()} config file.')
        action_recreate_config_file.triggered.connect(self.action_recreate_config_file_clicked)

        # create and configure "action_browse_config_file"
        action_browse_config_file = QAction(f'Browse {genlib.get_app_short_name()} config file', self)
        action_browse_config_file.setStatusTip(f'Browse the {genlib.get_app_short_name()} config file.')
        action_browse_config_file.triggered.connect(self.action_browse_config_file_clicked)

        # create and configure "action_install_miniconda3"
        action_install_miniconda3 = QAction('Miniconda3 and additional infrastructure software', self)
        action_install_miniconda3.setStatusTip('Install Miniconda3 and additional infrastructure software.')
        action_install_miniconda3.triggered.connect(self.action_install_miniconda3_clicked)

        # create and configure "action_run_naive_process"
        action_run_naive_process = QAction('Run imputation process', self)
        action_run_naive_process.setStatusTip('Run the process of naive imputation.')
        action_run_naive_process.triggered.connect(self.action_run_naive_process_clicked)

        # create and configure "action_review_naive_imputation"
        action_review_naive_imputation = QAction('Review imputation process', self)
        action_review_naive_imputation.setStatusTip('Review a process of naive imputation.')
        action_review_naive_imputation.triggered.connect(self.action_review_naive_imputation_clicked)

        # create and configure "action_run_gtdb_process"
        action_run_gtdb_process = QAction('Build a genotype database', self)
        action_run_gtdb_process.setStatusTip('Run the process for building a genotype database.')
        action_run_gtdb_process.triggered.connect(self.action_run_gtdb_process_clicked)

        # create and configure "action_run_som_process"
        action_run_som_process = QAction('Run imputation process', self)
        action_run_som_process.setStatusTip('Run a process of SOM imputation.')
        action_run_som_process.triggered.connect(self.action_run_som_process_clicked)

        # create and configure "action_review_som_imputation"
        action_review_som_imputation = QAction('Review imputation process', self)
        action_review_som_imputation.setStatusTip('Review a process of SOM imputation.')
        action_review_som_imputation.triggered.connect(self.action_review_som_imputation_clicked)

        # create and configure "action_browse_submitting_logs"
        action_browse_submitting_logs = QAction('Submitting logs', self)
        action_browse_submitting_logs.setStatusTip('Browse the submitting logs.')
        action_browse_submitting_logs.triggered.connect(self.action_browse_submitting_logs_clicked)

        # create and configure "action_browse_result_logs"
        action_browse_result_logs = QAction('Result logs', self)
        action_browse_result_logs.setStatusTip('Browse the result logs.')
        action_browse_result_logs.triggered.connect(self.action_browse_result_logs_clicked)

        # create and configure "action_manual"
        action_manual = QAction('&Manual', self)
        action_manual.setShortcut('F1')
        action_manual.setStatusTip('Open the manual')
        action_manual.triggered.connect(self.accion_manual_clicked)

        # create and configure "action_about"
        action_about = QAction('&About...', self)
        action_about.setStatusTip('Show the application information.')
        action_about.triggered.connect(self.accion_about_clicked)

        # create and configure "menubar"
        menubar = QMenuBar(self)
        menubar.setCursor(QCursor(Qt.PointingHandCursor))

        # create and configure "menu_application"
        menu_application = menubar.addMenu('&Application')
        menu_application.setCursor(QCursor(Qt.PointingHandCursor))
        menu_application.addAction(action_exit)

        # create and configure "menu_configuration" and its submenus
        menu_configuration = menubar.addMenu('&Configuration')
        menu_configuration.setCursor(QCursor(Qt.PointingHandCursor))
        menu_configuration.addAction(action_recreate_config_file)
        menu_configuration.addAction(action_browse_config_file)
        menu_configuration.addSeparator()
        submenu_bioinfo = menu_configuration.addMenu('Bioinfo software installation')
        submenu_bioinfo.addAction(action_install_miniconda3)

        # create and configure "menu_imputation" and its submenus
        menu_imputation = menubar.addMenu('&Imputation')
        menu_imputation.setCursor(QCursor(Qt.PointingHandCursor))
        submenu_naive_imputation = menu_imputation.addMenu('Naive imputation')
        submenu_naive_imputation.addAction(action_run_naive_process)
        submenu_naive_imputation.addAction(action_review_naive_imputation)
        menu_imputation.addSeparator()
        submenu_som_imputation = menu_imputation.addMenu('SOM imputation')
        submenu_som_imputation.addAction(action_run_gtdb_process)
        submenu_som_imputation.addSeparator()
        submenu_som_imputation.addAction(action_run_som_process)
        submenu_som_imputation.addAction(action_review_som_imputation)

        # create and configure "menu_logs"
        menu_logs = menubar.addMenu('&Logs')
        menu_logs.setCursor(QCursor(Qt.PointingHandCursor))
        menu_logs.addAction(action_browse_submitting_logs)
        menu_logs.addSeparator()
        menu_logs.addAction(action_browse_result_logs)

        # create and configure "menu_help"
        menu_help = menubar.addMenu('&Help')
        menu_help.setCursor(QCursor(Qt.PointingHandCursor))
        menu_help.addAction(action_manual)
        menu_help.addSeparator()
        menu_help.addAction(action_about)

        # set the menu bar in "MainWindow"
        self.setMenuBar(menubar)

        # configure "toolbar" in "MainWindow"
        self.toolbar = self.addToolBar('Salir')
        self.toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.toolbar.addAction(action_exit)

        # configure the status bar in "MainWindow"
        self.statusBar().showMessage(f'Welcome to {genlib.get_app_long_name()}.')

        # set the bakcground image in "MainWindow"
        self.set_background_image()

    #---------------

    def closeEvent(self, event):
        '''
        The application is going to be closed.
        '''

        title = f'{genlib.get_app_short_name()} - Exit'
        text = f'Are you sure to exit {genlib.get_app_short_name()}?'
        botton = QMessageBox.question(self, title, text, buttons=QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)
        if botton == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    #---------------

    def action_exit_clicked(self):
        '''
        Exit the application.
        '''

        self.close()

    #---------------

    def action_recreate_config_file_clicked(self):
        '''
        Recreate the config file of gtImputation.
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = configuration.FormRecreateConfigFile(self)

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def action_browse_config_file_clicked(self):
        '''
        Browse the config file of gtImputation.
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = configuration.FormBrowseConfigFile(self)

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def action_install_miniconda3_clicked(self):
        '''
        Install Miniconda3 software (Conda infrastructure).
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = bioinfosw.FormInstallBioinfoSoftware(self, genlib.get_miniconda3_code(), genlib.get_miniconda3_name())

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def action_run_naive_process_clicked(self):
        '''
        Run the process of naive imputation.
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = imputations.FormNaiveImputation(self)

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def action_review_naive_imputation_clicked(self):
        '''
        Review a process of naive imputation.
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = imputations.FormNaiveImputationReview(self)

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def action_run_gtdb_process_clicked(self):
        '''
        Run the process for building a genotype database..
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = imputations.FormGenotypeDatabase(self)

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def action_run_som_process_clicked(self):
        '''
        Run a process of SOM imputation.
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = imputations.FormSOMImputation(self)

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def action_review_som_imputation_clicked(self):
        '''
        Review a process of SOM imputation.
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = imputations.FormSOMImputationReview(self)

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def action_browse_submitting_logs_clicked(self):
        '''
        Browse submitting logs.
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = logs.FormBrowseSubmittingLogs(self)

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def action_browse_result_logs_clicked(self):
        '''
        Browse result logs.
        '''

        # close the existing subwindow
        if self.current_subwindow is not None:
            self.current_subwindow.close()

        # create a new subwindow to perform the action
        subwindow = logs.FormBrowseResultLogs(self)

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        v_box_layout.addWidget(subwindow, alignment=Qt.AlignCenter)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

        # save the current subwindow
        self.current_subwindow = subwindow

    #---------------

    def accion_manual_clicked(self):
        '''
        Open the help file.
        '''

        # set the path of the manual
        manual = os.path.abspath(genlib.get_app_manual_file())

        # browse the manual
        if os.path.exists(manual):
            webbrowser.open_new(f'file://{manual}')
        else:
            title = f'{genlib.get_app_short_name()} - Help - Manual'
            text = f'The document\n\n{manual}\n\nis not available.'
            QMessageBox.critical(self, title, text, buttons=QMessageBox.Ok)

    #---------------

    def accion_about_clicked(self):
        '''
        Show the application information.
        '''

        # create and execute "dialog_about"
        dialog_about = dialogs.DialogAbout(self)
        dialog_about.exec()

    #---------------

    def set_background_image(self):
        '''
        Set the bakcground image in MainWindow.
        '''

        # create and configure "label_image"
        label_image = QLabel(self)
        label_image.setStyleSheet(f'border-image : url({genlib.get_app_background_image_file()});')

        # create "widget_central"
        widget_central = QWidget(self)

        # create and configure "v_box_layout"
        v_box_layout = QVBoxLayout(widget_central)
        # v_box_layout.addWidget(label_image, alignment=Qt.AlignCenter)
        v_box_layout.addWidget(label_image)

        # set the central widget in "MainWindow"
        self.setCentralWidget(widget_central)

    #---------------

    def warn_unavailable_process(self):
        '''
        Show a message warning the process is unavailable.
        '''

        title = f'{genlib.get_app_short_name()} - Warning'
        text = 'This process is been built.\n\nIt is coming soon!'
        QMessageBox.warning(self, title, text, buttons=QMessageBox.Ok)

    #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    # check the operating system
    if sys.platform.startswith('win32'):
        command = 'whoami'
        null = open('nul', 'w', encoding='iso-8859-1')
        rc = genlib.run_command(command, null, is_script=False)
        null.close()
        if rc == 0:
            pass
        else:
            print('*** ERROR: The WSL 2 is not installed.')
            sys.exit(1)
    elif not sys.platform.startswith('linux') and not sys.platform.startswith('darwin'):
        print(f'*** ERROR: The {sys.platform} OS is not supported.')
        sys.exit(1)

    # check the Python version
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
        pass
    else:
        print('*** ERROR: Python 3.8 or greater is required.')
        sys.exit(1)

    # check if the current directory is gtImputation home directory
    current_dir = os.getcwd()
    program_name = os.path.basename(__file__)
    if not os.path.isfile(os.path.join(current_dir, program_name)):
        print(f'*** ERROR: {program_name} has to be run in the gtImputation home directory.')
        sys.exit(1)

    # set the font
    (default_font, default_size) = genlib.get_default_font_size()
    font = QFont(default_font, default_size)
    font.setStyleHint(QFont.SansSerif)

    # create and configure "application"
    application = QApplication(sys.argv)
    # -- if sys.platform.startswith('win32'):
    # --     application.setStyle(QStyleFactory.create('Fusion'))
    application.setFont(font)

    # create and execute "mainwindow"
    mainwindow = MainWindow()
    sys.exit(application.exec_())

#-------------------------------------------------------------------------------
