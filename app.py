
from flask import Flask, render_template, request, redirect, url_for, session, flash ,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import bcrypt
from datetime import datetime
import pytz

timestamp = datetime.now(pytz.timezone("Asia/Dubai")).strftime('%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Database helper function
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Ensure the correct file name
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call this function before running the app
create_tables()

# Function to fetch menu items
def get_menu_items(query=None):
    conn = get_db_connection()
    if query:
        query = f"%{query}%"
        menu_items = conn.execute('SELECT * FROM menu WHERE name LIKE ?', (query,)).fetchall()
    else:
        menu_items = conn.execute('SELECT * FROM menu').fetchall()
    conn.close()
    return menu_items


# Home route
@app.route('/')
def home():
    flash('wellcome to our reataurant website.', 'success')
    return render_template('index.html')

# Sign In (Registration) route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    # your logic here

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password, location) VALUES (?, ?, ?)',
                         (username, hashed_password, None))
            conn.commit()
            flash("Signin successful! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
            return redirect(url_for('signin'))
        finally:
            conn.close()
    return render_template('signin.html')



# Log In route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Log Out route
@app.route('/logout')
def logout():
    session.clear()
    session['alert'] = {'message': 'You have successfully logged out.', 'type': 'info'}
    return redirect(url_for('home'))



# Route to Update Location
@app.route("/update_location", methods=["POST"])
def update_location():
    if "user_id" not in session:
        return redirect(url_for("login"))

    new_location = request.form.get("location")
    
    if not new_location:
        flash("Location cannot be empty!", "warning")
        return redirect(url_for("profile"))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update location
    cursor.execute("UPDATE users SET location = ? WHERE id = ?", (new_location, session["user_id"]))
    conn.commit()
    conn.close()

    flash("Location updated successfully!", "success")
    return redirect(url_for("profile"))

# Route to Show Last Order
@app.route("/last_order")
def last_order():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT last_order FROM users WHERE id = ?", (session["user_id"],))
    last_order = cursor.fetchone()
    conn.close()

    return {"last_order": last_order["last_order"] if last_order else "No orders found"}


# Update Password
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' not in session:
        return redirect('/login')

    new_password = request.form['password']
    hashed_password = generate_password_hash(new_password)

    conn = get_db_connection()
    conn.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, session['username']))
    conn.commit()
    conn.close()

    flash("Password updated successfully!", "success")
    return redirect('/profile')
# Restricted Menu Page with Search and Order Now button
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    query = request.form.get('search')
    items = get_menu_items(query)
    return render_template('menu.html', menu_items=items)

@app.route('/cart')
def cart():
    total_price = sum(item['price'] * item['quantity'] for item in session.get('cart', {}).values())
    session['total_price'] = total_price
    return render_template('cart.html')

# Add to cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_name = request.form['item_name']
    item_price = float(request.form['item_price'])

    if 'cart' not in session:
        session['cart'] = {}

    if item_name in session['cart']:
        session['cart'][item_name]['quantity'] += 1
    else:
        session['cart'][item_name] = {'price': item_price, 'quantity': 1}

    session.modified = True
    flash(f"{item_name} added to cart!", "success")
    return redirect(url_for('cart'))

# Remove item from cart
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_name = request.form['item_name']

    if 'cart' in session and item_name in session['cart']:
        del session['cart'][item_name]

    session.modified = True
    flash(f"{item_name} removed from cart!", "danger")
    return redirect(url_for('cart'))

# Update item quantity (increase/decrease)
@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    item_name = request.form['item_name']
    action = request.form['action']

    if 'cart' in session and item_name in session['cart']:
        if action == "increase":
            session['cart'][item_name]['quantity'] += 1
        elif action == "decrease" and session['cart'][item_name]['quantity'] > 1:
            session['cart'][item_name]['quantity'] -= 1
        elif action == "decrease" and session['cart'][item_name]['quantity'] == 1:
            del session['cart'][item_name]  # Remove item if quantity reaches zero

    session.modified = True
    return redirect(url_for('cart'))

# Checkout (Clear Cart and Show Final Price)
@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first!"}), 401

    data = request.get_json()
    cart_items = data.get("cart", [])

    if not cart_items:
        return jsonify({"message": "Cart is empty!"}), 400

    # Here, you would save the order to your database
    print("Saving order:", cart_items)  # Debugging

    return jsonify({"message": "Order placed successfully!"}), 200


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user_id = session['user_id']

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        location = request.form['location']

        conn.execute(
            "UPDATE users SET username = ?, password = ?, location = ? WHERE id = ?",
            (username, password, location, user_id)
        )
        conn.commit()
        conn.close()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    return render_template('profile.html', user=user)


# 📌 Route for Submitting an Order
@app.route('/submit_order', methods=['POST'])
def submit_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user_id = session['user_id']

    # Get user location
    user = conn.execute("SELECT location FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user['location']:
        flash("Please set your location in your profile before ordering!", "warning")
        return redirect(url_for('profile'))

    cart = request.json.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert order into database
    conn.execute(
        "INSERT INTO orders (user_id, total_price, location, order_time) VALUES (?, ?, ?, ?)",
        (user_id, total_price, user['location'], timestamp)
    )
    order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # Insert order items
    for item in cart:
        conn.execute(
            "INSERT INTO order_items (order_id, item_name, price, quantity) VALUES (?, ?, ?, ?)",
            (order_id, item['name'], item['price'], item['quantity'])
        )

    conn.commit()
    conn.close()
    
    flash("Order submitted successfully!", "success")
    return redirect(url_for('my_orders'))


# 📌 Route for Viewing Order History
@app.route('/my_orders')
def my_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user_id = session['user_id']
    orders = conn.execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY order_time DESC",
        (user_id,)
    ).fetchall()
    conn.close()

    return render_template('my_orders.html', orders=orders)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # You can add logic here to save the message or send an email
    session['alert'] = {'message': 'message have sended successfully.', 'type': 'success'}
    return redirect(url_for('about'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





