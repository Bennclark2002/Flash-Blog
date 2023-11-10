import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'




# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    
    
    return "<h1>Index Page<\h1>"

@app.route('/create/', methods=('GET', 'POST'))
def create():
    

    return "<h1>Create a Post Page<\h1>"

#route to edit post
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):


    return "<h1>Edit a Post Page<\h1>"

# route to delete a post
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    
    
    return 


app.run(host="0.0.0.0", port=5001)