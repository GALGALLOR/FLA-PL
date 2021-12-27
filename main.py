
from flask import Flask,url_for,redirect,render_template,request

app=Flask(__name__)
app.secret_key='hey'

app.config

@app.route('/')
def free():
    return url_for('home')

@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
