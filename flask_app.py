import random
from flask import Flask, render_template, session
from flask_session import Session

app = Flask(__name__)
app.debug = True
app.secret_key ='sdfasfc25yxvy'
SESSION_TYPE ='filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/')

def hod_kostkou():
    hod = random.randint(1,6)
    hod2 = random.randint(1,6)

    if not 'score_a' in session:
        session['score_a'] = 0
    if not 'score_b' in session:
        session['score_b'] = 0
    if hod > hod2:
        session['score_a'] = session['score_a'] + 1


    elif hod < hod2:
        session['score_b'] = session['score_b'] + 1



    return render_template('index.html', hod=hod, hod2=hod2, score_a=session['score_a'], score_b=session['score_b'] )






if __name__ == '__main__':
    app.run()
