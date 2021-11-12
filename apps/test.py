from mysql import connector
from flask import Flask, redirect, render_template, request
import route
import mysql.connector
import pytest


db=mysql.connector.connect (    host="localhost" ,  
                                user="root", 
                                password="rootroot", 
                                database="tournament_test")

cursor=db.cursor() 

cursor.execute( "create table player_test (pid int, name char(25), surname char(25), email char(50), age int)")
db.commit
cursor.execute( "create table score (pid int, score1 int, score2 int, score3 int, score4 int)")
db.commit

def test_homepage(self):
    self.app.get('/')
    self.assert_template_used('home.html')

def test_newplayer(self):
        response = self.client.post("/submitplayer"),
        data = dict(pid='1', name = "test_name", surname = "test_surname", email = "test@email", age = 21),
        follow_redirects = True
        self.assertIn(b'test_name', response.data)


