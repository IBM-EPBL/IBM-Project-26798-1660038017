from flask import Flask, render_template
import datetime


app = Flask(__name__)

@app.route('/')
def index():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return render_template('index.html',text = current_time)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)