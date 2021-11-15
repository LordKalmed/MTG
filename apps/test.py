import flask
from mysql import connector
from flask import Flask, redirect, render_template, request
from werkzeug.wrappers.response import Response
import route
import mysql.connector
import pytest
import requests


db=mysql.connector.connect (    host="localhost" ,  
                                user="root", 
                                password="root", 
                                database="tournament_test")

cursor=db.cursor() 

drop1="drop table if exists player"
drop2="drop table if exists score"
cursor.execute(drop1)
cursor.execute(drop2)
db.commit



cursor.execute( "create table player (pid int, name char(25), surname char(25), email char(50), age int)")
db.commit
cursor.execute( "create table score (pid int, score1 int, score2 int, score3 int, score4 int)")
db.commit

def test_homepage():
    assert template_used == "home.html"

def test_newplayer(self):
    response = self.client.post("/submitplayer"),
    data = dict(pid='1', name = "test_name", surname = "test_surname", email = "test@email", age = 21),
    follow_redirects = True
    self.assertIn(b'test_name', response.data)

#def test_highscore():                                       #struggeling with test code. will try again next time.


#def test_addplayer():                          Need to test for return of url + get from database

#def test_subaddplayer():                       test submit detials to SQL

#def test_newplayerdetails():                      Test url for new player details (simple)




    

