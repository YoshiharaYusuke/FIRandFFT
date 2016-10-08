import os
import sys

from PySide import QtCore, QtGui
import numpy as np
from scipy import fromstring, int16
import scipy.signal as scsi
import wave as wv
import pyqtgraph as pg

import conf
import gui2


pg.setConfigOption('foreground', 'k')
pg.setConfigOption('background', 'w')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_graph = QtGui.QVBoxLayout()
        self.verticalLayout_graph.setObjectName("verticalLayout_graph")
        self.graphicsView_signal =  pg.PlotWidget()
        self.graphicsView_signal.setObjectName("graphicsView_signal")
        self.verticalLayout_graph.addWidget(self.graphicsView_signal)
        self.graphicsView_spectrum = pg.PlotWidget()
        self.graphicsView_spectrum.setObjectName("graphicsView_spectrum")
        self.verticalLayout_graph.addWidget(self.graphicsView_spectrum)
        self.horizontalLayout.addLayout(self.verticalLayout_graph)
        self.formLayout_property = QtGui.QFormLayout()
        self.formLayout_property.setObjectName("formLayout_property")
        self.comboBox_filter = QtGui.QComboBox(self.centralwidget)
        self.comboBox_filter.setObjectName("comboBox_filter")
        self.comboBox_filter.addItem("")
        self.comboBox_filter.addItem("")
        self.comboBox_filter.addItem("")
        self.comboBox_filter.addItem("")
        self.formLayout_property.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_filter)
        self.spinBox_tap = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_tap.setObjectName("spinBox_tap")
        self.formLayout_property.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBox_tap)
        self.doubleSpinBox_low = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_low.setObjectName("doubleSpinBox_low")
        self.formLayout_property.setWidget(3, QtGui.QFormLayout.FieldRole, self.doubleSpinBox_low)
        self.label_1 = QtGui.QLabel(self.centralwidget)
        self.label_1.setObjectName("label_1")
        self.formLayout_property.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout_property.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.doubleSpinBox_high = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_high.setObjectName("doubleSpinBox_high")
        self.formLayout_property.setWidget(4, QtGui.QFormLayout.FieldRole, self.doubleSpinBox_high)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout_property.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout_property.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout.addLayout(self.formLayout_property)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuLicence = QtGui.QMenu(self.menubar)
        self.menuLicence.setObjectName("menuLicence")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSample = QtGui.QAction(MainWindow)
        self.actionSample.setObjectName("actionSample")
        self.actionShow = QtGui.QAction(MainWindow)
        self.actionShow.setObjectName("actionShow")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSample)
        self.menuLicence.addAction(self.actionShow)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuLicence.menuAction())


        self.dialog = QtGui.QFileDialog()
        self.dialog.setModal(True)###############modal is on. Without it, main window is active while filedialog is showing up
        self.dialog.setDirectory(os.path.expanduser('~'))########Initial directory is home not current directory.
        filters = ["csv comma-separated values(*.csv)", "text file(*.txt)", "tab tab-separated values(*.tsv)", "wav file(*.wav)", "All(*)"]#     file extention.
        self.dialog.setNameFilters(filters)
        QtCore.QObject.connect(self.dialog, QtCore.SIGNAL("accepted()"), self.load)
        QtCore.QObject.connect(self.dialog, QtCore.SIGNAL("rejected()"), self.reject)


        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.open)
        QtCore.QObject.connect(self.actionSample, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.comboBox_filter, QtCore.SIGNAL("currentIndexChanged(int)"), MainWindow.close)
        QtCore.QObject.connect(self.doubleSpinBox_high, QtCore.SIGNAL("editingFinished()"), MainWindow.close)
        QtCore.QObject.connect(self.doubleSpinBox_low, QtCore.SIGNAL("editingFinished()"), MainWindow.close)
        QtCore.QObject.connect(self.spinBox_tap, QtCore.SIGNAL("editingFinished()"), MainWindow.close)
        QtCore.QObject.connect(self.actionShow, QtCore.SIGNAL("triggered()"), self.License)###########################################
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "FirAndFft", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_filter.setItemText(0, QtGui.QApplication.translate("MainWindow", "Low pass filter", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_filter.setItemText(1, QtGui.QApplication.translate("MainWindow", "High pass filter", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_filter.setItemText(2, QtGui.QApplication.translate("MainWindow", "Band pass filter", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_filter.setItemText(3, QtGui.QApplication.translate("MainWindow", "Band stop filter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_1.setText(QtGui.QApplication.translate("MainWindow", "Filter type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Tap number", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Lower cutoff frequency", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Higher cutoff frequency", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuLicence.setTitle(QtGui.QApplication.translate("MainWindow", "Licence", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSample.setText(QtGui.QApplication.translate("MainWindow", "Sample", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow.setText(QtGui.QApplication.translate("MainWindow", "Show", None, QtGui.QApplication.UnicodeUTF8))

    def License(self):
        conf.Window2.show()
        conf.Window1.hide()

    def load(self):
        if self.dialog.selectedFilter() == "csv comma-separated values(*.csv)":
            conf.original = np.loadtxt(unicode(self.dialog.selectedFiles()[0]), delimiter=',').T

        elif self.dialog.selectedFilter() == "text file(*.txt)":
            conf.original = np.loadtxt(unicode(self.dialog.selectedFiles()[0]), delimiter=',').T

        elif self.dialog.selectedFilter() == "wav file(*.wav)":
            wr = wv.open(self.dialog.selectedFiles()[0], "rb")
            conf.Srate = wr.getframerate()
            conf.duration = float(wr.getnframes()) * 2.0 / float(wr.getframerate())
            data = wr.readframes(wr.getnframes())
            num_data = fromstring(data, dtype = int16)
            conf.original = np.linspace(0, conf.duration, wr.getnframes() * 2)
            conf.original = np.vstack((conf.original, np.r_[num_data[::2],num_data[1::2]]))

        elif self.dialog.selectedFilter() == "tsv tab-separated values(*.tsv)":
            conf.original = np.loadtxt(unicode(self.dialog.selectedFiles()[0]), delimiter='\t').T

        else:
            conf.original = np.loadtxt(unicode(self.dialog.selectedFiles()[0]), delimiter=',').T

        #print("\n[0][0:4]"+str(conf.original[0][0:4])+"\n\n[1]"+str(conf.original[1][0:4]))


    def reject(self):
        pass

    def open(self):
        self.dialog.show()

class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):#constructer. it is function. this function is called when the class was
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    conf.Window1 = ControlMainWindow()
    conf.Window2 = gui2.ControlDia()
    conf.Window1.show()
    sys.exit(app.exec_())