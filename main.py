
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
app.config['MYSQL_USER']=''
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']=''


@app.route('/')



@app.route('/create-teamname',methods=['GET','POST'])
def create_teamname():
    if 'username' in session:
        if str(session['teamname'])!='None':
            print('you are not welcome here')
    else:
        print('go login bro')
        return redirect(url_for('login'))

    if 'teamname' in session:
        if str(session['teamname'])=='None':
            pass
        else:
            print('go h')
            return redirect(url_for('home'))
    else:
        print('welcome')
    print('go')
    if request.method=='POST':
        username=session['username']
        teamname=request.form['teamname']
        cursor=mydb.connection.cursor()
        cursor.execute('UPDATE USERDATA SET TEAMNAME="'+teamname+'" WHERE USERNAME="'+username+'"')
        cursor.execute('INSERT INTO LEAGUE(TEAMNAME,POINTS)VALUES(%s,%s)',(teamname,"0"))
        mydb.connection.commit()
        session['teamname']=teamname
        return redirect(url_for('transfers'))
    else:
        username=session['username']
        with app.app_context():
            cursor=mydb.connection.cursor()
            cursor.execute('SELECT COINS,POINTS FROM USERDATA WHERE USERNAME="'+username+'"')
            x=cursor.fetchall()
            ml=[]
            for items in x:
                for item in items:
                    ml.append(item)
        return render_template('create_team.html',username=username,points=ml[1],coins=ml[0])

@app.route('/team',methods=['GET','POST'])
def team():
    if 'teamname' in session:
        pass
    else:
        return redirect(url_for('create_teamname'))
    username=session['username']

    
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
            return redirect(url_for('transfers'))

    else:
        message='Welcome back'
        print(message)
    
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username +' WHERE STATUS="SUBSTITUTE"')
        substitute=cursor.fetchall()
        goalkeepers=[]
    defenders=[]
    midfielders=[]
    attackers=[]
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT COINS,POINTS FROM USERDATA WHERE USERNAME="'+username+'"')
        x=cursor.fetchall()
        ml=[]
        for items in x:
            for item in items:
                ml.append(item)

    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username +' WHERE ROLE="GOAL KEEPER" AND STATUS="ON"')
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
        cursor.execute('SELECT * FROM '+username +' WHERE ROLE="ATTACK" AND STATUS="ON"')
        attacker=cursor.fetchall()
        for st in attacker:
            attackers.append(st)
    miraa=goalkeepers,defenders,midfielders,attackers
    
        
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM PLAYERDATA')
        players=[]
        player=cursor.fetchall()
        for k in player:
            players.append(k)
        print(players)
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username+' WHERE STATUS="ON"')
        playing=cursor.fetchall()
    return render_template('team.html',coins=ml[0],points=ml[1],playing=playing,substitutes=substitute,username=username,players=players,goalkeepers=goalkeepers,midfielders=midfielders,defenders=defenders,attackers=attackers)

@app.route('/transfers',methods=['POST','GET'])
def transfers():
    if 'teamname' in session:
        pass
    else:
        return redirect(url_for('create_teamname'))
    username=session['username']
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT *, ROW_NUMBER() OVER(ORDER BY POINTS) AS ROW_NUM FROM PLAYERDATA ORDER BY POINTS DESC')
        xlo=cursor.fetchall()

    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username)
        owned=cursor.fetchall()
        names=[]
        for x in owned:
            for x in x:
                names.append(x)
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT COINS,POINTS FROM USERDATA WHERE USERNAME="'+username+'"')
        x=cursor.fetchall()
        ml=[]
        for items in x:
            for item in items:
                ml.append(item)
    xu=''
    if request.method=='POST':
        transaction=request.form['transaction']
        player=str(request.form['player'])
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
                cursor.execute('SELECT COUNT(NAME) FROM '+username)
                lolo=cursor.fetchall()
            ks=[]
            for lololo in lolo:
                for lololo in lololo:
                    ks.append(lololo)
            if ks[0]>12:
                xu='!!Maximum Players Bought Reached!!'
            else:
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
                    money=[]
                    for coin in coin:
                        for coin in coin:
                            money.append(coin)

                coins=int(money[0])-int(cash[0])
                if coins>1:
                
                    print(coins)

                    cursor=mydb.connection.cursor()
                    cursor.execute('UPDATE USERDATA SET COINS="'+str(coins)+'" WHERE USERNAME="'+username+'"')
                    mydb.connection.commit()
                    xu=''

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
                    cursor.execute('SELECT COUNT(NAME) FROM '+username+' WHERE STATUS="ON"')
                    lolo=cursor.fetchall()
                    ree=[]
                    for lolo in lolo:
                        for lolo in lolo:
                            ree.append(lolo)

                    if ree[0]>9:
                        cursor.execute('INSERT INTO '+username+'(NAME,AGE,ROLE,TEAM,HOUSE,POINTS,WORTH,STATUS)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(playerdata[0],playerdata[1],playerdata[2],playerdata[3],playerdata[4],'0',playerdata[6],'substitute'))
                    else:
                        cursor.execute('INSERT INTO '+username+'(NAME,AGE,ROLE,TEAM,HOUSE,POINTS,WORTH,STATUS)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(playerdata[0],playerdata[1],playerdata[2],playerdata[3],playerdata[4],'0',playerdata[6],'on'))
                    mydb.connection.commit()
                else:
                    xu=xu+' The Coins are not enough'


                
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT *, ROW_NUMBER() OVER(ORDER BY POINTS) AS ROW_NUM FROM PLAYERDATA ORDER BY POINTS DESC')
        xlo=cursor.fetchall()

    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT * FROM '+username)
        owned=cursor.fetchall()
        names=[]
        for x in owned:
            for x in x:
                names.append(x)
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT COINS,POINTS FROM USERDATA WHERE USERNAME="'+username+'"')
        x=cursor.fetchall()
        ml=[]
        for items in x:
            for item in items:
                ml.append(item)
        try:
            cursor=mydb.connection.cursor()
            cursor.execute('SELECT COUNT(NAME) FROM '+username)
            y=cursor.fetchall()
            yi=0
            for y in y:
                for y in y:
                    yi=yi+y
            numplayers=str(yi)
        except:
            numplayers='0'

    return render_template('transfers.html',numplayers=numplayers,message=xu,coins=ml[0],points=ml[1],username=username,xlo=xlo,owned=owned,names=names)

@app.route('/league')
def league():
    if 'teamname' in session:
        pass
    else:
        return redirect(url_for('create_teamname'))
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT *, ROW_NUMBER() OVER(ORDER BY POINTS) AS ROW_NUM FROM LEAGUE ORDER BY ROW_NUM DESC')
        teams=cursor.fetchall()
        print(teams)
    username=session['username']

    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT COINS,POINTS FROM USERDATA WHERE USERNAME="'+username+'"')
        x=cursor.fetchall()
        ml=[]
        for items in x:
            for item in items:
                ml.append(item)

    return render_template('league.html',coins=ml[0],points=ml[1],username=username,teams=teams)

@app.route('/accounts')
def accounts():
    if 'teamname' in session:
        pass
    else:
        return redirect(url_for('create_teamname'))
    username=session['username']
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT COINS,POINTS FROM USERDATA WHERE USERNAME="'+username+'"')
        x=cursor.fetchall()
        ml=[]
        for items in x:
            for item in items:
                ml.append(item)
    teamname=session['teamname']
    with app.app_context():
        cursor=mydb.connection.cursor()
        cursor.execute('SELECT POINTS FROM USERDATA WHERE USERNAME="'+username+'"')
        x=cursor.fetchall()
    sli=[]
    for slk in x:
        for slk in slk:
            sli.append(slk)
    position=sli[0]
    print(position)

    return render_template('accounts.html',position=position,teamname=teamname,username=username,coins=ml[0],points=ml[1])

@app.route('/')
def base():
    return redirect(url_for('home'))

@app.route('/home')
def home():

    if 'username' in session:
        if 'password' in session:
            if str(session['teamname'])!='None':
                print(session['teamname'])
            elif str(session['teamname'])=='None':
                try:
                    username=session['username']
                    with app.app_context():
                        cursor=mydb.connection.cursor()
                        cursor.execute('SELECT TEAMNAME FROM USERDATA WHERE USERNAME="'+username+'"')
                        x=cursor.fetchall()
                        li=[]
                        for x in x:
                            for x in x:
                                li.append(x)
                        teamname=li[0]
                        session['teamname']=teamname
                except:
                    return redirect(url_for('create_teamname'))
            else:
                return redirect(url_for('create_teamname'))
            username=session['username']
            
            



            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT COINS,POINTS FROM USERDATA WHERE USERNAME="'+username+'"')
                x=cursor.fetchall()
                ml=[]
                for items in x:
                    for item in items:
                        ml.append(item)
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
            print(session)
            return render_template('home.html',coins=ml[0],points=ml[1],username=username,my=my,xli=xli)

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
                with app.app_context():
                    cursor=mydb.connection.cursor()
                    cursor.execute('CREATE TABLE '+username+'(NAME VARCHAR(255),AGE VARCHAR(255),ROLE VARCHAR(255),TEAM VARCHAR(255),HOUSE VARCHAR(255),POINTS VARCHAR(255),WORTH VARCHAR(255),STATUS VARCHAR(255))')
                    mydb.connection.commit()
                cursor=mydb.connection.cursor()
                cursor.execute('INSERT INTO USERDATA(USERNAME,PASSWORD,EMAIL,PHONE_NUMBER,POINTS,COINS)VALUES(%s,%s,%s,%s,%s,%s)',(username,password,email,phone_number,'0','120'))
                mydb.connection.commit()

                return redirect(url_for('home'))


    else:
        try:
            if 'username' in session:
                session.pop('username',None)
                session.pop('password',None)
                session.pop('teamname',None)
                message='You Have Been Logged Out'
                return render_template('login.html',message=message)
            else:
                return render_template('login.html')
        except:
            return render_template('login.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    if 'username' in session:
        username=session['username']
        if 'gal' in username:
            pass
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
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
        elif submit=='results':
            date=str(day)+'/'+str(month)+'/'+str(year)
            team1= str(request.form['team1'])
            score1=str(request.form['score1'])
            team2= str(request.form['team2'])
            score2=str(request.form['score2'])

            cursor=mydb.connection.cursor()
            cursor.execute('INSERT INTO FIXTURES(TEAM1,TEAM2,SCORE1,SCORE2,DATE)VALUES(%s,%s,%s,%s,%s)',(team1,team2,score1,score2,date))
            mydb.connection.commit()
        elif submit=='submit':
            points=int(request.form['points'])
            player=str(request.form['player'])
        
            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT POINTS FROM PLAYERDATA WHERE NAME="'+player+'"')
                x=cursor.fetchall()
            po=[]
            for x in x:
                for x in x:
                    po.append(x)
            old_points=int(po[0])
            new_points=old_points+points

            cursor=mydb.connection.cursor()
            cursor.execute('UPDATE PLAYERDATA SET POINTS="'+str(new_points)+'" WHERE NAME="'+player+'"')
            mydb.connection.commit()

            pill=[]
            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT USERNAME FROM USERDATA')
                kl=cursor.fetchall() 
            for kl in kl:
                for kl in kl:
                    pill.append(kl)
            for user in pill:
                with app.app_context():
                    #updating individual player points in every Table for users
                    cursor=mydb.connection.cursor()
                    cursor.execute('SELECT POINTS FROM '+user+' WHERE NAME="'+player+'"')
                    tk=[]
                    fkk=cursor.fetchall()
                    for fkk in fkk:
                        for fkk in fkk:
                            tk.append(fkk)
                    try:
                        new_points=int(tk[0])+points
                    except:
                        new_points=0

                    cursor=mydb.connection.cursor()
                    cursor.execute('UPDATE '+user+' SET POINTS="'+str(new_points)+'" WHERE NAME="'+player+'"')  
                    mydb.connection.commit()

                    cursor=mydb.connection.cursor()
                    cursor.execute('SELECT POINTS FROM '+user)
                    popo=cursor.fetchall()
                    fkl=0
                    for popo in popo:
                        for popo in popo:
                            fkl=fkl+int(popo)
                    
                    cursor=mydb.connection.cursor()
                    cursor.execute('SELECT TEAMNAME FROM USERDATA WHERE USERNAME="'+user+'"')
                    crocs=cursor.fetchall()
                    snake=[]
                    for crocs in crocs:
                        for crocs in crocs:
                            snake.append(crocs)
                    teamname=snake[0]


                    print(fkl)
                    cursor=mydb.connection.cursor()
                    cursor.execute('UPDATE LEAGUE SET POINTS="'+str(fkl)+'" WHERE TEAMNAME="'+teamname+'"')  
                    mydb.connection.commit()

                    cursor=mydb.connection.cursor()                                      
                    cursor.execute('UPDATE USERDATA SET POINTS="'+str(fkl)+'" WHERE USERNAME="'+user+'"')
                    mydb.connection.commit()


        with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT NAME FROM PLAYERDATA')
                kl=cursor.fetchall() 
                players=[]
                for kl in kl:
                    for kl in kl:
                        players.append(kl)
        
    else:
        if 'gal' in session['username']:
            with app.app_context():
                cursor=mydb.connection.cursor()
                cursor.execute('SELECT NAME FROM PLAYERDATA')
                kl=cursor.fetchall() 
                players=[]
                for kl in kl:
                    for kl in kl:
                        players.append(kl)
        else:
            return redirect(url_for('home'))
    return render_template('admin.html',players=players)



if __name__ == '__main__':
    app.run(debug=True)
