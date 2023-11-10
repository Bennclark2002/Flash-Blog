import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

#Function to open a connection to the database.db file

def get_db_connection():
    #Get a database connection
    conn = sqlite3.connect('database.db')
    
    #allows us to have name base access to columns
    #the db connection will return rows we can access like python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

#Function to get a post
def get_post(post_id):
    #get a db connection 
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)

    return post



# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    
    #get a database connection
    conn = get_db_connection()

    #execute a query to get all popst from database
    #use fetchall() to get all of rows from teh query resultlo
    query = 'SELECT * FROM posts'
    posts =  conn.execute(query).fetchall()
    
    #Close the connection
    conn.close()

    return render_template('index.html', posts=posts)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        #get the title and the content that the user submitted
        title = request.form['title']
        content = request.form['content']

        #display error if title or content is not submitted
        #otherwise make a database connection and insert the post
        if not title:
            flash('Title is required!')
        elif not content:
            flash("Content is required!")
        else:   
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title,content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

#route to edit post
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == "POST":
    #get the title and the content that the user submitted
        title = request.form['title']
        content = request.form['content']

        #display error if title or content is not submitted
        #otherwise make a database connection and insert the post
        if not title:
            flash('Title is required!')
        elif not content:
            flash("Content is required!")
        else:   
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id) )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))


    return render_template('edit.html', post=post)

# route to delete a post
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    #get the post 
    post = get_post(id)
    #connect to the database
    conn = get_db_connection()
    #run a delete query 
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    #Commit changes and close connetion to the database
    conn.commit()
    conn.close()
    #Show a success message
    flash('"{}" was successfully deleted!'.format(post['title']))
    #Redirect back to index page
    return redirect(url_for('index'))


app.run(host="0.0.0.0", port=5001)