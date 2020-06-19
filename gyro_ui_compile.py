from PyQt5 import uic

def convert():
    fp = open('gui.py', "w", encoding="utf-8")
    uic.compileUi('input.ui', fp)
    fp.close()
convert()