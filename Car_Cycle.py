# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem
import requests
import xmltodict
import json

class Ui_Carcycle(object):
    def setupUi(self, Carcycle):
        Carcycle.setObjectName("Carcycle")
        Carcycle.resize(1080, 900)
        self.cbLbl = QtWidgets.QLabel(Carcycle)
        self.cbLbl.setGeometry(QtCore.QRect(30, 20, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)

        self.cbLbl.setFont(font)
        self.cbLbl.setObjectName("cbLbl")
        self.line = QtWidgets.QFrame(Carcycle)
        self.line.setGeometry(QtCore.QRect(20, 70, 241, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.carTable = QtWidgets.QTableWidget(Carcycle)
        self.carTable.setGeometry(QtCore.QRect(520, 170, 500, 235))
        self.carTable.setRowCount(7)
        self.carTable.setColumnCount(3)
        self.carTable.setObjectName("carTable")
        car_colum_headers = ['주차장명','총 주차 수','잔여 자리']
        self.carTable.setHorizontalHeaderLabels(car_colum_headers)
        self.carTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.carLbl = QtWidgets.QLabel(Carcycle)
        self.carLbl.setGeometry(QtCore.QRect(20, 130, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.carLbl.setFont(font)
        self.carLbl.setObjectName("carLbl")

        self.carBtn = QtWidgets.QPushButton(Carcycle)
        self.carBtn.setGeometry(QtCore.QRect(930, 132, 91, 31))
        self.carBtn.clicked.connect(self.call_parking_api)
        self.carBtn.setObjectName("carBtn")
        

        self.cycleTable = QtWidgets.QTableWidget(Carcycle)
        self.cycleTable.setGeometry(QtCore.QRect(520, 530, 500, 295))
        self.cycleTable.setRowCount(9)
        self.cycleTable.setColumnCount(3)
        self.cycleTable.setObjectName("cycleTable")
        colum_headers = ['주소 ','위치 ','잔여 대여 자리']
        self.cycleTable.setHorizontalHeaderLabels(colum_headers)
        self.cycleTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
       
        self.cycleBtn = QtWidgets.QPushButton(Carcycle)
        self.cycleBtn.setGeometry(QtCore.QRect(930, 490, 91, 31))
        self.cycleBtn.setObjectName("cycleBtn")
        self.cycleBtn.clicked.connect(self.call_cycle_api)
        

        self.cycleLbl = QtWidgets.QLabel(Carcycle)
        self.cycleLbl.setGeometry(QtCore.QRect(20, 490, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.cycleLbl.setFont(font)
        self.cycleLbl.setObjectName("cycleLbl")

        self.retranslateUi(Carcycle)
        QtCore.QMetaObject.connectSlotsByName(Carcycle)

    def retranslateUi(self, Carcycle):
        _translate = QtCore.QCoreApplication.translate
        Carcycle.setWindowTitle(_translate("Carcycle", "Form"))
        self.cbLbl.setText(_translate("Carcycle", "실시간 현황"))
        self.carLbl.setText(_translate("Carcycle", "실시간 주차장 현황"))
        self.carBtn.setText(_translate("Carcycle", "검색"))
        self.cycleBtn.setText(_translate("Carcycle", "검색"))
        self.cycleLbl.setText(_translate("Carcycle", "실시간 자전거 현황"))


    def call_parking_api(self):

        key = "y3hJyZd4gVr4xFzmKzqb53nioC68jdCSKnf8lZYuhvp9VOgSJ5N1GgtPP7fEVhcasTygTCSvigiqKj2syoMEyg%3D%3D"
        url_parking = "http://openapi.jejuits.go.kr/OPEN_API/pisInfo/getPisInfo?serviceKey={}&pageNo=1&numOfRows=100".format(key)

        content_parking = requests.get(url_parking).content

        dict_parking = xmltodict.parse(content_parking)

        jsonString_parking = json.dumps(dict_parking['ServiceResult']['msgBody'], ensure_ascii=False)
        jsonObj_parking = json.loads(jsonString_parking)
        
        result1=[]
        result2=[]
        result3=[]

        for list in jsonObj_parking['itemList']:
            result1.append(list['ISTL_LCTN_ADDR'])
            result2.append(list['WHOL_NPLS'])
            result3.append(list['GNRL_RMND_PRZN_NUM'])

        parking = {
            'name' : result1,
            'npls' : result2,
            'przn_num' : result3
        }
        print(parking)

        column_idx_loockup = {'name':0, 'npls':1, 'przn_num':2}

        for k, v in parking.items():
            col = column_idx_loockup[k]
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                if (col == 2):
                    item.setForeground(QBrush(QtCore.Qt.red))
                self.carTable.setItem(row, col, item)
        self.carTable.resizeColumnToContents(1)


    def call_cycle_api(self):  
        
        key = "y3hJyZd4gVr4xFzmKzqb53nioC68jdCSKnf8lZYuhvp9VOgSJ5N1GgtPP7fEVhcasTygTCSvigiqKj2syoMEyg%3D%3D"
        url_cycle="http://openapi.jejusi.go.kr/rest/PublicBikeInfoService/getPublicBikeInfoList?ServiceKey={}&pageNo=1&numOfRows=10".format(key)

        content_cycle = requests.get(url_cycle).content

        dict_cycle = xmltodict.parse(content_cycle)

        jsonString_cycle = json.dumps(dict_cycle['rfcOpenApi']['body'], ensure_ascii = False)
        jsonObj_cycle = json.loads(jsonString_cycle)

        result1_=[]
        result1=[]
        result2=[]
        result3=[]
        for list in jsonObj_cycle['data']['list']:
            result1_ = '제주시 ' + list['address']
            result1.append(result1_)
            result2.append(list['location'])
            result3.append(list['retal_enable_num'])

        cycle = {
            'cyadd' : result1,
            'cylocat' : result2,
            'cyretal' : result3
        }
        print(cycle)

        column_idx_loockup = {'cyadd':0, 'cylocat':1, 'cyretal':2}

        for k, v in cycle.items():
            col = column_idx_loockup[k]
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                self.cycleTable.setItem(row, col, item)
        
        self.cycleTable.resizeColumnToContents(0)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Carcycle = QtWidgets.QWidget()
    ui = Ui_Carcycle()
    ui.setupUi(Carcycle)
    Carcycle.show()
    sys.exit(app.exec_())