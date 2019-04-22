import os

from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import *
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user, logout_user

app = Flask(__name__)
app.config["SECRET_KEY"] = '\x1a\x1f\xc5Z\x15>\x81\x8fQ\xac\xea\xeb\xdb\x19\x8b`\xc3\x88\x92\xed\xc1s\x93\xeb'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:vench@localhost:5432/reminder"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# login manager set-up
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()

            if user is not None:
                if password == user.password:
                    login_user(user)
                    return redirect(url_for('dashboard'))
                else:
                    return render_template("index.html", message="Incorrect Password or Email")
            else:
                return render_template("index.html", message="Incorrect Password or Email")
        else:
            return render_template("index.html")


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        if request.form.get('password') == request.form.get('cpassword'):
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            password = request.form.get('password')
            email = request.form.get('email')
            gender = request.form.get('gender')
            age = request.form.get('age')
            try:
                user = User(fname=fname, lname=lname, password=password,
                            email=email, gender=gender, age=age)
                db.session.add(user)
                db.session.commit()
                return render_template("index.html", good_message="Registration Complete")
            except:
                return render_template("registration.html", message="Email Alredy Registered")
        else:
            return render_template("registration.html", message="Password Not Match")
    else:
        return render_template("registration.html")


@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    user = current_user
    titles = user.title
    if request.method == "POST":
        if 'add' in request.form:
            title = request.form.get('title')
            user.add_title(title)
        elif 'delete' in request.form:
            title_id = request.form.get('title_id')
            Task.query.filter_by(title_id = title_id).delete()
            Title.query.filter_by(id=title_id).delete()
            db.session.commit()
        return redirect(url_for('dashboard', titles=titles))
    return render_template('dashboard.html', titles=titles)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/task/<int:title_id>", methods=['POST', 'GET'])
@login_required
def task(title_id):
    title = Title.query.filter_by(id=title_id).first()
    tasks = Task.query.filter_by(title_id = title_id).order_by(Task.id).all()

    if 'addTask' in request.form:
        task = request.form.get('task')
        title.add_task(task)
        return redirect(url_for('task', title_id = title_id))
    elif 'delete' in request.form:
        task_id = request.form.get('task_id')
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('task', title_id = title_id))
    elif 'update' in request.form:
        task_id = request.form.get('task_id')
        task = request.form.get('task')
        task_update = Task.query.get(task_id)
        task_update.task = task
        db.session.commit()
        return redirect(url_for('task', title_id = title_id))
    elif 'done' in request.form:
        task_id = request.form.get('task_id')
        done = request.form.get('done')
        task_done = Task.query.get(task_id)
        task_done.done = done
        db.session.commit()
        return redirect(url_for('task', title_id = title_id))
    elif 'undone' in request.form:
        task_id = request.form.get('task_id')
        undone = request.form.get('undone')
        task_undone = Task.query.get(task_id)
        task_undone.done = undone
        db.session.commit()
        return redirect(url_for('task', title_id = title_id))
    return render_template("task.html", title=title, tasks=tasks)

@app.route("/setting", methods=['POST', 'GET'])
@login_required
def setting():
    user = current_user
    if request.method == "POST":
        if request.form.get('password') == request.form.get('cpassword'):
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            password = request.form.get('password')
            gender = request.form.get('gender')
            age = request.form.get('age')
            try:
                user.fname = fname
                user.lname = lname
                user.password = password
                user.gender = gender
                user.age = age
                db.session.commit()
                flash('Update Successfully', '-success')
                return redirect(url_for('setting'))
            except:
                flash('Update Unsuccessfully', '-danger')
                return redirect(url_for('setting'))
        else:
            flash('Password Not Match', '-danger')
            return redirect(url_for('setting', user=user))
    else:       
        return render_template('setting.html', user=user)
