from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('secretkey')

db = SQLAlchemy(app)

class players(db.Model):
    pid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))

class score(db.Model):
    pid = db.Column(db.Integer, primary_key = True)
    score1 = db.Column(db.String(50))
    score2 = db.Column(db.Integer)
    score3 = db.Column(db.Integer)
    score4 = db.Column(db.String(50))

db.drop_all()
db.create_all()
                                                                                     #get db connection to mysql with SQL alchemy
cursor=db.cursor()

#class forms instead of html!
class AddEmp(FlaskForm):
    emp_name = StringField("Name")
    salary = IntegerField("Salary")
    marks = IntegerField("Marks")
    subject = SelectField("Subject", choices=[('python', 'Python'), ('java', 'Java'), ('php', 'PHP'), ('sql', 'SQL')])
    department = SelectField('Department', choices=[('IT', 'Information technology'), ('HR', 'Human Resources'), ('sales', 'Sales'), ('training', 'Training')])
    submit = SubmitField('Add Employee')

@app.route("/")                                                                             #get high score data for leader board
def homepage():
    return render_template("/home.html")

@app.rout("/submitplayer", methods=["POST"])                                                #should now recieve post with all players details
def newplayer():
    cursor.execute("select ifnull(max(pid),100)+1 from player")
    newstudentid=cursor.fetchone()
    name=request.form["name"]
    surname=request.form["surname"]
    age=request.form["age"]
    email=request.form["email"]
    sqlquery="insert into players value({0},'{1}','{2}',{3}, '{4}')".format(newstudentid[0],name,surname,age, email)
    cursor.execute(sqlquery)
    db.commit()
    return redirect("/")

@app.route("/highscore")                                                                    #got the correct sql query for score calc.
def highscore():
    cursor.execute("select pid, sum(score1+score2+score3+score4) from  score group by pid order by pid desc")                                                 #get sql quesry to display highest decesding
    #####(select t.pid,u.name, sum(score1+score2+score3+score4) from score t inner join player u on t.pid = u.pid  group by pid order by pid desc)                                                                                   #need to figure out how to swap player_id for name here
    data=cursor.fetchall()
    render_template("highscore.html", records=data)                                         #sending all the sql query results to page

@app.route("/addplayer", methods=["POST"])                                                  #function is sent a player id to add to the score table.
def addplayer():
    cursor.execute("select pid,name,surname from player")
    data=cursor.fetchall()
    render_template("addplayer.html", records=data)


@app.route("/submitaddplayer/<pid>")
def subaddplayer(pid):
    cursor.execute("insert into scores value ('{0}', {1}, {2}, {3})".format(pid, 0,0,0))      #may need if/else for double entry
    db.commit()
    return redirect("addplayer.html")








app.run(debug=True)