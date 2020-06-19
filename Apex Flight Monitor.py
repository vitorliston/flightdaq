from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QFileDialog, QApplication, QSystemTrayIcon, QSplashScreen
from PyQt5.QtGui import QPixmap, QIcon, QQuaternion
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtCore, QtWidgets
import random
import sys
from gyro import GyroApp

from os import path, getcwd, listdir, environ, remove
import time
from Connect import connect

from plot import plot
import pyqtgraph as pg
from functools import partial
from gui import Ui_MainWindow
import random
from analysisplot import anplot


class AppWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)

        self.time = {'Time': [0]}
        self.speed = {'Abs': [0], 'Horizontal': [0], 'Vertical': [0], 'Angular': [0], 'Top': [0]}
        self.acceleration = {'Abs': [0], 'Horizontal': [0], 'Vertical': [0], 'Angular': [0], 'Top': [0]}
        self.position = {'Abs': [0], 'Horizontal': [0], 'Altitude': [0], 'Latitude': [0], 'Longitude': [0]}
        self.health = {'Coms': [0], 'Parachute': [0], 'T1': [0], 'T2': [0], 'Pressure': [0]}
        self.orientation = {'Pitch': [0], 'Roll': [0], 'Yaw': [0]}

        self.data = {'Speed': self.speed, 'Acceleration': self.acceleration, 'Position': self.position,
                     'Health': self.health, 'Time': self.time, 'Orientation': self.orientation}

        self.stages = {'Ignition': False, 'TF': False, 'FF': False, 'Apogee': False, 'FD': False, 'Parachute': False,
                       'PD': False, 'Ground': False}
        self.receiverdata = {}

        self.receiverdata_index = {}



        self.numberofplots = 0
        self.analysisplotsnames = []

        self.plotposition = {'1': [0, 0, False], '2': [1, 0, False], '3': [0, 1, False], '4': [1, 1, False],
                             '5': [0, 2, False], '6': [1, 2, False]}

        for key in list(self.data.keys()):
            for subkey in list(self.data[key].keys()):
                self.analysisplotsnames.append(str(key) + '.' + str(subkey))

        self.serial = None
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.gyro = GyroApp(self.ui.gyrolayout)
        self.gyro.rocketTransform.setRotation(QQuaternion.fromEulerAngles(-90, 0, 0))
        self.Connect()
        self.plot = plot(self.ui.plotlayout)

        self.ui.xaxisname.addItems(self.analysisplotsnames)
        self.ui.yaxisname.addItems(self.analysisplotsnames)
        self.analysisplots = {}
        self.listofplots = {}
        self.listoflegends = {}
        self.ui.sabsch.stateChanged.connect(partial(self.Plotitem, self.ui.sabsch, 'Speed', 'Abs'))
        self.ui.sverch.stateChanged.connect(partial(self.Plotitem, self.ui.sverch, 'Speed', 'Vertical'))
        self.ui.sangch.stateChanged.connect(partial(self.Plotitem, self.ui.sangch, 'Speed', 'Angular'))
        self.ui.shorch.stateChanged.connect(partial(self.Plotitem, self.ui.shorch, 'Speed', 'Horizontal'))

        self.ui.baddplot.clicked.connect(self.createplot)
        self.ui.bdelplot.clicked.connect(self.deleteplot)
        self.ui.bopenlog.clicked.connect(self.reorganizeplots)

        self.ui.data1.addItem('None')
        self.ui.data2.addItem('None')
        self.ui.data3.addItem('None')
        self.ui.data4.addItem('None')
        self.ui.data5.addItem('None')
        self.ui.data6.addItem('None')
        self.ui.data7.addItem('None')
        self.ui.data8.addItem('None')
        self.ui.data9.addItem('None')
        self.ui.data10.addItem('None')
        self.ui.data11.addItem('None')
        self.ui.data12.addItem('None')


        for key in list(self.data.keys()):
            for subkey in list(self.data[key].keys()):
                self.ui.data1.addItem(key+"."+subkey)
                self.ui.data2.addItem(key + "." + subkey)
                self.ui.data3.addItem(key + "." + subkey)
                self.ui.data4.addItem(key + "." + subkey)
                self.ui.data5.addItem(key + "." + subkey)
                self.ui.data6.addItem(key + "." + subkey)
                self.ui.data7.addItem(key + "." + subkey)
                self.ui.data8.addItem(key + "." + subkey)
                self.ui.data9.addItem(key + "." + subkey)
                self.ui.data10.addItem(key + "." + subkey)
                self.ui.data11.addItem(key + "." + subkey)
                self.ui.data12.addItem(key + "." + subkey)

        self.ui.data1.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data1, 0))
        self.ui.data2.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data2, 1))
        self.ui.data3.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data3, 2))
        self.ui.data4.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data4, 3))
        self.ui.data5.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data5, 4))
        self.ui.data6.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data6, 5))
        self.ui.data7.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data7, 6))
        self.ui.data8.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data8, 7))
        self.ui.data9.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data9, 8))
        self.ui.data10.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data10, 9))
        self.ui.data11.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data11, 10))
        self.ui.data12.currentTextChanged.connect(partial(self.setDataIndex, self.ui.data12, 11))





    @QtCore.pyqtSlot(str)
    def setDataIndex(self,combobox, index):
       if combobox.currentText!='':
        self.receiverdata_index[combobox.currentText()]=index
        self.clearallvectors()







    def Connect(self):
        test = True
        if not test:
            serialport = connect()
        else:
            serialport = 111
        if serialport is not None:

            self.worker = WorkerObject(serialport)
            self.worker.start()

            self.worker.signalStatus.connect(self.Process_data)

            self.ui.statusBar.showMessage(str(serialport), 10000)
        else:

            self.ui.statusBar.showMessage('Not connected', 10000)

    def Plotitem(self, checkbox, major, minor):

        if checkbox.isChecked():

            try:
                self.listofplots[major + '.' + minor] = self.plot.pw.plot(x=self.data['Time']['Time'],
                                                                          y=self.data[major][minor],
                                                                          name=major + '.' + minor,
                                                                          pen=pg.mkPen(
                                                                              "%06x" % random.randint(0, 0xFFFFFF),
                                                                              width=2))
            except:
                pass

        else:
            try:
                self.plot.pw.removeItem(self.listofplots[major + '.' + minor])
                del (self.listofplots[major + '.' + minor])
                self.plot.legend.removeItem(major + '.' + minor)
            except:
                pass

    def Updategui(self, data):  # sets and processes gui data
        if self.data['Speed']['Abs']!=[]:
            self.ui.sabsval.setText(str(self.data['Speed']['Abs'][-1]))
        if self.data['Speed']['Vertical'] !=[]:
            self.ui.sverval.setText(str(self.data['Speed']['Vertical'][-1]))
        if self.data['Speed']['Horizontal'] !=[]:
            self.ui.shorval.setText(str(self.data['Speed']['Horizontal'][-1]))
        if self.data['Speed']['Angular'] !=[]:
            self.ui.sangval.setText(str(self.data['Speed']['Angular'][-1]))
        if self.data['Speed']['Top'] !=[]:
            self.ui.stopval.setText(str(self.data['Speed']['Top'][-1]))
        if self.data['Acceleration']['Abs'] !=[]:
            self.ui.aabsval.setText(str(self.data['Acceleration']['Abs'][-1]))
        if self.data['Acceleration']['Vertical'] !=[]:
            self.ui.averval.setText(str(self.data['Acceleration']['Vertical'][-1]))
        if self.data['Acceleration']['Horizontal'] !=[]:
            self.ui.ahorval.setText(str(self.data['Acceleration']['Horizontal'][-1]))
        if self.data['Acceleration']['Angular'] !=[]:
            self.ui.aangval.setText(str(self.data['Acceleration']['Angular'][-1]))
        if self.data['Acceleration']['Top'] !=[]:
            self.ui.atopval.setText(str(self.data['Acceleration']['Top'][-1]))

        if self.data['Position']['Abs'] !=[]:

            self.ui.pabsval.setText(str(self.data['Position']['Abs'][-1]))
        if self.data['Position']['Altitude'] !=[]:
            self.ui.paltval.setText(str(self.data['Position']['Altitude'][-1]))
        if self.data['Position']['Horizontal'] !=[]:
            self.ui.phorval.setText(str(self.data['Position']['Horizontal'][-1]))
        if self.data['Position']['Latitude'] !=[]:
            self.ui.latitudeval.setText(str(self.data['Position']['Latitude'][-1]))
        if self.data['Position']['Longitude'] !=[]:
            self.ui.longval.setText(str(self.data['Position']['Longitude'][-1]))
        if self.data['Orientation']['Roll'] !=[]:

            self.ui.orolval.setText(str(self.data['Orientation']['Roll'][-1]))
        if self.data['Orientation']['Pitch'] !=[]:
            self.ui.opitval.setText(str(self.data['Orientation']['Pitch'][-1]))
        if self.data['Orientation']['Yaw'] !=[]:
            self.ui.oyawval.setText(str(self.data['Orientation']['Yaw'][-1]))



        try:
            self.plot.pw.setTitle('T +' + str(data[0]))
        except:
            pass
        try:
            self.gyro.rocketTransform.setRotation(QQuaternion.fromEulerAngles(data[0], data[1], data[2]))
        except:
            pass
        for key in list(self.listofplots.keys()):
            key = key.split('.')

            self.listofplots[key[0] + '.' + key[1]].setData(x=self.time['Time'], y=self.data[key[0]][key[1]],
                                                            clear=True)

    def Process_data(self, data):  # função principal para processamento dos dados

        self.ui.consolewin.append(data)  # insere os dados recebidos no console
        data = data.split(',')  # separa em lista
        del data[-1]
        data = [round(float(i), 2) for i in data]

        try:
            self.Updategui(data)  # atualiza interface
        except:
            pass

        for key in list(self.receiverdata_index.keys()):
            item = data[self.receiverdata_index[key]]

            # acessa o valor da lista de dados que corresponde a key  item = data[receiverdata_index[Speed.Absolute]]
            # receiverdata_index[Speed.Absolute] retorna o index da Speed.Absolute na lista de dados

            self.receiverdata[key] = item
            key = key.split('.')
            self.data[key[0]][key[1]].append(item)


    def clearallvectors(self):
        for key in list(self.data.keys()):
            for subkey in list(self.data[key].keys()):
                self.data[key][subkey].clear()


    def createplot(self):

        for key in list(self.plotposition.keys()):
            if self.plotposition[key][2] == False:

                xname = str(self.ui.xaxisname.currentText())
                yname = str(self.ui.yaxisname.currentText())
                x = xname.split(".")
                y = yname.split(".")

                if str(self.ui.plotname.text()) != '':
                    self.analysisplots[str(self.ui.plotname.text())] = anplot(self.ui.flightanlayout,
                                                                              self.data[x[0]][x[1]],
                                                                              self.data[y[0]][y[1]],
                                                                              str(self.ui.plotname.text()), xname,
                                                                              yname, self.plotposition[key], key)
                    self.ui.listdelplot.addItem(str(self.ui.plotname.text()))
                if str(self.ui.plotname.text()) == '':
                    name = yname + " x " + xname
                    self.analysisplots[name] = anplot(self.ui.flightanlayout, self.data[x[0]][x[1]],
                                                      self.data[y[0]][y[1]], name, xname, yname, self.plotposition[key],
                                                      key)
                    self.ui.listdelplot.addItem(name)

                self.plotposition[key][2] = True

                return

        # self.plot.one.setData(x=self.plot.x, y=self.plot.y, clear=True,pen=pg.mkPen('b', width=2))

        # self.plot.two.setData(x=self.plot.x, y=self.plot.y1, clear=True,pen=pg.mkPen('r', width=2))

    def deleteplot(self):

        try:

            self.plotposition[self.analysisplots[str(self.ui.listdelplot.currentText())].key][2] = False
            self.analysisplots[str(self.ui.listdelplot.currentText())].pw.close()
            # self.ui.flightanlayout.removeWidget(self.analysisplots[str(self.ui.listdelplot.currentText())].pw)
            # self.analysisplots.addWidget(self.analysisplots[str(self.ui.listdelplot.currentText())].pw, 0,0)

            del (self.analysisplots[str(self.ui.listdelplot.currentText())])
            index = self.ui.listdelplot.findText(str(self.ui.listdelplot.currentText()), QtCore.Qt.MatchFixedString)
            self.ui.listdelplot.removeItem(index)

            self.reorganizeplots()

        except:
            pass

    def clearall(self):
        for plot in list(self.analysisplots.keys()):
            self.analysisplots[plot].pw.close()

    def reorganizeplots(self):

        for key in list(self.plotposition.keys()):
            self.plotposition[key][2] = False

        for i in reversed(range(self.ui.flightanlayout.count())):
            widgetToRemove = self.ui.flightanlayout.itemAt(i).widget()
            # remove it from the layout list
            self.ui.flightanlayout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
        for key in list(self.analysisplots.keys()):
            for pos in list(self.plotposition.keys()):
                if self.plotposition[pos][2] == False:
                    self.ui.flightanlayout.addWidget(self.analysisplots[key].pw, self.plotposition[pos][0],
                                                     self.plotposition[pos][1])
                    self.plotposition[pos][2] = True
                    break


class WorkerObject(QThread):
    signalStatus = pyqtSignal(str)

    def __init__(self, serialport, parent=None):
        QThread.__init__(self)

        self.serialConnection = serialport
        self.rawdata = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                        '0', '0', '0', '0', '0']
        self.savedata = False
        self.datafile = None
        self.testvariable = 0
        self.test = True

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            self.serialread()
            self.feed_data()

    def feed_data(self):
        time.sleep(0.5)

        dataemit = ''
        for data in self.rawdata:
            dataemit += str(data) + ","

        self.signalStatus.emit(dataemit)

    def serialread(self):  # retrieve data

        if not self.test:
            self.rawdata = self.serialConnection.readline().decode('utf-8').strip('\r\n').split(',')

        else:
            self.rawdata = [self.testvariable, 15.09 * self.testvariable, 17.58 * self.testvariable,
                            13.988 * self.testvariable, 2.08 * self.testvariable,
                            13.05 * self.testvariable, 25.22 * self.testvariable, 66.89 * self.testvariable,
                            0.568 * self.testvariable, 78 * self.testvariable,
                            14 * self.testvariable, 7.05 * self.testvariable, self.testvariable,
                            15.09 * self.testvariable, 17.58 * self.testvariable, 13.988 * self.testvariable,
                            2.08 * self.testvariable,
                            13.05 * self.testvariable, 25.22 * self.testvariable, 66.89 * self.testvariable,
                            0.568 * self.testvariable, 78 * self.testvariable,
                            14 * self.testvariable, 7.05 * self.testvariable]
            self.testvariable += 1
        if self.savedata == True and self.oldtime != self.rawdata[0]:
            self.datafile.write(','.join(self.rawdata) + '\n')
            self.oldtime = self.rawdata[0]


app = QApplication(sys.argv)

w = AppWindow()
w.setWindowIcon(QIcon('apex.png'))

splash_pix = QPixmap('apex.png')
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
splash.setMask(splash_pix.mask())
splash.show()

app.processEvents()
# time.sleep(0.8)
w.show()

splash.finish(w)

sys.exit(app.exec_())
