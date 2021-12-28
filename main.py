
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


@app.route('/team',methods=['GET','POST'])
def team():
    username=session['username']
    goalkeepers=[]
    defenders=[]
    midfielders=[]
    attackers=[]
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username +' WHERE ROLE="GOALKEEPER" AND STATUS="ON"')
        goalkeeper=cursor.fetchall()
        for gk in goalkeeper:
            goalkeepers.append(gk)
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username +' WHERE ROLE="DEFENDER" AND STATUS="ON"')
        defender=cursor.fetchall()
        for cb in defender:
            defenders.append(cb)
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username +' WHERE ROLE="MIDFIELDER" AND STATUS="ON"')
        midfielder=cursor.fetchall()
        for mid in midfielder:
            midfielders.append(mid)
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username +' WHERE ROLE="ATTACKER" AND STATUS="ON"')
        attacker=cursor.fetchall()
        for st in attacker:
            attackers.append(st)
    miraa=goalkeepers,defenders,midfielders,attackers
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username +' WHERE STATUS="SUBSTITUTE"')
        substitute=cursor.fetchall()
        
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM PLAYERDATA')
        players=[]
        player=cursor.fetchall()
        for k in player:
            players.append(k)
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username+' WHERE STATUS="ON"')
        playing=cursor.fetchall()
    
    if request.method=='POST':
        submit=str(request.form['submit'])
        if submit=='substitute':
            subout=str(request.form['on'])
            subin=str(request.form['substitute'])
            cursor=mydb.connection.cursor()
            cursor.execute('UPDATE '+username+' SET STATUS="ON" WHERE NAME="'+subin+'"')
            cursor.execute('UPDATE '+username+' SET STATUS="SUBSTITUTE" WHERE NAME="'+subout+'"')
            mydb.connection.commit()
        else:
            player=str(request.form['sell'])
            cursor=mydb.connection.cursor()
            cursor.execute('DELETE FROM '+username+' WHERE NAME="'+player+'"')
            mydb.connection.commit()

            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT WORTH FROM PLAYERDATA WHERE NAME="'+player+'"')
                worth=cursor.fetchall()
                cash=[]
                for worth in worth:
                    for worth in worth:
                        cash.append(worth)
                print(cash[0])
            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT COINS FROM USERDATA WHERE USERNAME="'+username+'"')
                coin=cursor.fetchall()
                coins=[]
                for coin in coin:
                    for coin in coin:
                        coins.append(coin)

                coins=int(coins[0])+int(cash[0])
                print(coins)
            cursor=mydb.connection.cursor()
            cursor.execute('UPDATE USERDATA SET COINS="'+str(coins)+'" WHERE USERNAME="'+username+'"')
            mydb.connection.commit()


            
    else:
        message='Welcome back'
        print(message)
    return render_template('team.html',playing=playing,substitutes=substitute,username=username,players=players,goalkeepers=goalkeepers,midfielders=midfielders,defenders=defenders,attackers=attackers)

@app.route('/transfers',methods=['POST','GET'])
def transfers():
    username=session['username']
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM PLAYERDATA')
        xlo=cursor.fetchall()

    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username)
        owned=cursor.fetchall()
        names=[]
        for x in owned:
            for x in x:
                names.append(x)

    if request.method=='POST':
        transaction=request.form['transaction']
        player=request.form['player']
        if transaction=='sell':
            cursor=mydb.connection.cursor()
            cursor.execute('DELETE FROM '+username+' WHERE NAME="'+player+'"')
            mydb.connection.commit()

            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT WORTH FROM PLAYERDATA WHERE NAME="'+player+'"')
                worth=cursor.fetchall()
                cash=[]
                for worth in worth:
                    for worth in worth:
                        cash.append(worth)
                print(cash[0])
            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT COINS FROM USERDATA WHERE USERNAME="'+username+'"')
                coin=cursor.fetchall()
                coins=[]
                for coin in coin:
                    for coin in coin:
                        coins.append(coin)

                coins=int(coins[0])+int(cash[0])
                print(coins)
            cursor=mydb.connection.cursor()
            cursor.execute('UPDATE USERDATA SET COINS="'+str(coins)+'" WHERE USERNAME="'+username+'"')
            mydb.connection.commit()
        else:
            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT * FROM PLAYERDATA WHERE NAME="'+player+'"')
                player_data=cursor.fetchall()
                playerdata=[]
                for data in player_data:
                    for data in data:
                        playerdata.append(data)
                print(playerdata)

            cursor=mydb.connection.cursor()
            cursor.execute('INSERT INTO '+username+'(NAME,AGE,ROLE,TEAM,HOUSE,POINTS,WORTH,STATUS)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(playerdata[0],playerdata[1],playerdata[2],playerdata[3],playerdata[4],playerdata[5],playerdata[6],'on'))
            mydb.connection.commit()

            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT WORTH FROM PLAYERDATA WHERE NAME="'+player+'"')
                worth=cursor.fetchall()
                cash=[]
                for worth in worth:
                    for worth in worth:
                        cash.append(worth)
            
            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT COINS FROM USERDATA WHERE USERNAME="'+username+'"')
                coin=cursor.fetchall()
                coins=[]
                for coin in coin:
                    for coin in coin:
                        coins.append(coin)
            
            money=int(coins[0])-int(cash[0])
            print(money)

            cursor=mydb.connection.cursor()
            cursor.execute('UPDATE USERDATA SET COINS="'+str(money)+'" WHERE USERNAME="'+username+'"')
            mydb.connection.commit()

    return render_template('transfers.html',username=username,xlo=xlo,owned=owned,names=names)

@app.route('/league')
def league():
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT *, ROW_NUMBER() OVER(ORDER BY POINTS) AS ROW_NUM FROM LEAGUE ORDER BY ROW_NUM DESC')
        teams=cursor.fetchall()
        print(teams)
    return render_template('league.html',teams=teams)

@app.route('/accounts')
def accounts():
    return render_template('accounts.html')

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
                        with app.app_context():
                            cursor=mydb.connection.cursor()
                            cursor.execute('CREATE TABLE '+username+'(NAME VARCHAR(255),AGE VARCHAR(255),ROLE VARCHAR(255),TEAM VARCHAR(255),HOUSE VARCHAR(255),POINTS VARCHAR(255),WORTH VARCHAR(255))')
                            mydb.connection.commit()
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
