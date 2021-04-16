import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self,corpus,mot,parent=None):
        QMainWindow.__init__(self,parent)
        self.traitement=(True,-1)
        self.mot=mot
        self.corpus=corpus.split('\r')
        self.pos=mot[1][0]
        self.i=0
        self.resize(600,500)
        toolBar=QToolBar("Navigation")
        self.addToolBar(toolBar)
        actNext=QAction("Next",self)
        actPrevious=QAction("Previous",self)
        actAll=QAction("All",self)
        actOne=QAction("One",self)
        actOK=QAction("OK",self)

        actOK.triggered.connect(self.end)
        actNext.triggered.connect(self.next)
        actPrevious.triggered.connect(self.previous)
        actAll.triggered.connect(self.all)
        actOne.triggered.connect(self.one)
        toolBar.addAction(actPrevious)
        toolBar.addAction(actNext)
        toolBar.addAction(actAll)
        toolBar.addAction(actOne)
        toolBar.addAction(actOK)
        self.centralWidget=QTextEdit()
        line=self.corpus[self.pos[0]].split()
        s=" "
        line[self.pos[1]]="<span style=\"color:red \">"+line[self.pos[1]]+"</span>"
        line = s.join(line)
        self.centralWidget.setHtml(line)
        self.setCentralWidget(self.centralWidget)


    def next(self):
        if(self.i+1>len(self.mot[1])):
            self.i=0
        else:
            self.i+=1
        line=self.corpus[self.pos[0]].split()
        s=" "
        self.pos=self.mot[1][self.i]
        line[self.pos[1]]="<span style=\"color:red \">"+line[self.pos[1]]+"</span>"
        line = s.join(line)
        self.centralWidget.setHtml(line)

    def previous(self):
        if(self.i-1>0):
            self.i=len(self.mot[1])-1
        else:
            self.i-=1

        line=self.corpus[self.pos[0]].split()
        s=" "
        self.pos=self.mot[1][self.i]
        line[self.pos[1]]="<span style=\"color:red \">"+line[self.pos[1]]+"</span>"
        line = s.join(line)
        self.centralWidget.setHtml(line)

    def one(self):
        self.traitement=(False,self.i)

    def all(self):
        self.traitement=(True,-1)

    def end(self):
        self.close()
