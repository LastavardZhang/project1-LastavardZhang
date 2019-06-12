#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-
import pymysql
from flask import Flask
from flask import render_template
from flask import request   
import traceback  
app = Flask(__name__)

@app.route('/')

def login():
    return render_template('login.html')
@app.route('/regist')
def regist():
    return render_template('regist.html')

#设置响应头
def Response_headers(content):    
    resp = Response(content)    
    resp.headers['Access-Control-Allow-Origin'] = '*'    
    return resp 
@app.route('/registuser')
#获取注册请求及处理
def getRigistRequest():
    db = pymysql.connect("localhost","root","root","TESTDB" )
    cursor = db.cursor()
    sql = "INSERT INTO user(user, password) VALUES ("+request.args.get('user')+", "+request.args.get('password')+")"
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return render_template('login.html') 
    except:
        traceback.print_exc()
        db.rollback()
        db.close()
        return '注册失败'
    return "Hello!"

@app.route('/login')
def getLoginRequest():
    db = pymysql.connect("localhost","root","root","TESTDB" )
    cursor = db.cursor()
    sql = "select * from user where user="+request.args.get('user')+" and password="+request.args.get('password')+""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results)==1:
            return render_template('search.html')
        else:
            return '用户名或密码不正确'
        db.commit()
    except:
        traceback.print_exc()
        db.rollback()
    db.close()
    
@app.route('/search')
def searchBook():
    db = pymysql.connect("localhost","root","root","TESTDB" )
    cursor = db.cursor()
    sql = "select * from books where isbn like '%"+request.args.get('bookinfo')+"%'"
    csqs = " "
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        traceback.print_exc()
        db.rollback()
    db.close()

    return render_template('searchres.html',u=results) 

#使用__name__ == '__main__'是 Python 的惯用法，确保直接执行此脚本时才
#启动服务器，若其他程序调用该脚本可能父级程序会启动不同的服务器
if __name__ == '__main__':
   app.run(debug=True)