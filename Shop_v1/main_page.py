from product import Product

from prettytable import PrettyTable


def validate_user(user_credentials_file):
    with open(user_credentials_file) as f:
        auth_list = []
        for row in f:
            valid_user_name, valid_password = row.strip().split(", ")
            auth_list.append((valid_user_name, valid_password))
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


def get_products_list():
    products_list = []
    with open("products.txt") as f:
        for row in f:
            name, quantity, price = row.split(", ")
            quantity = float(quantity.strip())
            price = float(price.strip())
            product = Product(name, quantity, price)
            products_list.append(product)
    return products_list


def show_products_list(products_lst):
    for index, product in enumerate(products_lst):
        print(f"{index + 1}. {product}")


def modify_inventory():
    if validate_user("admin_credentials.txt"):
        print("Welcome, Admin")
        products_list = get_products_list()
        show_products_list(products_list)
        while True:
            choice = int(input("Choose what product to modify: "))
            # - 1 pentru ca primul index e 0 pt liste
            chosen_product = products_list[choice - 1]
            print(f"You have chosen: {chosen_product}")
            choice2 = int(input("What would you like to modify? (1 - quantity, 2 - price)"))
            if choice2 == 1:
                print("You have chosen to modify quantity")
                new_quantity = float(input("Enter new quantity: "))
                chosen_product.available_quantity = new_quantity
            elif choice2 == 2:
                print("You have chosen to modify price")
                new_price = float(input("Enter new price: "))
                chosen_product.price_per_kg = new_price
            else:
                print("Invalid input")
            print("List of products is now: ")
            show_products_list(products_list)
            save_products_to_file(products_list)
            action = input("Would you like to modify another product? Y/N")
            if action.lower() != "y":
                print("Goodbye!")
                break


def save_products_to_file(prd_lst):
    with open("products.txt", "w") as f:
        for prd in prd_lst:
            f.write(f"{prd.name}, {prd.available_quantity}, {prd.price_per_kg}\n")


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
    if validate_user("clients.txt"):
        total_price = 0
        products_list = get_products_list()
        h = {}
        while True:
            show_products_list(products_list)
            choice = int(input("What would you like to buy?"))
            chosen_product = products_list[choice - 1]
            print(f"You have chosen {chosen_product}.")
            if chosen_product.available_quantity == 0:
                print("Product depleted. Please choose another product.")
                continue
            while True:
                chosen_quantity = int(input("How many kg would you like to buy?"))
                if chosen_quantity > chosen_product.available_quantity or chosen_quantity < 0:
                    print("Invalid number of kgs. Please type number again.")
                    continue
                break
            total_price_pp = chosen_quantity * chosen_product.price_per_kg
            print(f"You have bought {chosen_quantity} kg of "
                  f"{chosen_product.name} for {total_price_pp} RON.")
            update_history(h, chosen_product.name, chosen_quantity, total_price_pp)
            # pt.add_row([chosen_product.name, f"{chosen_quantity} kg", f"{total_price_pp} RON"])
            total_price += total_price_pp
            chosen_product.available_quantity -= chosen_quantity
            save_products_to_file(products_list)
            choice3 = input("Would you like to buy anything else? Y/N")
            if choice3.lower() != "y":
                print("Thank you for your purchase! Here's your report: ")
                # print(h)
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


# validate_admin()
# prod = get_products_list()
# show_products_list(prod)
show_menu()

