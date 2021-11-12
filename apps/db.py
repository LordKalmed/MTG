from os import getenv



dbhost=getenv("sqlhost")
dbuser=getenv("sqluser")
dbpass=getenv("sqlpass1")
dbdata=getenv("sqldata")


dbconn=getenv("sqlconnect")

"select score.pid, player.name, sum(score.score1+score.score2+score.score3+score.score4) from score inner join player score.pid=player.pid group by pid order by pid desc

select score.pid, player.name, sum(score1+ score2+ score3+score4) from score, player inner join player on score.pid = player.pid

select score.pid, player.name , sum(score1+ score2 + score3 + score4) as total from score, player where score.pid = player.pid;

print(dbhost)
print(dbuser)
print(dbpass)
print(dbdata)