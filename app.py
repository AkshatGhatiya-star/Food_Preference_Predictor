import os
import pickle
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.ensemble import RandomForestClassifier

# --- App Initialization ---
app = Flask(__name__)
# A real secret key is important for security
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_truly_secret_key_for_dev')
# Set the database file path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Extensions Initialization ---
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to login page if user is not authenticated

# --- Load the AI Model and Columns ---
# This function will load the model, handling potential errors gracefully.
def load_model():
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('model_columns.pkl', 'rb') as f:
            model_columns = pickle.load(f)
        return model, model_columns
    except FileNotFoundError:
        print("CRITICAL: model.pkl or model_columns.pkl not found. Please train the model first.")
        return None, None

model, model_columns = load_model()

# --- Database Model ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'warning')
            return redirect(url_for('signup'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/recommend', methods=['POST'])
@login_required
def recommend():
    if model is None:
        flash("Model not loaded. Please ensure 'model.pkl' and 'model_columns.pkl' exist.", 'danger')
        return redirect(url_for('dashboard'))

    try:
        user_input = {
            'Weight': float(request.form['weight']),
            'City': request.form['city'],
            'State': request.form['state'],
            'Temperature': float(request.form['temperature']),
            'Season': request.form['season'],
            'Income_Level': request.form['income_level'],
            'Stress_Level': request.form['stress_level'],
            'Sleep_Hours': float(request.form['sleep_hours']),
            'Work_Life_Balance': request.form['work_life_balance'],
            'Context': request.form['context']
        }
    except ValueError:
        # Handle cases where user enters non-numeric data
        flash('Please enter valid numbers for Weight, Temperature, and Sleep Hours.', 'danger')
        return render_template('dashboard.html', recommendation=None)

    # Convert user input into a DataFrame
    input_df = pd.DataFrame([user_input])

    # One-hot encode the input DataFrame
    input_encoded = pd.get_dummies(input_df)

    # Align columns with the model's training columns
    # This adds missing columns with a value of 0 and removes extra columns.
    final_input = input_encoded.reindex(columns=model_columns, fill_value=0)

    # Make a prediction
    prediction = model.predict(final_input)
    recommendation = prediction[0]

    # Render the dashboard with the result
    flash(f'Based on your input, we recommend: {recommendation}', 'info')
    return render_template('dashboard.html', recommendation=recommendation)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

