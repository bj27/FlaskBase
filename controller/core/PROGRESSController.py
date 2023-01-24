from controller.core.ODBCController import ODBCController

class PROGRESSController():

    fields = []
    odbc = False
    content = []
    internalId = 1
    error = ""
    sql = ""

    def generateInstance(self):
        self.odbc = ODBCController()
        self.odbc.isDefault = False
        self.odbc.internalId = self.internalId
        self.odbc.cursor = self.odbc.preparateODBC() 
        self.error = self.odbc.error
        return self.odbc.cursor
    
    def execute(self, sql = "", dictionary = False ):
        response = []
        if sql.upper().lstrip().startswith("SELECT"):
            sql += " WITH (NOLOCK) "
        if self.odbc.cursor :
            response = self.odbc.execute(sql, dictionary )
            self.error = self.odbc.error
            self.fields = self.odbc.fields
        else:
            self.error = 'Problemas de conexion'
            self.fields = []
        self.sql = sql

        return response

    def printError(self):
        self.odbc.printError()
    
    def commit(self):
        return self.odbc.commit()

    def close( self ):
        self.odbc.close()

    # def querySelectSubstring(self, record = "", fieldname = ""):
    #     if record and fieldname:
    #         if not fieldname == "*":
    #             odbc = MYSQLController()
    #             odbc.preparateMySQL()
    #             sql = """
    #                     SELECT t1.COL COL, IFNULL(t2.COLTYPE,t1.COLTYPE) COLTYPE, IFNULL(t2.WIDTH,t1.WIDTH) WIDTH
    #                     FROM `progress_describetables` t1 
    #                     LEFT JOIN progress_replacedescribetables t2 ON t2.ID = t1.ID and t2.TBL = t1.TBL and t2.COL = t1.COL
    #                     WHERE t1.TBL = '%s'
    #                     AND t1.COL = '%s'
    #                 """%(record, fieldname)
    #             response = odbc.execSQL(sql)
    #             if response:
    #                 for row in response:
    #                     if row.get("COLTYPE") == "varchar":
    #                         fieldname = " SUBSTRING(%s, %s,%s) '%s' "%( row.get("COL"), 1, row.get("WIDTH"), row.get("COL"))
    #             odbc.closeMySQL()
    #     return fieldname

    def selectGeneric(self, params, clasic_response=False):
        sFields = []
        tName = ""
        wFields = []
        if params.get("tableName"):
            tName = params.get("tableName")
        if tName:
            if params.get("selectFields"):
                sFields = params.get("selectFields")
            if sFields:
                sql  = " select "
                tmp = ""
                for irow in sFields:
                    if not tmp:
                        tmp += "  %s "%(self.querySelectSubstring(tName, irow))
                    else:
                        tmp += " ,%s "%(self.querySelectSubstring(tName, irow))
                sql += tmp
                if not tName in ("SYSTABLES","SYSCOLUMNS"):
                    sql += ' FROM pub."%s" '%( tName )
                else:
                    sql += ' FROM "%s" '%( tName )
                wsql = ""
                if params.get("whereFields"):
                    wFields = params.get("whereFields")
                    for wrow in wFields.keys():
                        if not wsql:
                            wsql += " WHERE "
                        else:
                            wsql += " AND "
                        wsql += " %s = '%s' "%( wrow , wFields.get(wrow) )
                    sql += " %s "%( wsql)
                self.generateInstance()
                content = self.execute( sql )
                if not clasic_response:
                    if not content: response = {}
                    else:
                        response = content
                        content = []
                        for rrow in response:
                            tmp = {}
                            count = 0
                            tmp["rowNr"] = count
                            for srow in sFields:
                                tmp[srow] = rrow[count]
                                count += 1
                            content.append( tmp )
                    # response = {"data" : content, "message" : self.error, "query" : sql if self.error else ""}
                    response = {"data" : content, "message" : self.error,  "length" : len(content) if content else 0, "query" : sql }   # COMENTAR AL REALIZAR EL PASE A PRODUCTIVO
                else:
                    response = content
                self.close()
                return response

    # def syncShowTables(self):
    #     params = {"selectFields":["ID","TBL","CREATOR","OWNER","TBLTYPE"],"tableName":"SYSTABLES"}
    #     response = self.selectGeneric( params, True )
    #     if response:
    #         mdata = MasiveDataController()
    #         mdata.instanceName = self.__class__.__name__
    #         if len(response) > 0 : 
    #             odbc = MYSQLController()
    #             odbc.preparateMySQL()
    #             sql  = " TRUNCATE progress_showtables "
    #             odbc.execSQL(sql)
    #             odbc.commit()
    #             odbc.closeMySQL()
    #             response = mdata.generateFile(params.get("selectFields"), response)
    #             if response:
    #                 mdata.nameTable = "progress_showtables"
    #                 mdata.uploadFileMassive(True)

    # def syncDescribeTables(self):
    #     odbc = MYSQLController()
    #     odbc.preparateMySQL()
    #     sql  = " SELECT * FROM progress_showtables "
    #     res_show_tables = odbc.execSQL(sql)
    #     if res_show_tables:
    #         sql  = " TRUNCATE progress_describetables "
    #         odbc.execute(sql)
    #         odbc.commit()
    #         for irow in res_show_tables:
    #             params = {"selectFields":["ID","COL","TBL","COLTYPE","WIDTH","CHARSET","COLLATION"],"tableName":"SYSCOLUMNS","whereFields": {"TBL": irow.get("TBL")}}
    #             response = self.selectGeneric( params, True )
    #             if response:
    #                 mdata = MasiveDataController()
    #                 mdata.instanceName = self.__class__.__name__
    #                 if len(response) > 0 : 
    #                     response = mdata.generateFile(params.get("selectFields"), response)
    #                     if response:
    #                         mdata.nameTable = "progress_describetables"
    #                         mdata.uploadFileMassive(True)

    #     odbc.close()