import requests
import xmltodict
import json

# 공공데이터포털 사이트로 크롤링 요청 위한 인증키와 요청 메세지
# 우선은 페이지 수와 출력 줄 수 설정 안 해둠
key = "wGCosOLwUd0xyA6jmnIMi4dbtYCJYKBl6Af8HjuCMhPGi9tprfPpeG9FjrJWOdopp2pfZgg4ChyhAb%2FRgMvIRg%3D%3D"
url = "http://openapi.jejusi.go.kr/rest/PublicBikeInfoService/getPublicBikeInfoList?ServiceKey={}".format(key)

# 웹에 요청
content = requests.get(url).content
# xml형식은 정보 분리하기 힘들어서 json으로 파싱
dict = xmltodict.parse(content)
# json으로 변화된 정보를 구분해서 출력
jsonString = json.dumps(dict['rfcOpenApi']['body'], ensure_ascii = False)
jsonObj = json.loads(jsonString)

for list in jsonObj['data']['list']:
    print(list['address'],list['location'],list['retal_enable_num'])