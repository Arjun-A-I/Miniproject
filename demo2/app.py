from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from wtforms import SelectField  # Import necessary class


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class PreferenceForm(FlaskForm):
    # Dummy options for the dropdown menus
    choices = [
        ('', 'Select...'),
        ('ny', 'New York'),
        ('sf', 'San Francisco'),
        ('la', 'Los Angeles')
    ]

    starting_point = SelectField(
        'Starting Point', 
        validators=[InputRequired()],
        choices=choices,
        render_kw={"class": "form-control"}
    )

    ending_point = SelectField(
        'Ending Point', 
        validators=[InputRequired()],
        choices=choices,
        render_kw={"class": "form-control"}
    )

    age = StringField(
        'Age', 
        validators=[InputRequired(), Length(min=1, max=2)],
        render_kw={"placeholder": "Age", "class": "form-control"}
    )

    submit = SubmitField('Let\'s Go', render_kw={"class": "btn btn-primary"})

@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('user_preference'))
    return render_template('login.html', form=form)

@app.route('/user_preference', methods=['GET', 'POST'])
def user_preference():
    form = PreferenceForm()
    if form.validate_on_submit():
        print("********dfgdfgdg****************************************************************************")
        start = form.starting_point.data 
        end = form.ending_point.data
        age = form.age.data
        
        # Print details in the server console
        print(f"Starting Point: {start}")
        print(f"Ending Point: {end}")
        print(f"Age: {age}")
        
        # For now, let's redirect to the home page after printing
        # You might want to redirect somewhere relevant or handle data
        return redirect(url_for('dashboard'))
        
    return render_template('preference.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
