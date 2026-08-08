from flask import Flask, render_template, redirect,url_for, request,session
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("canteen.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered!"

        conn.close()

        return "Registration successful!"

    return render_template("signup.html")

app.secret_key = "shlok_canteen_secret"

# Shlok's Canteen Data --> Food Menu
food_menu = [
    {"name": "Veg Burger", "price": 50,
     "image": "burger.png"},
    {"name": "Pizza", "price": 80,
     "image": "pizza.png"},
    {"name": "French Fries", "price": 60,
     "image": "french.png"},
    {"name": "Cold Drink", "price": 30,
     "image": "colddrink.png"},
]

# Shlok's Canteen Data --> Beverages
Milkshake_menu = [
    {"name": "Chocolate Milkshake", "price": 90,
     "image": "chocolate.png"},
    {"name": "Strawberry Milkshake", "price": 100,
     "image": "strawberry.png"},
    {"name": "Vanilla Milkshake", "price": 80,
     "image": "vanilla.png"},
    {"name": "Fresh Lime Juice", "price": 40,
     "image": "limejuice.png"},
]
# Shlok's Canteen Data --> Today's Specials
daily_specials = [
    {"name": "Chicken Burger", "price": 70},
    {"name": "Pasta", "price": 100},
    {"name": "Veg Biryani", "price": 120}
]
#cart
cart = []
orders = []

cart = []
orders = []


@app.route('/')
def Home():

    return render_template(
        'Home.html',
        daily_specials=daily_specials,
        user=session.get('user')
    )

@app.route('/Menu')
def Menu():
    return render_template(
        'Menu.html',
        food_menu=food_menu,
        Milkshake_menu=Milkshake_menu
    )
@app.route('/add_to_cart/<item_name>')
def add_to_cart(item_name):
    for item in food_menu + Milkshake_menu:
        if item["name"] == item_name:
            found = False

            for cart_item in cart:
                if cart_item["name"] == item["name"]:
                    cart_item["quantity"] += 1
                    found = True
                    break

            if not found:
                new_item = item.copy()
                new_item["quantity"] = 1
                cart.append(new_item)

            break

    return redirect(url_for('Menu'))
@app.route('/cart')
def cart_page():
    total = sum(item["price"] * item["quantity"] for item in cart)
    return render_template(
        'cart.html',
        cart=cart,
        total=total
    )
@app.route('/remove_from_cart/<item_name>')
def remove_from_cart(item_name):
    for item in cart:
        if item["name"] == item_name:
            cart.remove(item)
            break
    return redirect(url_for('cart_page'))
@app.route('/increase_quantity/<item_name>')
def increase_quantity(item_name):
    for item in cart:
        if item["name"] == item_name:
            item["quantity"] += 1
            break
    return redirect(url_for('cart_page'))

@app.route('/decrease_quantity/<item_name>')
def decrease_quantity(item_name):
    for item in cart:
        if item["name"] == item_name:
            item["quantity"] -= 1

            if item["quantity"] <= 0:
                cart.remove(item)

            break

    return redirect(url_for('cart_page'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("canteen.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, email, password FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user'] = user[1]
            session['user_id'] = user[0]

            return redirect(url_for('Home'))

        else:
            return render_template(
                'login.html',
                error="Invalid Email or Password"
            )

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('Home'))

@app.route('/my_orders')
def my_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = sqlite3.connect("canteen.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, customer_name, table_number,
               payment, total, order_date
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    orders_data = cursor.fetchall()

    conn.close()

    return render_template(
        'my_orders.html',
        orders=orders_data
    )

@app.route('/about')
def About_us():
    return render_template('About_us.html')


@app.route('/checkout')
def checkout():
    total = sum(item["price"] * item["quantity"] for item in cart)

    return render_template(
        'checkout.html',
        cart=cart,
        total=total
    )
@app.route('/place_order', methods=['POST'])
def place_order():
    customer_name = request.form['customer_name']
    table_number = request.form['table_number']
    payment = request.form['payment']

    total = sum(
        item["price"] * item["quantity"]
        for item in cart
    )

    user_id = session.get('user_id')

    conn = sqlite3.connect("canteen.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO orders
    (user_id, customer_name, table_number, payment, total, status)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    user_id,
    customer_name,
    table_number,
    payment,
    total,
    "Pending"
))

    order_id = cursor.lastrowid

    for item in cart:
        cursor.execute("""
            INSERT INTO order_items
            (order_id, food_name, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (
            order_id,
            item["name"],
            item["quantity"],
            item["price"]
        ))

    conn.commit()
    conn.close()

    cart.clear()

    return render_template(
        'order_success.html',
        customer_name=customer_name,
        table_number=table_number,
        payment=payment,
        total=total
    )
@app.route('/admin')
def admin():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect("canteen.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE id = ?",
        (session['user_id'],)
    )

    user = cursor.fetchone()

    if not user or user[0] != 'admin':
        conn.close()
        return "Access Denied! Admin only."

    cursor.execute("""
        SELECT id, customer_name, table_number,
               payment, total, order_date,status
        FROM orders
        ORDER BY id DESC
    """)

    orders_data = cursor.fetchall()

    total_orders = len(orders_data)

    cursor.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM orders
    """)

    total_revenue = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'admin.html',
        orders=orders_data,
        total_orders=total_orders,
        total_revenue=total_revenue
    )

@app.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect("canteen.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE id = ?",
        (session['user_id'],)
    )

    user = cursor.fetchone()

    if not user or user[0] != 'admin':
        conn.close()
        return "Access Denied! Admin only."

    status = request.form['status']

    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (status, order_id))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

if __name__== "__main__":
    app.run(debug=True)
