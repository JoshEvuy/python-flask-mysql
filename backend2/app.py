from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, DateField, DateTimeField
from passlib.hash import sha256_crypt
from data import Articles
from datetime import datetime

# App Config
app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ewaveadmin'
app.config['MYSQL_PASSWORD'] = 'ewaveadmin'
app.config['MYSQL_DB'] = 'fctewave'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# MySQL Init
mysql = MySQL(app)

# Call the articles
Articles = Articles()

# Index Route
@app.route('/')
def viewIndex():
    return render_template('home.html')

# About Route
@app.route('/about')
def viewAbout():
    return render_template('about.html')

# Articles Route
@app.route('/articles')
def viewArticles():
    return render_template('articles.html', articles = Articles)

# Single Article Route
@app.route('/article/<string:id>')
def viewArticle(id):
    return render_template('article.html', id=id)

# User Register Form
class UserRegisterForm(Form):
    uname = StringField('Name', [validators.Length(min=3, max=50), validators.DataRequired])
    unick = StringField('Nick', [validators.Length(min=3, max=50)])
    utype = SelectField('Type', choices=[('Estudiante','Estudiante'),('Tutor','Tutor'),('Centro Docente','Centro Docente'),('Empresa','Empresa'), validators.DataRequired])
    uemail = StringField('Email', [validators.Length(min=7, max=50), validators.DataRequired])
    upassword = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('uconfirmpassword', message='Passwords do not match')
    ])
    uconfirmpassword = PasswordField('Confirm Password')
    # ucreationdate = DateTimeField('Account Creation Date', default=datetime.now(), format='%Y-%m-%d %H:%i:%S', [validators.DataRequired])
    #ucreationdate = DateTimeField('Account Creation Date', default=datetime.now(), format='%Y-%m-%d %H:%M:%S')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def viewRegister():
    form = UserRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        uname = form.uname.data        
        unick = form.unick.data
        utype = form.utype.data
        uemail = form.uemail.data
        upassword = sha256_crypt.encrypt(str(form.upassword.data))
        #ucreationdate = form.ucreationdate.data
        
        # Create Cursor
        cur = mysql.connection.cursor()
        
        # Check email
        # cur.execute("SELECT useremail FROM fctewave.users WHERE useremail = '%s'", (uemail))

        # Execute query
        cur.execute("INSERT INTO users(username, usernick, usertype, useremail, userpwd) VALUES(%s, %s, %s, %s, %s)", (uname, unick, utype, uemail, upassword))
        
        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('viewIndex'))       
    return render_template('register.html', form=form)
"""
# User Login
@app.route('/login', methods=['GET', 'POST'])
def viewLogin():
    if request.method == 'POST':
        # Get form fields    
    return render_template('login.html')
"""

# Start app
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)