from flask import Flask  
from flask import make_response  
from flask import session  
from flask import render_template
from flask import request

app = Flask(__name__)  
app.secret_key = "Naalayathiran"  
 
@app.route('/',methods = ['GET','POST'])  
def home():  
    if request.method == 'GET':
        res = make_response(render_template('Q2.html',cookies = request.cookies, session = session)  )
        return res

    elif request.method == 'POST' and request.form['id'] == '1':
        key,value, exptime = request.form['key'],  request.form['value'], int(request.form['exptime'])
        res = make_response(render_template('Q2.html',cookies = request.cookies |{key: value}, session = session)  )
        res.set_cookie(key,value,exptime)
        return res

    elif request.method == 'POST' and request.form['id'] == '2':
        session[request.form['key']] = request.form['value']
        res = make_response()
        res.data = render_template('Q2.html',cookies = request.cookies, session = session)
        return res
        
 
if __name__ == '__main__':  
    app.run(debug = True)  