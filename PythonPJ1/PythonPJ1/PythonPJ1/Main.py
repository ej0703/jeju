# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap

from Car_cycle import Ui_Carcycle
from Info import Ui_infoWidget


class Ui_mainForm(object):
    def setupUi(self, mainForm):
        mainForm.setObjectName("mainForm")
        mainForm.resize(1080, 900)
        mainForm.move(300,50)
        mainForm.setStyleSheet("background-color:rgb(200,231,244) ")

        #제주도 관광지도 button
        self.infoBtn = QtWidgets.QPushButton(mainForm)
        self.infoBtn.setGeometry(QtCore.QRect(150, 30, 180, 70))
        self.infoBtn.setIcon(QtGui.QIcon("관광지도btn1.png"))
        self.infoBtn.setStyleSheet("background-color:rgb(255,255,244) ")
        self.infoBtn.setIconSize(QtCore.QSize(160,60))
        self.infoBtn.setObjectName("infoBtn")
        self.infoBtn.clicked.connect(self.click_infoBtn)
        #주차장 자전거 현황 button
        self.carBtn = QtWidgets.QPushButton(mainForm)
        self.carBtn.setGeometry(QtCore.QRect(450, 30, 181, 71))
        self.carBtn.setObjectName("carBtn")
        self.carBtn.setIcon(QtGui.QIcon("주차장자전거.png"))
        self.carBtn.setStyleSheet("background-color:rgb(255,255,244) ")
        self.carBtn.setIconSize(QtCore.QSize(160,60))
        self.carBtn.clicked.connect(self.click_carBtn)

        #종료 button
        self.exitBtn = QtWidgets.QPushButton(mainForm)
        self.exitBtn.setGeometry(QtCore.QRect(750, 30, 180, 70))
        self.exitBtn.setObjectName("exitBtn")
        self.exitBtn.clicked.connect(QCoreApplication.instance().quit)      
        self.exitBtn.setIcon(QtGui.QIcon("종료btn.png"))
        self.exitBtn.setStyleSheet("background-color:rgb(255,255,244) ")
        self.exitBtn.setIconSize(QtCore.QSize(170,60))
        
        self.widget = QtWidgets.QWidget(mainForm)
        self.widget.setGeometry(QtCore.QRect(-10, 120, 1080, 780))
        self.widget.setObjectName("widget")

        #travel_jeju label
        self.mainLbl = QtWidgets.QLabel(self.widget)
        self.mainLbl.setGeometry(QtCore.QRect(380, 20, 421, 71))
        self.mainLbl.setPixmap(QPixmap('travel_jeju.png'))
        self.mainLbl.setObjectName("mainLbl")

        #워드클라우드
        self.wordcloudLbl = QtWidgets.QLabel(self.widget)
        self.wordcloudLbl.setGeometry(QtCore.QRect(300, 200, 500, 500))
        self.wordcloudLbl.setPixmap(QPixmap('wordcloud2.png'))
        self.wordcloudLbl.setObjectName("wordcloudLbl")

        #클라우드 출처
        self.cloudLbl = QtWidgets.QLabel(self.widget)
        self.cloudLbl.setGeometry(QtCore.QRect(630, 600, 200, 81))
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.cloudLbl.setFont(font)
        self.cloudLbl.setObjectName("cloudLbl")

        #파도그림 삽입
        self.surfLbl = QtWidgets.QLabel(self.widget)
        self.surfLbl.setGeometry(QtCore.QRect(300, 82, 500, 88))
        self.surfLbl.setPixmap(QPixmap('surf1.png'))
        self.surfLbl.setObjectName("surfLbl")

        self.retranslateUi(mainForm)
        QtCore.QMetaObject.connectSlotsByName(mainForm)

    def retranslateUi(self, mainForm):
        _translate = QtCore.QCoreApplication.translate
        mainForm.setWindowTitle(_translate("mainForm", "제주도 관광 "))
        self.cloudLbl.setText(_translate("Form", "출처 : 제주여행장소. csv"))

    #info button클릭시 이벤트
    def click_infoBtn(self):
        self.infowidget = QtWidgets.QWidget()
        self.ui1 = Ui_infoWidget()
        self.ui1.setupUi(self.infowidget)
        self.infowidget.show()
    #car button클릭시 이벤트
    def click_carBtn(self):
        self.carWidget = QtWidgets.QWidget()
        self.ui2 = Ui_Carcycle()
        self.ui2.setupUi(self.carWidget)
        self.carWidget.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainForm = QtWidgets.QWidget()
    infoWidget = QtWidgets.QWidget()
    carWidget = QtWidgets.QWidget()
    ui = Ui_mainForm()
    ui.setupUi(mainForm)
    mainForm.show()
    sys.exit(app.exec_())

