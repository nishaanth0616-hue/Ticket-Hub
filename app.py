import os
import json
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_booking_key_for_prod')

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

def init_db():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_current_user():
    if 'user_id' in session:
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=10)
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?", (session['user_id'],))
            user = c.fetchone()
            return user
        except Exception:
            return None
        finally:
            if conn:
                conn.close()
    return None

def load_data(dtype):
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    if dtype == 'movies':
        with open(os.path.join(data_dir, 'movies.json'), 'r') as f:
            return json.load(f)
    elif dtype == 'buses':
        df = pd.read_csv(os.path.join(data_dir, 'buses.csv'))
        return df.to_dict(orient='records')
    elif dtype == 'trains':
        df = pd.read_csv(os.path.join(data_dir, 'trains.csv'))
        return df.to_dict(orient='records')
    return []

@app.route('/')
def index():
    return render_template('index.html', user=get_current_user())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=10)
            c = conn.cursor()
            c.execute("INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)", (name, phone, email, password))
            conn.commit()
            flash('Account created successfully! Welcome to the future.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Error: This email is already registered.', 'danger')
        except Exception as e:
            flash(f'An unexpected error occurred: {str(e)}', 'danger')
        finally:
            if conn:
                conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=10)
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials.', 'danger')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            if conn:
                conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('cart', None)
    return redirect(url_for('index'))

@app.route('/movies')
def movies():
    movies_data = load_data('movies')
    return render_template('movies.html', movies=movies_data, user=get_current_user())

@app.route('/movies/book/<int:movie_id>')
def movie_booking(movie_id):
    if not get_current_user():
        flash('Please login to book tickets.', 'warning')
        return redirect(url_for('login'))
    movies_data = load_data('movies')
    movie = next((m for m in movies_data if m['id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_booking.html', movie=movie, user=get_current_user())

@app.route('/buses', methods=['GET', 'POST'])
def buses():
    bus_data = load_data('buses')
    if request.method == 'POST':
        source = request.form.get('source', '').lower()
        destination = request.form.get('destination', '').lower()
        if source and destination:
            bus_data = [b for b in bus_data if b['source'].lower() == source and b['destination'].lower() == destination]
    return render_template('buses.html', buses=bus_data, user=get_current_user(), request=request)

@app.route('/buses/book/<int:bus_id>')
def bus_booking(bus_id):
    if not get_current_user():
        flash('Please login to book tickets.', 'warning')
        return redirect(url_for('login'))
    buses_data = load_data('buses')
    bus = next((b for b in buses_data if b['id'] == bus_id), None)
    if not bus:
        return "Bus not found", 404
    return render_template('bus_booking.html', bus=bus, user=get_current_user())

@app.route('/trains', methods=['GET', 'POST'])
def trains():
    train_data = load_data('trains')
    if request.method == 'POST':
        source = request.form.get('source', '').lower()
        destination = request.form.get('destination', '').lower()
        if source and destination:
            train_data = [t for t in train_data if t['source'].lower() == source and t['destination'].lower() == destination]
    return render_template('trains.html', trains=train_data, user=get_current_user(), request=request)

@app.route('/trains/book/<int:train_id>')
def train_booking(train_id):
    if not get_current_user():
        flash('Please login to book tickets.', 'warning')
        return redirect(url_for('login'))
    train_data = load_data('trains')
    train = next((t for t in train_data if t['id'] == train_id), None)
    if not train:
        return "Train not found", 404
    return render_template('train_booking.html', train=train, user=get_current_user())

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if not get_current_user():
        return redirect(url_for('login'))
    item_type = request.form.get('type')
    details = request.form.get('details')
    price = float(request.form.get('price', 0))
    seats = int(request.form.get('seats', 1))
    selected_seats = request.form.get('selected_seats', '')
    
    total = price * seats
    
    if 'cart' not in session:
        session['cart'] = []
        
    cart = session['cart']
    cart.append({
        'type': item_type,
        'details': details,
        'price': price,
        'seats': seats,
        'selected_seats': selected_seats,
        'total': total
    })
    session['cart'] = cart
    flash('Added to cart successfully!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    if not get_current_user():
        return redirect(url_for('login'))
    cart = session.get('cart', [])
    total_amount = sum(item['total'] for item in cart)
    return render_template('cart.html', cart=cart, total_amount=total_amount, user=get_current_user())

@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    if not get_current_user():
        return redirect(url_for('login'))
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('index'))
    total_amount = sum(item['total'] for item in cart)
    return render_template('payment.html', total_amount=total_amount, user=get_current_user())

@app.route('/process_payment', methods=['POST'])
def process_payment():
    session.pop('cart', None)
    return render_template('success.html', user=get_current_user())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
