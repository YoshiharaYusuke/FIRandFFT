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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTip("")
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_graph = QtGui.QVBoxLayout()
        self.verticalLayout_graph.setObjectName("verticalLayout_graph")
        self.graphicsView_signal = pg.PlotWidget()
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
        self.dialog.setModal(True)
        self.dialog.setDirectory(os.path.expanduser('~'))
        filters = ["csv comma-separated values(*.csv)", "text file(*.txt)", "tab tab-separated values(*.tsv)", "wav file(*.wav)", "All(*)"]  # File extention.
        self.dialog.setNameFilters(filters)
        QtCore.QObject.connect(self.dialog, QtCore.SIGNAL("accepted()"), self.load)
        QtCore.QObject.connect(self.dialog, QtCore.SIGNAL("rejected()"), self.reject)

        self.graphicsView_spectrum.setLogMode(x=1, y=1)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.open)
        QtCore.QObject.connect(self.actionSample, QtCore.SIGNAL("triggered()"), self.sample)
        QtCore.QObject.connect(self.comboBox_filter, QtCore.SIGNAL("currentIndexChanged(int)"), self.rePlot)
        QtCore.QObject.connect(self.doubleSpinBox_high, QtCore.SIGNAL("editingFinished()"), self.cutoff)
        QtCore.QObject.connect(self.doubleSpinBox_low, QtCore.SIGNAL("editingFinished()"), self.cutoff)
        QtCore.QObject.connect(self.spinBox_tap, QtCore.SIGNAL("editingFinished()"), self.tap)
        QtCore.QObject.connect(self.actionShow, QtCore.SIGNAL("triggered()"), self.License)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.spinBox_tap.setProperty("value", 101)
        self.spinBox_tap.setMinimum(1)
        self.spinBox_tap.setMaximum(9999999)
        self.spinBox_tap.setSingleStep(2)

        self.graphicsView_signal.addLegend(bkgnd=(0, 0, 0, 0), frame=(0, 0, 0, 255))
        self.graphicsView_spectrum.addLegend(bkgnd=(0, 0, 0, 0), frame=(0, 0, 0, 255))

        labelStyle = {'color': 'B', 'font-size': '14pt', 'font-family': 'Arial'}

        self.graphicsView_signal.setLabel("bottom", text="x", **labelStyle)
        self.graphicsView_signal.setLabel("left", text="y", **labelStyle)
        self.graphicsView_signal.addLine(y=0, pen=pg.mkPen([0, 0, 0]))  # Line at origin

        self.graphicsView_spectrum.setLabel("bottom", text="Frequency f", units="Hz",  **labelStyle)
        self.graphicsView_spectrum.setLabel("left", text="Amplitude", **labelStyle)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "FIRandFFT", None, QtGui.QApplication.UnicodeUTF8))
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
            num_data = fromstring(data, dtype=int16)
            conf.original = np.linspace(0, conf.duration, wr.getnframes() * 2)
            conf.original = np.vstack((conf.original, np.r_[num_data[::2], num_data[1::2]]))

        elif self.dialog.selectedFilter() == "tsv tab-separated values(*.tsv)":
            conf.original = np.loadtxt(unicode(self.dialog.selectedFiles()[0]), delimiter='\t').T

        else:
            conf.original = np.loadtxt(unicode(self.dialog.selectedFiles()[0]), delimiter=',').T

        self.start()

    def start(self):
        self.clearPlot()
        self.setProperty()
        self.plotOriginal()
        self.filter()
        self.plotFiltered()
        self.setInitialRegion()

    def setProperty(self):
        conf.num_samples = len(conf.original[0])
        conf.duration = conf.original[0][-1] - conf.original[0][0]
        conf.minfrq = 1.0 / conf.duration
        conf.Srate = 1.0 / (conf.original[0][-1] - conf.original[0][-2])
        conf.nyquist = conf.Srate / 2.0

        self.doubleSpinBox_high.setValue(conf.nyquist/1.1)
        self.doubleSpinBox_low.setValue(conf.minfrq*1.1)
        self.doubleSpinBox_high.setSingleStep(conf.minfrq)
        self.doubleSpinBox_low.setSingleStep(conf.minfrq)
        self.spinBox_tap.setMaximum(conf.num_samples)

    def reject(self):
        pass

    def sample(self):
        num = 10001
        frq1 = 1
        frq2 = 10
        frq3 = 100
        frq4 = 1000
        theta1 = np.linspace(0, 2*np.pi*frq1, num)
        theta2 = np.linspace(0, 2*np.pi*frq2, num)
        theta3 = np.linspace(0, 2*np.pi*frq3, num)
        theta4 = np.linspace(0, 2*np.pi*frq4, num)
        sin1 = np.sin(theta1)
        sin2 = np.sin(theta2)
        sin3 = np.sin(theta3)
        sin4 = np.sin(theta4)

        x = np.linspace(0, 1, num)
        y = sin1 + sin2 + sin3 + sin4
        conf.original = np.vstack((x, y))
        self.start()

    def open(self):
        self.dialog.show()

    def tap(self):
        if self.spinBox_tap.value() % 2 == 0:
            v = self.spinBox_tap.value() - 1
            self.spinBox_tap.setValue(v)
        self.rePlot()

    def plotOriginal(self):
        conf.p1 = self.graphicsView_signal.plot(conf.original[0], conf.original[1], name="Original signal")
        frq = np.linspace(0, conf.nyquist, int(np.floor(conf.num_samples / 2.0))) # + conf.minfrq / 10.0
        spectrum = abs(np.fft.fft(conf.original[1])[0:int(np.floor(conf.num_samples / 2.0))]) / len(conf.original[1]) * 2.0
        conf.p2 = self.graphicsView_spectrum.plot(frq[1::], spectrum[1::], name="FFT spectrum of the original signal")

    def plotFiltered(self):
        conf.p3 = self.graphicsView_signal.plot(conf.original[0], conf.filtered, name="Filtered signal", pen=[250, 0, 0, 100])
        frq = np.linspace(0, conf.nyquist, int(np.floor(conf.num_samples / 2.0))) # + conf.minfrq / 10.0
        spectrum = abs(np.fft.fft(conf.filtered)[0:int(np.floor(conf.num_samples / 2.0))]) / len(conf.original[1]) * 2.0
        conf.p4 = self.graphicsView_spectrum.plot(frq[1::], spectrum[1::], name="FFT spectrum of the filtered signal", pen=[250, 0, 0, 100])

    def clearPlot(self):
        self.graphicsView_signal.clear()
        self.graphicsView_spectrum.clear()

        self.clearLegend()

    def clearPlotFiltered(self):
        self.graphicsView_signal.removeItem(conf.p1)
        self.graphicsView_spectrum.removeItem(conf.p2)
        self.graphicsView_signal.removeItem(conf.p3)
        self.graphicsView_spectrum.removeItem(conf.p4)

        self.clearLegend()

    def clearLegend(self):
        self.graphicsView_signal.plotItem.legend.removeItem("Original signal")
        self.graphicsView_signal.plotItem.legend.removeItem("Filtered signal")
        self.graphicsView_spectrum.plotItem.legend.removeItem("FFT spectrum of the original signal")
        self.graphicsView_spectrum.plotItem.legend.removeItem("FFT spectrum of the filtered signal")

    def filter(self):
        if self.comboBox_filter.currentIndex() == 0:  # LP
            filtre = np.array(scsi.firwin(self.spinBox_tap.value(), self.doubleSpinBox_high.value(), nyq=conf.nyquist))
        elif self.comboBox_filter.currentIndex() == 1:  # HP
            filtre = np.array(scsi.firwin(self.spinBox_tap.value(), self.doubleSpinBox_high.value(), pass_zero=False, nyq=conf.nyquist))
        elif self.comboBox_filter.currentIndex() == 2:  # BP
            filtre = np.array(scsi.firwin(self.spinBox_tap.value(), [self.doubleSpinBox_low.value(), self.doubleSpinBox_high.value()], pass_zero=False, nyq=conf.nyquist))
        elif self.comboBox_filter.currentIndex() == 3:  # BS
            filtre = np.array(scsi.firwin(self.spinBox_tap.value(), [self.doubleSpinBox_low.value(), self.doubleSpinBox_high.value()], nyq=conf.nyquist))
        else:
            pass
        conf.filtered = np.convolve(conf.original[1], filtre, mode='same')

    def setInitialRegion(self):
        self.doubleSpinBox_low.setMinimum(conf.minfrq)
        self.doubleSpinBox_high.setMaximum(conf.nyquist)
        self.region = pg.LinearRegionItem(bounds=[self.doubleSpinBox_low.value(), self.doubleSpinBox_high.value()])
        self.region.setZValue(10)
        self.region.setBounds([np.log10(conf.minfrq), np.log10(conf.nyquist-conf.minfrq)])
        self.region.setRegion([np.log10(self.doubleSpinBox_low.value()), np.log10(self.doubleSpinBox_high.value())])
        self.region.sigRegionChanged.connect(self.regionRange)
        self.region.sigRegionChangeFinished.connect(self.regionRangeAndCal)
        self.midPoints()
        self.graphicsView_spectrum.addItem(self.region)

    def regionRange(self):
        v1, v2 = self.region.getRegion()
        self.doubleSpinBox_low.setValue(10**v1)
        self.doubleSpinBox_high.setValue(10**v2)
        self.midPoints()

    def regionRangeAndCal(self):
        v1, v2 = self.region.getRegion()
        self.doubleSpinBox_low.setValue(10**v1)
        self.doubleSpinBox_high.setValue(10**v2)
        self.midPoints()
        self.rePlot()

    def cutoff(self):
        self.setRegion()
        self.rePlot()

    def rePlot(self):
        self.clearPlotFiltered()
        self.plotOriginal()
        self.filter()
        self.plotFiltered()

    def setRegion(self):
        v1 = np.log10(self.doubleSpinBox_low.value())
        v2 = np.log10(self.doubleSpinBox_high.value())
        self.region.setRegion((v1, v2))
        self.midPoints()

    def midPoints(self):
        Lower_Cutoff = self.doubleSpinBox_low.value()
        Higher_Cutoff = self.doubleSpinBox_high.value()
        self.doubleSpinBox_high.setMinimum(Lower_Cutoff)
        self.doubleSpinBox_low.setMaximum(Higher_Cutoff)


class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    conf.Window1 = ControlMainWindow()
    conf.Window2 = gui2.ControlDia()
    conf.Window1.show()
    sys.exit(app.exec_())
