import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui



class anplot:
    def __init__(self,layout,xaxis, yaxis, name,xname,yname,pos,key):

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOption('background', 'w')


        self.key = key
        self.pw = pg.PlotWidget()
        self.pw.setTitle(name)

      #  self.legend = 0
        self.pw.setLabel('bottom', text=xname)
        self.pw.setLabel('left', text=yname)
       # self.legend = self.pw.addLegend()

        layout.addWidget(self.pw,pos[0],pos[1])


        self.x = xaxis
        self.y = yaxis




        self.data = self.pw.plot(x=self.x, y=self.y)






