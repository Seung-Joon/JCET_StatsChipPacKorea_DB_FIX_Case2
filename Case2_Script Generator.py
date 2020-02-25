print("Initializing...")
import Case2_sql
import cx_Oracle
import pandas as pd
import pyperclip
import os
from pandas import Series, DataFrame

connectionString = {
    "user_ID": "rts",
    "user_PW": "rts4sck0",
    "database_IP": "10.20.20.56",
    "database_Port": "1521",
    "database_Sid": "SKCIMDWH",
} # DB 연결 정보



logFileString = {
    "file_path": 'C:\pythonTemp\\',
    "file_name": 'Case2_DataQueryLog.txt',
}# 로그파일 정보



#======= Fix Data 가공 함수 =======
def formatFixData(data):
    targetLotid = data[0][0]
    data = list(map(lambda x: [x[1], x[2]], data)) # COM_LOCATION, COM_LOT 데이터를 추출하여 재가공
    keys = list(set(list(map(lambda x: x[0], data)))) # COM_LOCATION 리스트 생성

    dataSets = {}
    for i in keys: dataSets[i] = []
    for j in data: dataSets[j[0]].append(j[1]) if (j != 'None') else ""

    fixData = {}
    for key in dataSets.keys():
        if None in dataSets[key]:
            dataSets[key] = list(filter(lambda x: x != None, dataSets[key]))
            fixData[key] = dataSets[key][0]
            
    return {targetLotid: fixData}


#======= 로그 기록 함수 =======
def log_FixedData(logFileString,fixData):
    import time
    if os.path.isdir(logFileString["file_path"]) == False: os.makedirs(logFileString["file_path"], exist_ok=True) #로그파일 디렉터리 확인
    filePath = logFileString["file_path"] + logFileString["file_name"]
    file = open(filePath, 'a')
    sysTime = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
    file.write(str([sysTime, fixData]) + ",\n")
    file.close

if __name__ == "__main__":
    targetLotid = input('Lotid 를 입력하세요. -> ') #LotID 입력
    print("데이터 조회중...")
    
    connection = Case2_sql.Db.initDbConnection(connectionString) #DB 연결
    dataSets = Case2_sql.Get.sqlGetData_case2DataList(connection, targetLotid) # 데이터 조회
    
    columns_id = ['LOTID', 'COM_LOCATION', 'COM_LOT', 'REEL_OPTION', 'REEL_OPTION']
    data = list(map(list, dataSets)) # COM_LOCATION 별 데이터를 리스트 형태로 저장함
    print(pd.DataFrame(data, columns=columns_id)) # 데이터 차트 표시
    
    fixData = formatFixData(data) # dataSets -> 가공 -> fixData

    buffer = ""
    buffer += Case2_sql.Format.formatSqlQuery_updateData(fixData) + "\n\n"
    buffer += Case2_sql.Format.formatSqlQuery_UpdateUTP(targetLotid) + "\n\n"
    buffer += Case2_sql.Format.formatSqlQuery_UpdateUTP_DataCheck(targetLotid) + "\n\n"
    pyperclip.copy(buffer) #스크립트 복사


    print("\n스크립트가 클립보드에 복사 되었습니다.")
    log_FixedData(logFileString,fixData)#로그 기록
    print("로그 기록됨.")
    input("press enter to terminate this generator->")

    
