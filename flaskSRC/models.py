import mysql.connector

class DBManger:
    def __init__(self, database='Movie_Sys', host='db',port= '3306', user= 'root', password='root'):
        #file = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user= user,
            password = password,
            host = host,
            database=database,
            auth_plugin='mysql_native_password')
        self.cursor = self.connection.cursor()
        #self.cursor.execute('CREATE DATABASE MARKS;')
        self.cursor.execute('DROP TABLE IF EXISTS Account;')
        self.cursor.execute('''CREATE TABLE Account (username VARCHAR(50) NOT NULL PRIMARY KEY,
                                password VARCHAR(250) NOT NULL,
                                age Int NOT NULL,
                                gender VARCHAR(10) NOT NULL);''')
        self.connection.commit()

    def insertAccount (self, account):
        insert_stmt = "INSERT INTO Account (username,password,age,gender)  VALUES (%s, %s, %s, %s ) ;"
        try:
            self.cursor.execute(insert_stmt, (account['username'], account['password'], account['age'], account['gender']))
            self.connection.commit()
        except Exception as e:
            return e
        
        return None
    
    def findUserByUsername(self, username):
        stmt = "select * from Account where username=%s;"
        account = None
        try:
            self.cursor.execute(stmt, (username,))
            account = self.cursor.fetchall()
        except Exception as e:
            return None, e
        return account, None

    def findUser(self ):

        stmt = "select * from Account;"
        self.cursor.execute(stmt)
        name_lis = self.cursor.fetchall()
        return name_lis

if __name__ == "__main__":
    db = DBManger()
    dic1 = {
            "username": "ty1",
            "password": "passward",
            "age": 12,
            "gender": "Male"}
    
    dic2 = {
            "username": "ty2",
            "password": "passward",
            "age": 12,
            "gender": "Male"}
    db.insertAccount(dic1)
    db.insertAccount(dic2)
    
    print(db.findUserByUsername())
