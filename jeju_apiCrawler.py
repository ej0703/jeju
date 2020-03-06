import requests
import xmltodict
import json

# 공공데이터포털 사이트로 크롤링 요청 위한 인증키와 요청 메세지
key = "y3hJyZd4gVr4xFzmKzqb53nioC68jdCSKnf8lZYuhvp9VOgSJ5N1GgtPP7fEVhcasTygTCSvigiqKj2syoMEyg%3D%3D"
url_cycle="http://openapi.jejusi.go.kr/rest/PublicBikeInfoService/getPublicBikeInfoList?ServiceKey={}&pageNo=1&numOfRows=10".format(key)
url_parking = "http://openapi.jejuits.go.kr/OPEN_API/pisInfo/getPisInfo?serviceKey={}&pageNo=1&numOfRows=100".format(key)

# 웹에 요청
content_cycle = requests.get(url_cycle).content
content_parking = requests.get(url_parking).content
# xml형식은 정보 분리하기 힘들어서 json으로 파싱
dict_cycle = xmltodict.parse(content_cycle)
dict_parking = xmltodict.parse(content_parking)
# json으로 변화된 정보를 구분해서 출력-공공자전거
jsonString_cycle = json.dumps(dict_cycle['rfcOpenApi']['body'], ensure_ascii = False)
jsonObj_cycle = json.loads(jsonString_cycle)

for list in jsonObj_cycle['data']['list']:
    print(list['address'],list['location'],list['retal_enable_num'])

print('\n')

# json으로 변화된 정보를 구분해서 출력-주차장
jsonString_parking = json.dumps(dict_parking['ServiceResult']['msgBody'], ensure_ascii = False)
jsonObj_parking = json.loads(jsonString_parking)

for list in jsonObj_parking['itemList']:
    print(list['ISTL_LCTN_ADDR'],list['WHOL_NPLS'],list['GNRL_RMND_PRZN_NUM'])