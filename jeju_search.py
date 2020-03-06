import pymysql

#MySQL이랑 연결 한 거, db 저장한 거에 따라 내용 변경해서 사용할 것
conn = pymysql.connect(host='localhost', user='root', password='1234', db='jeju_info', charset='utf8')

# Connection 으로부터 Dictoionary Cursor 생성
curs = conn.cursor(pymysql.cursors.DictCursor)

#버튼 이벤트로 받은 단어를 받을 변수(임시로 그냥 프롬프트에서 입력받는 것으로 했음)
search=input()

#SQL문으로 검색(필요하다고 생각한 정보만 검색했음)
sql = "select category, loc_name, tel, address from jeju where category like '%"+search+"%'"+" or loc_name like '%"+search+"%';"
curs.execute(sql)

# 데이타 Fetch
rows = curs.fetchall()
for row in rows:
    #print(row)
    print(row['category'], row['loc_name'], row['tel'], row['address'])
 
# Connection 닫기
conn.close()