from os import getenv
import mysql.connector



dbhost=getenv("sqlhost")
dbuser=getenv("sqluser")
dbpass=getenv("sqlpass1")
dbdata=getenv("sqldata")


db=mysql.connector.connect (    host="34.142.92.109" ,  
                                user="root", 
                                password="root", 
                                database="tournament") 

print(dbhost)
print(dbuser)
print(dbpass)
print(dbdata)

cursor=db.cursor() 

cursor.execute("select * from score where pid=105")
test=cursor.fetchall()
print(test)