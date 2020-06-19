import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui



class plot:
    def __init__(self,layout, parent=None):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOption('background', 'w')



        self.pw = pg.PlotWidget()

        self.legend = 0
        self.pw.setLabel('bottom', text='Time(s)')
        self.legend = self.pw.addLegend()

        layout.addWidget(self.pw)

        self.x = []




        #self.one = self.pw.plot(x=self.x, y=self.y, name = 'test 1')

        #self.two = self.pw.plot(x=self.x, y=self.y1, name = 'test 2')




