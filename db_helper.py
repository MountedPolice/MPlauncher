import mysql.connector
import time

class dbline:
    def __init__(self,date, user, operand, operation, operand2, result):
        self.date = date
        self.user = user
        self.operand = operand
        self.operation = operation
        self.operand2 = operand2
        self.result = result

class dbClient:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def get_table(self, lines):
        actiontab = self._select_fetchall('Actions')
        j = 0
        conn = mysql.connector.connect(host=self.host,
                                       port=self.port,
                                       database=self.database,
                                       user=self.user,
                                       password=self.password)
        curs = conn.cursor()
        for i in actiontab:
            temp = []
            temp.append(i[1].__str__())
            message = "SELECT Username FROM MainCALCDB.User WHERE (`idUser` = '"+ str(i[2]) + "');"
            curs.execute(message)

            userid = curs.fetchall()
            user = userid[0][0]

            temp.append(user)

            curs.execute("SELECT * FROM MainCALCDB.Action WHERE (`idAction` = '"+ str(i[3]) + "');")
            action = (curs.fetchall())
            temp.append(action[0][1])
            temp.append(action[0][2])
            temp.append(action[0][3])
            temp.append(action[0][4])
            lines.append(temp)
            j = j+1;
        return lines



    def add_log_line_math(self, user, operation):
        try:
            conn = mysql.connector.connect(host=self.host,
                                           port=self.port,
                                           database=self.database,
                                           user=self.user,
                                           password=self.password)
            curs = conn.cursor()
            curs.execute("INSERT INTO `MainCALCDB`.`Action` (`Operation`, `Operand1`, `Operand2`, `Result`) VALUES ('"+ operation[1] +"',"
                         " '"+operation[0] + "', '"+  operation[2]+"', '"+ operation[4] +"');")
            conn.commit()
            curs.execute("SELECT idAction FROM MainCALCDB.Action ORDER BY idAction DESC LIMIT 1;")
            freeid = curs.fetchall()
            freeid = freeid[0][0]
            curs.execute("SELECT idUser FROM MainCALCDB.User WHERE (`Username` = '"+ user + "');")
            userid = (curs.fetchall())
            userid = userid[0][0]
            curs.execute("INSERT INTO `MainCALCDB`.`Actions` (`Date`, `UserID`, `ActionID`) VALUES (NOW"
                         "(), '"+ str(userid)+"', '" +str(freeid)+"');")
            conn.commit()
            curs.close()
            conn.disconnect()
        except mysql.connector.errors.InterfaceError:
            print('DB connection error')
        except mysql.connector.errors.InterfaceError:
            print('unex')

    def _select_fetchall(self, table):
        try:
            conn = mysql.connector.connect(host=self.host,
                                           port=self.port,
                                           database=self.database,
                                           user=self.user,
                                           password=self.password)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM " + self.database + "." + table)
            tab = cursor.fetchall()
            cursor.close()
            conn.disconnect()
            return tab
        except mysql.connector.errors.InterfaceError:
            lprint('DB connection error')
            return []
        except:
            lprint('DB unexpected error')
            return []


def lprint(message):
    print(time.asctime() + ' ' + str(message))
