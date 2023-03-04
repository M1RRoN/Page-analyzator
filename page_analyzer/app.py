import os
import psycopg2
from flask import Flask, render_template, flash, redirect, url_for
from .database import Urls

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.get('/urls')
def show_all_urls():
    try:
        with Urls() as db:
            urls_data = db.get_urls_data()

        return render_template(
            'urls.html', urls=urls_data
        )

    except psycopg2.DatabaseError:
        flash('Не удалось подключиться к базе данных', 'alert-warning')
        return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run()
