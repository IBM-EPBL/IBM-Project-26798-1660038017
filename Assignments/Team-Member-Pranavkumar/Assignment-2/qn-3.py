from urllib import request
from flask import Flask
from flask import request
from flask import render_template
from flask import send_file

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('qn-3.html')
    else:
        f = request.files['file']  
        f.save('Assignment-2/resume')  
        return send_file('resume', mimetype='application/pdf')

if __name__ == '__main__':  
    app.run(debug = True)  