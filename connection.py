import mysql.connector

class Connection():

    #defining function to connect the database
    def getConn():
        my_database = mysql.connector.connect(
            host='127.0.0.1',
            user='username', 
            password='userpassword',
            database='STUDENT',
        )
        return my_database


    #Closing the connection
    def closeConn(con):
        con.close()