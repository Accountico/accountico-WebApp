#Aqui vão as rotas e seus renders

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')
    