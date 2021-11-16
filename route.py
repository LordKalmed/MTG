from flask import Flask, redirect, render_template, request
import mysql.connector
from werkzeug.datastructures import CombinedMultiDict
from os import getenv, environ


dbhost=getenv("sqlhost")
dbuser=getenv("sqluser")
dbpass=getenv("sqlpass")
dbdata=getenv("sqldata")
#db=mysql.connector.connect (db_connect)

db=mysql.connector.connect (    host="localhost" ,  
                                user="root", 
                                password="root", 
                                database="tournament") 


app=Flask(__name__,)                    #get db connection to mysql with SQL alchemy if possible for security.
cursor=db.cursor()


@app.route("/")                                                             #Mostly just hyper links and info
def homepage():
    return render_template('home.html')

@app.route("/submitplayer", methods=['GET', 'POST'])                        #functional code that inserts the user values as a new player
def newplayer():
    cursor.execute("select ifnull(max(pid),100)+1 from player")
    newpid=cursor.fetchone()
    name=request.form["name"]
    surname=request.form["surname"]
    age=request.form["age"]
    email=request.form["email"]
    sqlquery="insert into player value({0},'{1}','{2}','{3}', {4})".format(newpid[0],name,surname,email, age)
    cursor.execute(sqlquery)
    db.commit()
    return redirect("/")

@app.route("/highscore", methods=['GET', 'POST'])                           #got the correct sql query for score calc. Desc order for easy winner
def highscore():
    cursor.execute("SET SESSION sql_mode=''")
    cursor.execute("select t.pid, u.name, sum(score1+score2+score3+score4) as Total from score t inner join player u on t.pid = u.pid group by pid order by Total desc")                                                 #get sql quesry to display highest decesding
    data=cursor.fetchall()
    return render_template('highscore.html',records=data)                                         #sending all the sql query results to page

@app.route("/addplayer", methods=['GET', 'POST'])                           #makes a table of all players to add to tournament(score)
def addplayer():
    cursor.execute("select pid,name,surname from player")
    data=cursor.fetchall()
    return render_template('addplayer.html', records=data)

@app.route("/submitaddplayer/<pid>")                                        #function to add a player to the score table with 0 score.
def subaddplayer(pid):
    cursor.execute("select * from score where pid={0}".format(pid))
    ontable=cursor.fetchall()
    if ontable=="[]":
        cursor.execute("insert into score value ({0}, {1}, {2}, {3}, {4})".format(pid, 0,0,0,0))      #may need if/else for double entry
        db.commit()
        return redirect("/addplayer")
    else:
        return redirect("/addplayer")

@app.route("/newplayerdetails")                                             #functional page that send player details to /submitplayer
def newplayerdetails():
    return render_template('newplayer.html')  

@app.route('/editscoresub', methods=["POST", "GET"])                        #fuction to update scores for specific players.
def editscoresub():
    pid=request.form["pid"]
    score1=request.form["score1"]
    score2=request.form["score2"]
    score3=request.form["score3"]
    score4=request.form["score4"]
    sqlquery="update score set score1 = {1}, score2 = {2}, score3 = {3}, score4 = {4} where pid = {0}".format(pid, score1, score2, score3, score4)
    cursor.execute(sqlquery)
    db.commit
    return redirect('/highscore')

@app.route('/updatescore/<pid>')                                            #function gets the name of the player and scores from both tables, then allows us to update the scores
def editscore(pid):
    cursor.execute("select * from score where pid={0}".format(pid))
    data=cursor.fetchall()
    cursor.execute("select name from player where pid={0}".format(pid))
    name=cursor.fetchall()
    return render_template('updatescore.html', records=data, player=name)

@app.route('/editplayer')                                                   #functions fine to pull all data and render edit player.
def editplayer():
    cursor.execute("select * from player")
    data=cursor.fetchall()
    return render_template('editplayer.html', records=data)

@app.route('/editplayerdetails/<pid>')                                      #correctly displays current data for player.
def editplayerdetails(pid):
    cursor.execute("select * from player where pid={0}".format(pid))
    data=cursor.fetchall()
    return render_template("editplayerdetails.html", records=data)

@app.route('/submiteditplayer', methods=["POST"])                           #function to submit new details to player table
def submiteditplayer():
    pid=request.form["pid"]
    name=request.form["name"]
    surname=request.form["surname"]
    email=request.form["email"]
    age=request.form["age"]
    cursor.execute("update player set name = '{1}', surname = '{2}', email = '{3}', age={4} where pid={0}".format(pid,name,surname,email,age))
    db.commit
    return redirect("/")

@app.route('/deleteplayer/<pid>')                                           #function to delet player inside the edit form
def deleteplayer(pid):
    cursor.execute("delete from player where pid={0}".format(pid))
    db.commit
    return redirect("/")

@app.route('/resettournament')                                              #function to drop all scoires from score, reset the tournament
def reset():
    cursor.execute("delete from score")
    db.commit
    return redirect("/")

app.run(debug=True)
