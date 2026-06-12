# my_project.py

# Main Entity Dictionary
canteen_info = {
    "canteen_name": "College Canteen",
    "owner": "Shlok Mitkar",
    "location": "Hingoli",
    "contact": "7498622054",
    "opening_time": "8:00 AM",
    "closing_time": "6:00 PM"
}

# List of Dictionaries (5 Records)
orders = [
    {"order_id": 101, "customer": "Lucky", "item": "Burger", "quantity": 2},
    {"order_id": 102, "customer": "Manisha", "item": "Pizza", "quantity": 1},
    {"order_id": 103, "customer": "Ram", "item": "Tea", "quantity": 3},
    {"order_id": 104, "customer": "Pawan", "item": "Coffee", "quantity": 2},
    {"order_id": 105, "customer": "Rohan", "item": "Sandwich", "quantity": 1}
]

# Bonus: Second Dictionary Type
item_prices = {
    "Burger": 50,
    "Pizza": 120,
    "Tea": 15,
    "Coffee": 25,
    "Sandwich": 40
}

# get_status() Function
def get_status():
    return "Canteen is Open"

# Challenge: search_records() Function
def search_records(customer_name):
    found = False

    for order in orders:
        if order["customer"].lower() == customer_name.lower():
            print("\nRecord Found:")
            print(order)
            found = True

    if not found:
        print("No record found.")

# Print Main Entity
print("===== CANTEEN DETAILS =====")
for key, value in canteen_info.items():
    print(f"{key}: {value}")

# Print Status
print("\nStatus:", get_status())

# Loop Through Records
print("\n===== ORDER RECORDS =====")
for order in orders:
    print(
        f"Order ID: {order['order_id']}, "
        f"Customer: {order['customer']}, "
        f"Item: {order['item']}, "
        f"Quantity: {order['quantity']}"
    )

# Search Record
name = input("\nEnter customer name to search: ")
search_records(name)