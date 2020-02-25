import cx_Oracle       

class Format:
    def formatSqlQuery_getDataTableByLotid(lotid):
        sql = ""
        sql += "SELECT DISTINCT  --M.STRIP_ID," + "\n"
        sql += "\tM.A_LOT_ID,"
        sql += "\tD.COM_LOCATION,D.COM_LOT,D.COM_PART,D.REEL_OPTION" + "\n"
        sql += "FROM T_KSY_RUNLOTSTRIP_CUR M  , CCM.T_SIP_CCM_D_SG D" + "\n"
        sql += "WHERE M.A_LOT_ID IN (\'" + lotid + "\')" + "\n"
        sql += "\tAND M.STRIP_ID=D.STRIP_ID" + "\n"
        sql += "\tAND D.COM_PART LIKE 'C%'" + "\n"
        sql += "order by 1,2"
        return sql

    def formatSqlQuery_updateData(fixData):
        targetLotId = list(fixData.keys())[0]
        fixDataFrame = list(fixData.values())[0]
        fixDataFrameKey = list(fixDataFrame.keys())
        
        sql = ""
        sql += "update CCM.T_SIP_CCM_D_SG D"
        sql += "\n\t" + "set com_lot=decode(com_location,"
        for key in fixDataFrameKey:
            sql += "\n\t\t" + '\'' + key + '\', \'' + fixDataFrame[key] + '\'' + ','
        sql += "\n\t" + "null),REEL_OPTION=\'RECOVER\'"
        sql += "\n" + "WHERE strip_id in (select strip_id from t_ksy_runlotstrip_cur where A_LOT_ID = \'" + targetLotId + '\')'
        sql += "\n\t" + "and com_location IN ("
        for index in range(len(fixDataFrameKey)):
            sql += '\'' + fixDataFrameKey[index] + '\''
            if index != len(fixDataFrameKey) - 1:
                sql += ','
        sql += ")"
        sql += "\n\t" + "AND COM_LOT IS NULL;"
        return sql

    def formatSqlQuery_UpdateUTP(lotid):
        import time
        from random import randint
        
        sql = ""
        sql += "UPDATE UPTDAT@LINK_CPKMES1" + '\n'
        sql += "\tSET DATA1 = \' \'," + '\n'
        
        sql += "\t    DATA3 = \' \'," + '\n'
        sql += "\t    DATA5 = \'Resend:" + time.strftime('%Y-%m-%d', time.localtime(time.time())) + "\'" + "," + "\n"
        sql += "\t    DATA10 = "  + '\'' + str(randint(1, 3)) + '\',' + "\n"
        sql += "\t    RESV_FIELD1 = \' \'," + '\n'
        sql += "\t    RESV_FIELD2 = \' \'," + '\n'
        sql += "\t    RESV_FIELD3 = \' \'" + '\n'
        sql += "WHERE FACTORY=\'ASSEMBLY\'" + "\n"
        sql += "\tAND TABLE_NAME = \'QUL_GENEALOGY_LOT\'" + "\n"
        sql += "\tAND KEY1 IN (\'" + lotid + '\');'
        sql += '\n'
        return sql

    def formatSqlQuery_UpdateUTP_DataCheck(lotid):
        sql = ""
        sql += "SELECT * FROM UPTDAT@LINK_CPKMES1 " 
        sql += "WHERE FACTORY=\'ASSEMBLY\' " 
        sql += "AND TABLE_NAME = \'QUL_GENEALOGY_LOT\' "
        sql += "AND KEY1 IN(\'" + lotid + "\');"
        return sql


class Get:
    def sqlGetData_case2DataList(connection, lotid):
        cursor = connection.cursor()
        cursor.execute(Format.formatSqlQuery_getDataTableByLotid(lotid))
        return cursor
        #for data in cursor: print(data)
          
class Db:
    def initDbConnection(connectionString):
       return cx_Oracle.connect(connectionString["user_ID"],
                                connectionString["user_PW"],
                                connectionString["database_IP"] + ":" + connectionString["database_Port"] + "/" + connectionString["database_Sid"])

   
