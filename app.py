import os
import json
import sqlite3
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_booking_key_for_prod')

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

def init_db():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, type TEXT, details TEXT, price REAL, seats INTEGER, selected_seats TEXT, total REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
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
    elif dtype == 'flights':
        df = pd.read_csv(os.path.join(data_dir, 'flights.csv'))
        return df.to_dict(orient='records')
    elif dtype == 'events':
        df = pd.read_csv(os.path.join(data_dir, 'events.csv'))
        return df.to_dict(orient='records')
    elif dtype == 'hotels':
        df = pd.read_csv(os.path.join(data_dir, 'hotels.csv'))
        return df.to_dict(orient='records')
    elif dtype == 'cabs':
        df = pd.read_csv(os.path.join(data_dir, 'cabs.csv'))
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
        hashed_password = generate_password_hash(password)
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=10)
            c = conn.cursor()
            c.execute("INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)", (name, phone, email, hashed_password))
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
            c.execute("SELECT * FROM users WHERE email=?", (email,))
            user = c.fetchone()
            if user and check_password_hash(user[4], password):
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

@app.route('/flights', methods=['GET', 'POST'])
def flights():
    flight_data = load_data('flights')
    if request.method == 'POST':
        source = request.form.get('source', '').lower()
        destination = request.form.get('destination', '').lower()
        if source and destination:
            flight_data = [f for f in flight_data if f['source'].lower() == source and f['destination'].lower() == destination]
    return render_template('flights.html', flights=flight_data, user=get_current_user(), request=request)

@app.route('/flights/book/<int:flight_id>')
def flight_booking(flight_id):
    if not get_current_user():
        flash('Please login to book tickets.', 'warning')
        return redirect(url_for('login'))
    flights_data = load_data('flights')
    flight = next((f for f in flights_data if f['id'] == flight_id), None)
    if not flight:
        return "Flight not found", 404
    return render_template('flight_booking.html', flight=flight, user=get_current_user())

@app.route('/events')
def events():
    events_data = load_data('events')
    return render_template('events.html', events=events_data, user=get_current_user())

@app.route('/events/book/<int:event_id>')
def event_booking(event_id):
    if not get_current_user():
        flash('Please login to book tickets.', 'warning')
        return redirect(url_for('login'))
    events_data = load_data('events')
    event = next((e for e in events_data if e['id'] == event_id), None)
    if not event:
        return "Event not found", 404
    return render_template('event_booking.html', event=event, user=get_current_user())

@app.route('/hotels')
def hotels():
    hotels_data = load_data('hotels')
    return render_template('hotels.html', hotels=hotels_data, user=get_current_user())

@app.route('/hotels/book/<int:hotel_id>')
def hotel_booking(hotel_id):
    if not get_current_user():
        flash('Please login to book tickets.', 'warning')
        return redirect(url_for('login'))
    hotels_data = load_data('hotels')
    hotel = next((h for h in hotels_data if h['id'] == hotel_id), None)
    if not hotel:
        return "Hotel not found", 404
    return render_template('hotel_booking.html', hotel=hotel, user=get_current_user())

@app.route('/cabs', methods=['GET', 'POST'])
def cabs():
    cab_data = load_data('cabs')
    if request.method == 'POST':
        source = request.form.get('source', '').lower()
        destination = request.form.get('destination', '').lower()
        if source and destination:
            cab_data = [c for c in cab_data if c['source'].lower() == source and c['destination'].lower() == destination]
    return render_template('cabs.html', cabs=cab_data, user=get_current_user(), request=request)

@app.route('/cabs/book/<int:cab_id>')
def cab_booking(cab_id):
    if not get_current_user():
        flash('Please login to book tickets.', 'warning')
        return redirect(url_for('login'))
    cabs_data = load_data('cabs')
    cab = next((c for c in cabs_data if c['id'] == cab_id), None)
    if not cab:
        return "Cab not found", 404
    return render_template('cab_booking.html', cab=cab, user=get_current_user())

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
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    cart = session.get('cart', [])
    if cart:
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=10)
            c = conn.cursor()
            for item in cart:
                c.execute("INSERT INTO bookings (user_id, type, details, price, seats, selected_seats, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (user[0], item['type'], item['details'], item['price'], item['seats'], item['selected_seats'], item['total']))
            conn.commit()
        except Exception as e:
            flash(f'Error saving booking: {str(e)}', 'danger')
        finally:
            if conn:
                conn.close()
                
    session.pop('cart', None)
    return render_template('success.html', user=user)

@app.route('/my_bookings')
def my_bookings():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    conn = None
    bookings = []
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM bookings WHERE user_id=? ORDER BY created_at DESC", (user[0],))
        bookings = c.fetchall()
    except Exception as e:
        flash(f'Error fetching bookings: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
            
    return render_template('my_bookings.html', user=user, bookings=bookings)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
