# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Info.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
import pymysql
import pandas as pd
import matplotlib as plt
import folium
import functools
import io
import sys

class Ui_infoWidget(object):

    def setupUi(self, infoWidget):
        infoWidget.setObjectName("infoWidget")
        infoWidget.resize(1080, 900)
        infoWidget.move(350,50)
        infoWidget.setStyleSheet("background-color:rgb(255,255,219) ")

        #제주도광광지도 label
        self.infoLbl = QtWidgets.QLabel(infoWidget)
        self.infoLbl.setGeometry(QtCore.QRect(50, 20, 392, 60))
        self.infoLbl.setPixmap(QPixmap('제주도관광지도.png'))
        self.infoLbl.setObjectName("cbLbl")

        #제주도 관광지 검색결과 나타내는 table
        self.tableWidget = QtWidgets.QTableWidget(infoWidget)
        self.tableWidget.setGeometry(QtCore.QRect(430, 590, 600, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        table_colum_headers = ['분류','이름','전화번호','주소']
        self.tableWidget.setHorizontalHeaderLabels(table_colum_headers)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setStyleSheet("background-color:rgb(255,255,255) ")

        #검색 button
        self.searchBtn = QtWidgets.QPushButton(infoWidget)
        self.searchBtn.setGeometry(QtCore.QRect(960, 555, 70, 30))
        self.searchBtn.setObjectName("searchBtn")
        self.searchBtn.setIcon(QtGui.QIcon("검색1.png"))
        self.searchBtn.setStyleSheet("background-color:rgb(255,255,244) ")
        self.searchBtn.setIconSize(QtCore.QSize(40,25))
        self.searchBtn.clicked.connect(self.click_search)

        #검색창 
        self.lineEdit = QtWidgets.QLineEdit(infoWidget)
        self.lineEdit.setGeometry(QtCore.QRect(655, 555, 300, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("background-color:rgb(255,255,255) ")

        #제주도 관광 map
        self.info_webEngineView = QtWebEngineWidgets.QWebEngineView(infoWidget)
        self.info_webEngineView.setGeometry(QtCore.QRect(60, 90, 971, 441))
        self.info_webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.info_webEngineView.setObjectName("info_webEngineView")

        #귤하르방 그림 삽입
        self.imageLbl = QtWidgets.QLabel(infoWidget)
        self.imageLbl.setGeometry(QtCore.QRect(70, 620, 300, 222))
        self.imageLbl.setPixmap(QPixmap('귤하르방.png'))
        self.imageLbl.setObjectName("imageLbl")

        self.retranslateUi(infoWidget)
        QtCore.QMetaObject.connectSlotsByName(infoWidget)




    def retranslateUi(self, infoWidget):
        _translate = QtCore.QCoreApplication.translate
        infoWidget.setWindowTitle(_translate("infoWidget", "제주도 관광 지도"))
        


    def click_search(self):
        
        #DB 연동 -MySQL
        conn = pymysql.connect(host='34.64.133.169', user='root', password='1234', db='jeju', charset='utf8')

        #Connection 으로부터 Dictoionary Cursor 생성
        curs = conn.cursor(pymysql.cursors.DictCursor)

        search = self.lineEdit.text()

        #SQL문으로 검색(필요하다고 생각한 정보만 검색했음)
        sql = "select x as x, y as y, category as category, loc_name as loc_name, tel as tel, address as address from jeju where category like '%"+search+"%'"+" or loc_name like '%"+search+"%';"
        curs.execute(sql)

        #데이타 Fetch
        rows = curs.fetchall()

        #DB에서 가져온 값을 리스트에 입력 & 딕셔너리로 변경
        self.tableWidget.setRowCount(len(rows)) 

        result1 =[]
        result2 =[]
        result3 =[]
        result4 =[]

        for row in rows:
            result1.append(row['category'])
            result2.append(row['loc_name'])
            result3.append(row['tel'])
            result4.append(row['address'])
            dataframe = pd.DataFrame(rows)
            dataframe.to_csv("jeju_info.csv",header=None, index=False, encoding ='euc-kr')

        
        info = {
            'category' : result1,
            'loc_name' : result2,
            'tel' : result3,
            'address' : result4
        }

        #검색한 DB table에 나타내기
        column_idx_loockup = {'category':0, 'loc_name':1, 'tel':2, 'address':3}

        for k, v in info.items():
            col = column_idx_loockup[k]
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                self.tableWidget.setItem(row, col, item)
        self.tableWidget.resizeColumnToContents(1)
        

        #idx_col = 'category' # 인덱스를 종류구분체계 열로 지정
        
        df =pd.read_csv('jeju_info.csv',encoding='euc-kr', names=['x','y','category','loc_name','tel','addr'])


        print("---------------------------------------------------------------")
        pd.set_option('display.width',None)
        pd.set_option('display.max_rows',100)
        pd.set_option('display.max_columns',10)
        pd.set_option('display.max_colwidth',20)
        pd.set_option('display.unicode.east_asian_width',True)

        print(df)

        # 지도에 위치 표시
        jeju_map = folium.Map(location=[33.389398,126.541236], tiles='stamen Terrain', zoom_start=10)
 
        for name, lat, lng in zip(df.loc_name, df.x, df.y):
            folium.CircleMarker([lat,lng],
                                 radius=3,
                                 color='brown',
                                 fill=True,
                                 fill_color='coral',
                                 fill_opacity=0.7,
                                 popup=name
                               ).add_to(jeju_map)

        # HTML 파일로 저장  
        jeju_map.save('./jeju_locationEX.html')
       
        # HTML 파일 map으로 나타내기
        url = QtCore.QUrl.fromLocalFile('C:/Users/60414/source/repos/PythonPJ1/PythonPJ1/jeju_locationEX.html')
        self.info_webEngineView.load(url)
    

        conn.close()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    infoWidget = QtWidgets.QWidget()
    ui = Ui_infoWidget()
    ui.setupUi(infoWidget)
    infoWidget.show()
    sys.exit(app.exec_())

