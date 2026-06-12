# canteen_order.py

print("===== CANTEEN ORDER SYSTEM =====")

menu = {
    1: ("Burger", 50),
    2: ("Pizza", 120),
    3: ("Sandwich", 40),
    4: ("Tea", 15),
    5: ("Coffee", 25)
}

total_bill = 0

while True:
    print("\nMenu:")
    for key, value in menu.items():
        print(f"{key}. {value[0]} - ₹{value[1]}")

    choice = int(input("\nEnter item number: "))

    if choice in menu:
        quantity = int(input("Enter quantity: "))
        item_name = menu[choice][0]
        item_price = menu[choice][1]

        cost = item_price * quantity
        total_bill += cost

        print(f"{item_name} x {quantity} = ₹{cost}")
    else:
        print("Invalid choice!")

    more = input("Order more items? (y/n): ").lower()
    if more != 'y':
        break

print("\n===== FINAL BILL =====")
print(f"Total Amount = ₹{total_bill}")
print("Thank You! Visit Again.")