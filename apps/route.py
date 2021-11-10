from flask import Flask, redirect, render_template, request
import mysql.connector

db=mysql.connector.connect (    host="localhost" ,  
                                user="root",
                                password="root",
                                database="tournament")  #exposed SQL details security issue.

app=Flask(__name__, template_folder='../templates')
#get db connection to mysql with SQL alchemy if possible for security.
cursor=db.cursor()

#class forms instead of html!
#class AddEmp(FlaskForm):
    #salary = IntegerField("Salary")
    #marks = IntegerField("Marks")
    #subject = SelectField("Subject", choices=[('python', 'Python'), ('java', 'Java'), ('php', 'PHP'), ('sql', 'SQL')])
    #department = SelectField('Department', choices=[('IT', 'Information technology'), ('HR', 'Human Resources'), ('sales', 'Sales'), ('training', 'Training')])
    #submit = SubmitField('Add Employee')

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
    cursor.execute("select t.pid,u.name, sum(score1+score2+score3+score4) from score t inner join player u on t.pid = u.pid  group by pid order by pid desc")                                                 #get sql quesry to display highest decesding
    data=cursor.fetchall()
    return render_template('highscore.html',records=data)                                         #sending all the sql query results to page

@app.route("/addplayer", methods=['GET', 'POST'])                           #makes a table of all players to add to tournament(score)
def addplayer():
    cursor.execute("select pid,name,surname from player")
    data=cursor.fetchall()
    return render_template('addplayer.html', records=data)


@app.route("/submitaddplayer/<pid>")                                        #function to add a player to the score table with 0 score.
def subaddplayer(pid):
    cursor.execute("insert into score value ({0}, {1}, {2}, {3}, {4})".format(pid, 0,0,0,0))      #may need if/else for double entry
    db.commit()
    return redirect("/addplayer")

@app.route("/newplayerdetails")                                             #functional page that send player details to /submitplayer
def newplayerdetails():
    return render_template('newplayer.html')  

@app.route('/editscoresub/<pid>', methods=["POST", "GET"])
def editscoresub(pid):
    pid=request.form["pid"]
    score1=request.form["score1"]
    score2=request.form["score2"]
    score3=request.form["score3"]
    score4=request.form["score4"]
    sqlquery="update score set score1 = {1}, score2 = {2}, score3 = {3}, score4 = {4} where pid={0}".format(pid, score1, score2, score3, score4)
    cursor.execute(sqlquery)
    db.commit
    return redirect('/highscore')

@app.route('/updatescore/<pid>')
def editscore(pid):
    cursor.execute("select * from score where pid={0}".format(pid))
    data=cursor.fetchall()
    cursor.execute("select name from player where pid={0}".format(pid))
    name=cursor.fetchall()
    return render_template('updatescore.html', record=data, player=name)







app.run(debug=True)