from flask import Blueprint , render_template , request , flash , redirect , url_for
from .models import User
from . import db
#from werkzeug.security import generated_password_hash , check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods = ['Get', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:   
                flash("loggend in successfully!", category= 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.user'))
            else:
                flash("incorrect password try again!", category= 'error')
        else:
            flash("user doesn't exist signup first!", category='error')
    return render_template("login.html", user = current_user)####

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/join", methods = ['Get', 'POST'])
def join():
    if request.method == 'POST':
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        account_toggle = request.form.get('accountToggle')

        # Check if the accountToggle is 'on' (toggled) or not
        account_state = False
        if account_toggle == 'on':
            account_state = True
        else:
            account_state = False
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists! login please.", category='error')
        else:
            new_user = User(email=email, name=name, password= password, state= account_state)#generated_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("successfully joined!", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.user'))
    return render_template("join.html", user = current_user)


