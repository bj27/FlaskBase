import json
import pyodbc
import os

class ODBCController():

    drive, tail = os.path.splitdrive(os.getcwd())
    connect = False
    cursor = False
    error = ""
    fields = []
    credential = ""

    isDefault = True
    internalId = 0

    def __init__(self):
        self.DRIVER = os.getenv("ALTERNATIVE_DRVER")
        self.HOST = os.getenv("ALTERNATIVE_HOST")
        self.PORT = os.getenv("ALTERNATIVE_PORT")
        self.DB = os.getenv("ALTERNATIVE_NAME")
        self.UID = os.getenv("ALTERNATIVE_USER")
        self.PWD = os.getenv("ALTERNATIVE_PASS")
        self.credential = 'DRIVER={%s};'%( self.DRIVER )
        self.credential += 'HOST=%s;'%( self.HOST )
        self.credential += 'PORT=%s;'%( self.PORT )
        self.credential += 'DB=%s;'%( self.DB )
        self.credential += 'UID=%s;'%( self.UID )
        self.credential += 'PWD=%s;'%( self.PWD )

    def preparateStringConnection(self):        
        self.credential = 'DRIVER={%s};'%( self.DRIVER )
        self.credential += 'HOST=%s;'%( self.HOST )
        self.credential += 'PORT=%s;'%( self.PORT )
        self.credential += 'DB=%s;'%( self.DB )
        self.credential += 'UID=%s;'%( self.UID )
        self.credential += 'PWD=%s;'%( self.PWD )
        #self.credential += 'PWD=ZZZZZ;'

    def preparateODBC(self):
        self.preparateStringConnection()
        self.error = ""
        try:
            print (self.credential)
            self.connect = pyodbc.connect(self.credential)
            self.connect.setencoding(encoding='utf-8')
            self.cursor = self.connect.cursor()
            return self.cursor

        except Exception as e:
            self.error = str(e)
            #self.sql = sql
            print("ERROR CONEXION", self.error )
            return False

    def printError(self):
        print (self.error)

    def execute( self, sql = "" , dictionary = False ):
        self.error = ""
        content = False
        if self.connect and self.cursor:
            sql = sql.lstrip()
            try:
                if sql.upper().startswith("INSERT"):
                    self.cursor.execute( sql )
                    content = True
                elif sql.upper().startswith("UPDATE"):
                    res = self.cursor.execute( sql )
                    content = True
                elif sql.upper().startswith("DELETE"):
                    self.cursor.execute( sql )
                    content = True
                else:
                    data = self.cursor.execute( sql )
                    #print("DATA",data)
                    self.fields = [column[0] for column in self.cursor.description]
                    #print(self.fields)
                    content = data.fetchall()
                    if dictionary:
                        data = []
                        for row in content:
                            tmp = {}
                            x = 0
                            for field in self.fields:
                                tmp[field] = '%s'%row[x]
                                x += 1
                            data.append(tmp)
                        content = data
                        #print(content)
                    return content
            except Exception as e:
                self.error = str(e)
                self.sql = sql
                print("ERROR SQL", self.error )
                return False
        return content

    def commit(self):
        if len(self.error) == 0:
            self.connect.commit()
            return True
        return False

    def close( self ):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()