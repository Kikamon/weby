import sqlite3
import os
from wtforms import RadioField
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, length
from wtforms import TextAreaField

app = Flask(__name__)
app.debug = True
app.secret_key = 'svsdfvsdsfgsgsrg'

aktualni_adresar = os.path.abspath(os.path.dirname(__file__))
databaze = (os.path.join(aktualni_adresar, 'poznamky.db'))


class PoznamkaForm(FlaskForm):
    poznamka = TextAreaField('Poznámka', validators=[DataRequired(), length(max=250)])
    dulezitost = RadioField("Dulezitost", choices=[("1", 'Běžná poznámka'), ("2", 'Hromadná poznámka'), ("3", 'Důležitá poznámka')])

@app.route('/', methods=['GET', 'POST'])
def hlasuj():
    """Zobrazí hlasovací formulář."""
    form = PoznamkaForm()
    poznamka_text = form.poznamka.data
    dulezitost = form.dulezitost.data
    if form.validate_on_submit():
        conn = sqlite3.connect(databaze)
        c = conn.cursor()
        c.execute("INSERT INTO poznamka(telo, dulezitost) VALUES (?, ?)", (poznamka_text, dulezitost,))
        conn.commit()
        conn.close()
        return redirect('/vysledky')
    return render_template('hlasuj.html', form=form)


@app.route('/vysledky')
def zobraz_vysledky():
    """Zobrazí výsledky hlasování."""
    conn = sqlite3.connect(databaze)
    c = conn.cursor()
    c.execute(
        "SELECT rowid, telo, kdy, dulezitost FROM poznamka ORDER BY datetime(kdy) DESC ")
    poznamky = c.fetchall()
    conn.close()
    return render_template('vysledky.html', poznamky=poznamky)


@app.route('/smaz/<int:poznamka_id>')
def smaz_poznamku(poznamka_id):
    """Smaže vybranou poznámku"""
    conn = sqlite3.connect(databaze)
    c = conn.cursor()
    c.execute("DELETE FROM poznamka WHERE rowid=?", (poznamka_id,))
    conn.commit()
    conn.close()
    return redirect('/vysledky')

@app.route('/uprav/<int:poznamka_id>', methods=['GET', 'POST'])
def uprav_poznamku(poznamka_id):
    """Upraví poznámku."""
    conn = sqlite3.connect(databaze)
    c = conn.cursor()
    c.execute("SELECT telo, kdy, dulezitost FROM poznamka WHERE rowid=?", (poznamka_id,))
    poznamka_tuple = c.fetchone()
    conn.close()
    form = PoznamkaForm(poznamka=poznamka_tuple[0])
    poznamka_text = form.poznamka.data
    dulezitost = form.dulezitost.data
    if form.validate_on_submit():
        conn = sqlite3.connect(databaze)
        c = conn.cursor()
        c.execute("UPDATE poznamka SET telo=?, dulezitost=? WHERE rowid=?", (poznamka_text, dulezitost, poznamka_id))
        conn.commit()
        conn.close()
        return redirect('/vysledky')
    return render_template('hlasuj.html', form=form)



if __name__ == '__main__':
    app.run()
