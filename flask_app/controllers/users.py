import re
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/register' , methods=['POST'])
def register():

    if not User.validate_user(request.form):
        return redirect('/')

    if User.email_exsists(request.form):
        flash("Email is already associated with this account", "Email_exisits")
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['pw'])

    # print(pw_hash)

    data = {
        'fname' : request.form['fname'],
        'lname' : request.form['lname'],
        'email' : request.form['email'],
        'pw' : pw_hash
    }

    
    user_id = User.save(data)
    session['id'] = user_id
    return redirect('/success')

@app.route('/success')
def success():

    if "id" not in session:
        return redirect("/")


    user_id = User.get_by_id(session)
    # print(user_id)

    return render_template("success.html", user_id = user_id)

@app.route('/login' , methods = ['POST'])
def login():

    data = {
        "email" : request.form['email']
    }

    user_in_db = User.get_by_email(data)
    #false
    # print(user_in_db)

    if not user_in_db:
        flash("Invalid Email!", 'email_login_error')
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['pw']):
        flash("Invalid Password!", 'password_login_error')
        return redirect('/')

    session['id'] = user_in_db.id
    print(session["id"])

    return redirect('/success')


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")
