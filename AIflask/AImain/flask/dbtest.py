import pymysql
 
  
def getEmps():
    ret = []
    db = pymysql.connect(host='localhost', user='ssafy', db='common_pjt', password='ssafy', charset='utf8')
    curs = db.cursor()
    
    sql = "select * from imgAi";
    curs.execute(sql)
    
    rows = curs.fetchall()
    for e in rows:
        temp = {'id':e[0],'img':e[1] }
        ret.append(temp)
    
    db.commit()
    db.close()
    return ret

 
if __name__ == '__main__':
    print(getEmps())











### 연결 테스트용
# db = pymysql.connect(host='localhost', user='ssafy', db='common_pjt', password='ssafy', charset='utf8')
# curs = db.cursor()


# sql = "select * from imgAi";

# curs.execute(sql)

# rows = curs.fetchall()
# print(rows)

# db.commit()
# db.close()