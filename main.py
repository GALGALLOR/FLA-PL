
from sys import unraisablehook
from flask import Flask,url_for,redirect,render_template,request,session,get_flashed_messages
from flask_mysqldb import MySQL
import datetime

x=datetime.datetime.now()
year=x.year
month=x.month
day=x.day
date=str(day)+'/'+str(month)+'/'+str(year)

app=Flask(__name__)

mydb=MySQL(app)
app.secret_key='hey'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='GALGALLO10'
app.config['MYSQL_DB']='FLAPL'


@app.route('/')
def base():
    return redirect(url_for('home'))

@app.route('/home')
def home():

    if 'username' in session:
            if 'password' in session:
                username=session['username']

                with app.app_context():
                    cursor=mydb.connection.cursor()
                    cursor.execute('SELECT *, ROW_NUMBER() OVER(ORDER BY DATE) AS ROW_NUM FROM UPDATES ORDER BY ROW_NUM DESC')
                    x=cursor.fetchall()
                    my=[]
                    for xl in x:
                        my.append(xl)
                
                with app.app_context():
                    cursor=mydb.connection.cursor()
                    cursor.execute('SELECT *, ROW_NUMBER() OVER(ORDER BY DATE) AS ROW_NUM FROM FIXTURES ORDER BY ROW_NUM DESC')
                    xli=cursor.fetchall()  
                    xli=xli[0:3]
                return render_template('home.html',username=username,my=my,xli=xli)

    return redirect(url_for('login'))



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        submit=str(request.form['login'])
        print(submit)
        if submit=='login':
            username=str(request.form['username'])
            password=str(request.form['password'])
            try:
                with app.app_context():
                    cursor=mydb.connection.cursor()
                    cursor.execute('SELECT USERNAME FROM USERDATA WHERE USERNAME="'+username+'" AND PASSWORD="'+password+'"')
                    x=cursor.fetchall()
                    sample_name=[]
                    for xy in x:
                        for xl in xy:
                            sample_name.append(xl)
                    
                    if username in sample_name:
                        session['username']=username
                        session['password']=password

                        return redirect(url_for('home'))
                    else:
                        message='The Username or Password does nnot exist'
                        return render_template('login',message=message)
            except:
                message='The Username or Password is incorrect'
                print(message)
                return render_template('login.html',message=message)

        if submit=='signup':
            username=str(request.form['username'])
            password=str(request.form['password'])
            email=str(request.form['email'])
            phone_number=str(request.form['phone'])
            with app.app_context():
                    cursor=mydb.connection.cursor()
                    cursor.execute('SELECT USERNAME FROM USERDATA WHERE USERNAME="'+username+'"')
                    x=cursor.fetchall()
                    sample_name=[]
                    for xy in x:
                        for xl in xy:
                            sample_name.append(xl)
                            
            if username in sample_name:
                print(sample_name)
                message='The username already exists'
                return render_template('login.html',message=message)
            else:
                session['username']=username
                session['password']=password

                cursor=mydb.connection.cursor()
                cursor.execute('INSERT INTO USERDATA(USERNAME,PASSWORD,EMAIL,PHONE_NUMBER)VALUES(%s,%s,%s,%s)',(username,password,email,phone_number))
                mydb.connection.commit()

                return redirect(url_for('home'))


    else:
        try:
            if 'username' in session:
                session.pop('username',None)
                session.pop('password',None)
                message='You Have Been Logged Out'
                return render_template('login.html',message=message)
            else:
                return render_template('login.html')
        except:
            return render_template('login.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST':
        submit=str(request.form['post'])
        if submit=='updates':
            date=str(day)+'/'+str(month)+'/'+str(year)
            url=str(request.form['url'])
            url2=str(request.form['url2'])
            news=str(request.form['news'])

            cursor=mydb.connection.cursor()
            cursor.execute('INSERT INTO UPDATES(URL,URL2,NEWS,DATE)VALUES(%s,%s,%s,%s)',(url,url2,news,date))
            mydb.connection.commit()
        elif submit=='playerdata':
            playername=request.form['name']
            age=request.form['age']
            role=request.form['role']
            team=request.form['team']
            house=request.form['house']
            worth=request.form['worth']
            points=request.form['points']

            cursor=mydb.connection.cursor()
            cursor.execute('INSERT INTO PLAYERDATA(NAME,AGE,ROLE,TEAM,HOUSE,POINTS,WORTH)VALUES(%s,%s,%s,%s,%s,%s,%s)',(playername,age,role,team,house,points,worth))
            mydb.connection.commit()
        else:
            date=str(day)+'/'+str(month)+'/'+str(year)
            team1= str(request.form['team1'])
            score1=str(request.form['score1'])
            team2= str(request.form['team2'])
            score2=str(request.form['score2'])

            cursor=mydb.connection.cursor()
            cursor.execute('INSERT INTO FIXTURES(TEAM1,TEAM2,SCORE1,SCORE2,DATE)VALUES(%s,%s,%s,%s,%s)',(team1,team2,score1,score2,date))
            mydb.connection.commit()

        return render_template('admin.html')
    else:
        if 'gal' in session['username']:
            return render_template('admin.html')
        else:
            return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
