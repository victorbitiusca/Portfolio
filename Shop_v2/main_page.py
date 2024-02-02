from mysql.connector import connect

from prettytable import PrettyTable


def validate_user(user_type):
    auth_list = []
    result = execute_sql(f"SELECT * FROM {user_type};")
    for row in result:
        auth_list.append(row[1:])
    user_name = input("Please provide username: ")
    password = input("Please provide password: ")
    while True:
        if (user_name, password) in auth_list:
            return True
        else:
            print("Wrong username or password!")
            choice = input("Would you like to try again? Y/N ")
            if choice.lower() == "y":
                user_name = input("Please provide username: ")
                password = input(f"Please provide password for user {user_name}: ")
            else:
                return False


def show_products_list():
    result = execute_sql(f"SELECT * FROM products;")
    for product_data in result:
        print(f"{product_data[0]}. {product_data[1]}, {product_data[2]} kg available, {product_data[3]} RON/kg")


def execute_sql(sql_command):
    with connect(host="localhost", user="root", password="Quantum1988!", database="first_db", autocommit=True) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_command)
            if "SELECT" in sql_command:
                result = cursor.fetchall()
                return result


def modify_inventory():
    if validate_user("admin"):
        print("Welcome, Admin")
        show_products_list()
        while True:
            product_id = int(input("Choose what product to modify: "))
            chosen_product = execute_sql(f"SELECT name FROM products WHERE id={product_id};")
            print(f"You have chosen: {chosen_product}")
            choice2 = int(input("What would you like to modify? (1 - quantity, 2 - price)"))
            if choice2 == 1:
                print("You have chosen to modify quantity")
                new_quantity = float(input("Enter new quantity: "))
                save_product_to_db(product_id, 'available_quantity', new_quantity)
            elif choice2 == 2:
                print("You have chosen to modify price")
                new_price = float(input("Enter new price: "))
                save_product_to_db(product_id, 'price_per_kg', new_price)
            else:
                print("Invalid input")
            print("List of products is now: ")
            show_products_list()
            action = input("Would you like to modify another product? Y/N")
            if action.lower() != "y":
                print("Goodbye!")
                break


def save_product_to_db(id, col_name, new_value):
    execute_sql(f'UPDATE products SET {col_name}={new_value} WHERE id={id};')


def update_history(history, prd_name, qty, price):
    if prd_name not in history:
        history[prd_name] = [qty, price]
    else:
        history[prd_name][0] += qty
        history[prd_name][1] += price


def print_report(history):
    pt = PrettyTable(["Product", "Quantity", "Price"])
    # dict contine nume: [cantitate, pret] si
    # add_row are nevoie de [nume, cantitate, pret]
    for key in history:
        pt.add_row([key, f"{history[key][0]} kg", f"{history[key][1]} RON"])
    print(pt)


def buy_product():
    if validate_user("clients"):
        total_price = 0
        h = {}
        while True:
            show_products_list()
            product_id = int(input("What would you like to buy?"))
            chosen_product_data = execute_sql(f'SELECT * FROM products WHERE id={product_id};')
            _, product_name, available_quantity, price_per_kg = chosen_product_data[0]
            print(f"You have chosen {product_name}.")
            if available_quantity == 0:
                print("Product depleted. Please choose another product.")
                continue
            while True:
                chosen_quantity = int(input("How many kg would you like to buy?"))
                if chosen_quantity > available_quantity or chosen_quantity < 0:
                    print("Invalid number of kgs. Please type number again.")
                    continue
                break
            total_price_pp = chosen_quantity * price_per_kg
            print(f"You have bought {chosen_quantity} kg of "
                  f"{product_name} for {total_price_pp} RON.")
            update_history(h, product_name, chosen_quantity, total_price_pp)
            total_price += total_price_pp
            new_quantity = available_quantity - chosen_quantity
            save_product_to_db(product_id, 'available_quantity', new_quantity )
            choice3 = input("Would you like to buy anything else? Y/N")
            if choice3.lower() != "y":
                print("Thank you for your purchase! Here's your report: ")
                print_report(h)
                print("Your total price is: ", total_price, "RON")
                break


def show_menu():
    while True:
        print("Press 1 for admin, 2 for buyer or 0 to exit: ")
        choice = int(input())
        if choice == 1:
            modify_inventory()
        elif choice == 2:
            buy_product()
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid input.")


show_menu()
