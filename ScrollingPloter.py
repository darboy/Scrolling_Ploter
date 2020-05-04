import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import re, time, os, sys
import numpy as np

class ScrollingPloter:
    def __init__(self, title_name, plot_num, x_data_num = 300, refresh_rate = 1):
        self.x_data_num = x_data_num
        self.title_name = title_name
        self.plot_num = plot_num
        self.refresh_rate = refresh_rate
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle(self.title_name)
        self.plot_array = []
        self.curve_array = []
        self.data_array = []
        self.timer_array = []
        self.slot_func_array = []
        self.func = []
        for i in range(0, plot_num):
            p = self.win.addPlot()
            p.showGrid(x=True,y=True)
            self.plot_array.append(p)
            init_data = np.zeros(x_data_num)
            self.data_array.append(init_data)
            curve = p.plot(self.data_array[i], pen="y", symbolBrush=(255,0,0), symbolPen='w')
            self.win.nextRow()
            self.curve_array.append(curve)
            self.func.append(self.noFunc)

    def noFunc(self):
        pass

    def setFunc(self, plot_index, func):
        self.timer = pg.QtCore.QTimer()
        self.func[plot_index] = func
        self.timer.timeout.connect(func)
        self.timer.start(1)

import serial
ser=serial.Serial("COM9",115200)
def update():
    data_str = ser.read(20).hex()
    print(int(data_str[12:16],16) / 10.0)
    x.data_array[0][:-1] = x.data_array[0][1:]
    x.data_array[0][-1] = (int(data_str[12:16],16) / 10.0)
    x.curve_array[0].setData(x.data_array[0])

x = ScrollingPloter("test", 1)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()