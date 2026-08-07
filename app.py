from flask import Flask, render_template, redirect,url_for, request,session

app = Flask(__name__)

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

users = {
    "admin": "1234",
    "student": "1111"
}


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

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:

            session['user'] = username

            return redirect(url_for('Home'))

        else:
            return render_template(
                'login.html',
                error="Invalid Username or Password"
            )

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('Home'))

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

    orders.append({
        "customer_name": customer_name,
        "table_number": table_number,
        "payment": payment,
        "items": cart.copy()
    })

    cart.clear()

    return render_template(
        'order_success.html',
        customer_name=customer_name,
        table_number=table_number,
        payment=payment
    )
@app.route('/admin')
def admin():
    total_orders = len(orders)

    total_revenue = 0
    for order in orders:
        for item in order["items"]:
            total_revenue += item["price"] * item["quantity"]

    return render_template(
        'admin.html',
        orders=orders,
        total_orders=total_orders,
        total_revenue=total_revenue
    )

if __name__== '__main__':
    app.run(debug=True)
