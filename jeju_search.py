import pymysql
import pandas as pd

#DB 연동 -MySQL
conn = pymysql.connect(host='34.64.133.169', user='root', password='1234', db='jeju', charset='utf8')

#Connection 으로부터 Dictoionary Cursor 생성
curs = conn.cursor(pymysql.cursors.DictCursor)

#버튼 이벤트로 받은 단어를 받을 변수(임시로 그냥 프롬프트에서 입력받는 것으로 했음)
search=input()

#SQL문으로 검색(필요하다고 생각한 정보만 검색했음)
sql = "select x, y, category, loc_name, tel, address from jeju where category like '%"+search+"%'"+" or loc_name like '%"+search+"%';"
curs.execute(sql)

#데이타 Fetch
rows = curs.fetchall()
for row in rows:
    #print(row) #해당 로우들 전체 출력
    print(row['category'], row['loc_name'], row['tel'], row['address'])

# 검색결과 csv 파일 저장
dataframe = pd.DataFrame(rows)
dataframe.to_csv("검색결과.csv",header=False, index=False, encoding ='euc-kr')
 
#Connection 닫기
conn.close()