from os import getenv



dbhost=getenv("sqlhost")
dbuser=getenv("sqluser")
dbpass=getenv("sqlpass1")
dbdata=getenv("sqldata")


dbconn=getenv("sqlconnect")

print(dbconn)
print(dbhost)
print(dbuser)
print(dbpass)
print(dbdata)