# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem

import requests
import xmltodict
import json
import folium
import pandas as pd 
import io
import sys
import functools

class Ui_Carcycle(object):
    def setupUi(self, Carcycle):
        Carcycle.setObjectName("Carcycle")
        Carcycle.resize(1080, 900)
        Carcycle.setStyleSheet("background-color:rgb(255,255,219) ")

        #실시간현황 label
        self.cbLbl = QtWidgets.QLabel(Carcycle)
        self.cbLbl.setGeometry(QtCore.QRect(30, 20, 298, 60))
        self.cbLbl.setPixmap(QPixmap('실시간현황.png'))
        self.cbLbl.setObjectName("cbLbl")
       
        #실시간현황label밑 line
        self.line = QtWidgets.QFrame(Carcycle)
        self.line.setGeometry(QtCore.QRect(20, 80, 241, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #실시간 주차장 현황 tablewidget
        self.carTable = QtWidgets.QTableWidget(Carcycle)
        self.carTable.setGeometry(QtCore.QRect(520, 170, 500, 255))
        self.carTable.setRowCount(8)
        self.carTable.setColumnCount(5)
        self.carTable.setObjectName("carTable")
        car_colum_headers = ['주차장명','주소','총 주차 수','잔여 자리','장애인 잔여 자리'] #테이블 헤더
        self.carTable.setHorizontalHeaderLabels(car_colum_headers)
        self.carTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.carTable.setStyleSheet("background-color:rgb(255,255,255) ")
        
        #실시간 주차장 현황 label
        self.carLbl = QtWidgets.QLabel(Carcycle)
        self.carLbl.setGeometry(QtCore.QRect(20, 110, 320, 42))
        self.carLbl.setPixmap(QPixmap('실시간주차장현황.png'))
        self.carLbl.setObjectName("carLbl")
                
        #실시간 주차장 현황 map
        self.car_webEngineView = QtWebEngineWidgets.QWebEngineView(Carcycle)
        self.car_webEngineView.setGeometry(QtCore.QRect(10, 160, 500, 301))
        self.car_webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.car_webEngineView.setObjectName("car_webEngineView")
       
        #주차장 검색 button
        self.carBtn = QtWidgets.QPushButton(Carcycle)
        self.carBtn.setGeometry(QtCore.QRect(930, 130, 90, 30))
        self.carBtn.clicked.connect(self.call_parking_api)
        self.carBtn.setIcon(QtGui.QIcon("검색1.png"))
        self.carBtn.setStyleSheet("background-color:rgb(255,255,244) ")
        self.carBtn.setIconSize(QtCore.QSize(40,25))
        self.carBtn.setObjectName("carBtn")

        #실시간 자전거 현황 label
        self.cycleLbl = QtWidgets.QLabel(Carcycle)
        self.cycleLbl.setGeometry(QtCore.QRect(20, 480, 287, 44))
        self.cycleLbl.setPixmap(QPixmap('실시간자전거현황.png'))
        self.cycleLbl.setObjectName("cycleLbl")
        
        #실시간 자전거 현황 table
        self.cycleTable = QtWidgets.QTableWidget(Carcycle)
        self.cycleTable.setGeometry(QtCore.QRect(520, 530, 500, 295))
        self.cycleTable.setRowCount(9)
        self.cycleTable.setColumnCount(3)
        self.cycleTable.setObjectName("cycleTable")
        colum_headers = ['주소 ','위치 ','잔여 대여 자리'] #테이블 헤더
        self.cycleTable.setHorizontalHeaderLabels(colum_headers)
        self.cycleTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cycleTable.setStyleSheet("background-color:rgb(255,255,255) ")
       
        #자전거 검색 button
        self.cycleBtn = QtWidgets.QPushButton(Carcycle)
        self.cycleBtn.setGeometry(QtCore.QRect(925, 485, 90, 30))
        self.cycleBtn.setIcon(QtGui.QIcon("검색1.png"))
        self.cycleBtn.setStyleSheet("background-color:rgb(255,255,244) ")
        self.cycleBtn.setIconSize(QtCore.QSize(40,25))
        self.cycleBtn.setObjectName("cycleBtn")
        self.cycleBtn.clicked.connect(self.call_cycle_api)
        
        #자전거 실시간 현황 map
        self.cycle_webEngineView = QtWebEngineWidgets.QWebEngineView(Carcycle)
        self.cycle_webEngineView.setGeometry(QtCore.QRect(10, 530, 500, 301))
        self.cycle_webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.cycle_webEngineView.setObjectName("cycle_webEngineView")

        self.retranslateUi(Carcycle)
        QtCore.QMetaObject.connectSlotsByName(Carcycle)

    def retranslateUi(self, Carcycle):
        _translate = QtCore.QCoreApplication.translate
        Carcycle.setWindowTitle(_translate("Carcycle", "실시간 주차장 자전거 현황"))


    def call_parking_api(self):

        key = "y3hJyZd4gVr4xFzmKzqb53nioC68jdCSKnf8lZYuhvp9VOgSJ5N1GgtPP7fEVhcasTygTCSvigiqKj2syoMEyg%3D%3D"
        url_parking = "http://openapi.jejuits.go.kr/OPEN_API/pisInfo/getPisInfo?serviceKey={}&pageNo=1&numOfRows=100".format(key)

        content_parking = requests.get(url_parking).content

        dict_parking = xmltodict.parse(content_parking)

        #제주도맵 folium에 불러오기
        jeju_map = folium.Map(location=[33.389398,126.541236], tiles='stamen Terrain',zoom_start=9)


        jsonString_parking = json.dumps(dict_parking['ServiceResult']['msgBody'], ensure_ascii=False)
        jsonObj_parking = json.loads(jsonString_parking)
        
        df_park = pd.DataFrame(jsonObj_parking['itemList'])
        df_park = df_park.loc[:,['ISTL_LCTN_ADDR','WHOL_NPLS','GNRL_RMND_PRZN_NUM']]

        # 지도에 위치를 마킹하기 위해 x,y좌표를 수동으로 입력해줌
        df_p1 = pd.DataFrame({'x':[33.516518,33.504720,33.494673,33.494823,33.249802,33.512080,33.512090,33.5159351]}) # x좌표 lat
        df_p2 = pd.DataFrame({'y':[126.525296,126.541789,126.535459,126.535294,126.562276,126.528340,126.528215,126.5287851]}) # y좌표 lon

        #좌표를 리스트에 추가함
        df_park = pd.concat([df_park,df_p1],axis=1)
        df_park = pd.concat([df_park,df_p2],axis=1)
        print(df_park) # 최종 리스트 출력

        # for문을 반복하여 주차장의 위치를 지도에 마킹 + 설명과 잔여 주차가능 대수를 확인할수있음.
        for x , y , name, num in zip(df_park.x , df_park.y , df_park.ISTL_LCTN_ADDR ,df_park.GNRL_RMND_PRZN_NUM):
            if int(num) < 10:
                folium.CircleMarker([x,y],
                         radius=4,
                         color='red',
                         fill=True,
                         fill_color='red',
                         fill_opacity=0.7,
                         popup=name+num
                       ).add_to(jeju_map)  # 10대 미만은 적색등.
        
            elif int(num) < 20:
                folium.CircleMarker([x,y],
                         radius=4,
                         color='orange',
                         fill=True,
                         fill_color='orange',
                         fill_opacity=0.7,
                         popup=name+num
                       ).add_to(jeju_map) # 10~20대 미만은 주황등.
            
            else :
                folium.CircleMarker([x,y],
                         radius=4,
                         color='green',
                         fill=True,
                         fill_color='green',
                         fill_opacity=0.7,
                         popup=name+num
                       ).add_to(jeju_map) # 20대 이상은 초록등.

        #HTML 파일로 저장    
        jeju_map.save('./jeju_park.html')
        
        #HTML파일 map으로 나타내기
        url = QtCore.QUrl.fromLocalFile('C:/Users/60414/source/repos/PythonPJ1/PythonPJ1/jeju_park.html')
        self.car_webEngineView.load(url)
    


        #크롤링한 값을 리스트에 입력 & 딕셔너리로 변경
        result1=[]
        result2=['제주시 삼도이동 1192-8',
                    '제주시 일도이동 409-11',
                    '제주시 이도2동 1066',
                    '제주시 이도2동 1992-7',
                    '서귀포시 서귀동 291-3',
                    '제주시 일도1동 1230-5',
                    '제주시 일도1동 1103',
                    '제주 제주시 건입동 1328-6']
        result3=[]
        result4=[]
        result5=[]

        for list in jsonObj_parking['itemList']:
            result1.append(list['ISTL_LCTN_ADDR'])
            result3.append(list['WHOL_NPLS'])
            result4.append(list['GNRL_RMND_PRZN_NUM'])
            result5.append(list['HNDC_RMND_PRZN_NUM'])

        parking = {
            'name' : result1,
            'addr' : result2,
            'npls' : result3,
            'gnrl_num' : result4,
            'hndc_num' : result5
        }
        
       
        #주차장 테이블에 값 입력
        column_idx_loockup = {'name':0, 'addr':1, 'npls':2, 'gnrl_num':3,'hndc_num':4}
       
        for k, v in parking.items():
            col = column_idx_loockup[k]
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                self.carTable.setItem(row, col, item)
        self.carTable.resizeColumnToContents(1)

        #잔여 자리 수에 따라 컬럼색 변경
        for row in range(7):
            item1 = QtWidgets.QTableWidgetItem(result4[row])
            if int(result4[row]) < 10:
                item1.setBackground(QtGui.QColor(255,76,76))
            elif int(result4[row]) < 20:
                item1.setBackground(QtGui.QColor(255,183,77))
            else:
                item1.setBackground(QtGui.QColor(152,251,152))

            self.carTable.setItem(row,3,item1)
       
        #장애인 잔여 자리 수에 따라 컬럼색 변경
        for row in range(7):
            item1 = QtWidgets.QTableWidgetItem(result5[row])
            if int(result5[row]) < 3:
                item1.setBackground(QtGui.QColor(255,76,76))
            elif int(result5[row]) < 5:
                item1.setBackground(QtGui.QColor(255,183,77))
            else:
                item1.setBackground(QtGui.QColor(152,251,152))
            self.carTable.setItem(row,4,item1)

    def call_cycle_api(self):  
        
        key = "y3hJyZd4gVr4xFzmKzqb53nioC68jdCSKnf8lZYuhvp9VOgSJ5N1GgtPP7fEVhcasTygTCSvigiqKj2syoMEyg%3D%3D"
        url_cycle="http://openapi.jejusi.go.kr/rest/PublicBikeInfoService/getPublicBikeInfoList?ServiceKey={}&pageNo=1&numOfRows=10".format(key)

        content_cycle = requests.get(url_cycle).content

        dict_cycle = xmltodict.parse(content_cycle)

        #제주도맵 folium에 불러오기
        jeju_map = folium.Map(location=[33.389398,126.541236], tiles='stamen Terrain',zoom_start=9)

        jsonString_cycle = json.dumps(dict_cycle['rfcOpenApi']['body'], ensure_ascii = False)
        jsonObj_cycle = json.loads(jsonString_cycle)

        df_cycle = pd.DataFrame(jsonObj_cycle['data']['list'])

        # 지도에 위치를 마킹하기 위해 x,y좌표를 수동으로 입력해줌
        df_c1 = pd.DataFrame({'x':[33.4845,33.4889,33.4908,33.4794,33.4852,33.4753,33.5112,33.5004,33.4998]}) # x좌표 lat
        df_c2 = pd.DataFrame({'y':[126.5007,126.4906,126.4866,126.4772,126.4882,126.5154,126.5432,126.5297,126.5178]}) # y좌표 lon

        #좌표를 리스트에 추가함
        df_cycle = pd.concat([df_cycle,df_c1],axis=1)
        df_cycle = pd.concat([df_cycle,df_c2],axis=1)
        print(df_cycle)# 최종 리스트 출력

        # for문을 반복하여 자전거대여소의 위치를 지도에 마킹 + 설명과 잔여 대여 대수를 확인할수있음.
        for x , y , loc, num in zip(df_cycle.x , df_cycle.y , df_cycle.location ,df_cycle.retal_enable_num):
            if int(num) == 0:
                folium.CircleMarker([x,y],
                         radius=4,
                         color='red',
                         fill=True,
                         fill_color='red',
                         fill_opacity=0.7,
                         popup=loc+num
                       ).add_to(jeju_map)  # 대여가능 대수가 0대일시 적색등.
        
            elif int(num) < 5:
                folium.CircleMarker([x,y],
                         radius=4,
                         color='orange',
                         fill=True,
                         fill_color='orange',
                         fill_opacity=0.7,
                         popup=loc+num
                       ).add_to(jeju_map) #  5대 미만은 주황등.
            
            else :
                folium.CircleMarker([x,y],
                         radius=4,
                         color='green',
                         fill=True,
                         fill_color='green',
                         fill_opacity=0.7,
                         popup=loc+num
                       ).add_to(jeju_map) # 5대 이상은 초록등.

           
        #HTML 파일로 저장   
        jeju_map.save('./jeju_cycle.html')      
        #HTML 파일 map에 불러오기
        url = QtCore.QUrl.fromLocalFile('C:/Users/60414/source/repos/PythonPJ1/PythonPJ1/jeju_cycle.html')
        self.cycle_webEngineView.load(url)
    
        #크롤링한 값을 리스트에 입력 & 딕셔너리로 변경
        result1_=[]
        result1=[]
        result2=[]
        result3=[]

        for list in jsonObj_cycle['data']['list']:
            result1_ = '제주시 '+ list['address']
            result1.append(result1_)
            result2.append(list['location'])
            result3.append(list['retal_enable_num'])
        
        cycle = {
            'cyadd' : result1,
            'cylocat' : result2,
            'cyretal' : result3
        }

        column_idx_loockup = {'cyadd':0, 'cylocat':1, 'cyretal':2}

        #자전거 정보 table에 나타내기
        for k, v in cycle.items():
            col = column_idx_loockup[k]
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                self.cycleTable.setItem(row, col, item)
        
        self.cycleTable.resizeColumnToContents(1)

        #자전거 잔여 대수에 따른 컬럼색 변경
        for row in range(9):
            item1 = QtWidgets.QTableWidgetItem(result3[row])
            if int(result3[row]) == 0:
                item1.setBackground(QtGui.QColor(255,76,76))
            elif int(result3[row]) <5:
                item1.setBackground(QtGui.QColor(255,183,77))
            else:
                item1.setBackground(QtGui.QColor(152,251,152))
            
            self.cycleTable.setItem(row,2,item1)
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Carcycle = QtWidgets.QWidget()
    ui = Ui_Carcycle()
    ui.setupUi(Carcycle)
    Carcycle.show()
    sys.exit(app.exec_())
