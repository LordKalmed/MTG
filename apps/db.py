from os import getenv



dbhost=getenv("sqlhost")
dbuser=getenv("sqluser")
dbpass=getenv("sqlpass")
dbdata=getenv("sqldata")

print(dbhost)
print(dbuser)
print(dbpass)
print(dbdata)