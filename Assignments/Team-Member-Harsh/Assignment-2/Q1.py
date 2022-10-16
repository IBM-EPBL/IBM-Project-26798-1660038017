from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('Q1.html',name = '', email = '', phone = '')
        
    if request.method == 'POST':
        n,e,p = request.form['name'],request.form['email'],request.form['phone']
        return render_template('Q1.html',name = n, email = e, phone = p)

if __name__ == '__main__':
    app.run(debug = True)