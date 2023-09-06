# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm

from operation_user import UserOperation
from operation_order import OrderOperation
from operation_customer import CustomerOperation
from operation_admin import AdminOperation
from opreation_product import ProductOperation
from io_interface import Interface
import time


# This method is to control the login
def login_control():
    interface = Interface()
    user_operation = UserOperation()
    username, password = interface.get_user_input("Enter username and password: ", 2)
    if not user_operation.validate_password(password):
        interface.print_error_message("UserOperation.login", "password incorrect")
    elif not user_operation.validate_username(username):
        interface.print_error_message("UserOperation.login", "username incorrect")
    with open("./data/users.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        user_data = eval(line.strip())
        register_name = user_data['user_name']
        if username == register_name:
            encrypted_password = user_data['user_password']
            decrypted_password = user_operation.decrypt_password(encrypted_password)
            print(f"User ID: {user_data['user_id']}, decrypted password: {decrypted_password}")
    login_result = user_operation.login(username, password)
    if login_result is not None:
        if login_result.user_role == "admin":
            interface.print_message(f"Welcome Admin {username} login succeeded")
            admin_control()
        else:
            interface.print_message(f"Welcome Customer {username} login succeeded")
            # objects = interface.get_user_input("Please input which object you want?", 1)
            customer_control(login_result)
    else:
        interface.print_error_message("UserOperation.login", "Please input correct things")


def customer_control(object):
    interface = Interface()

    # Create an instance of ProductOperation class
    product_operation = ProductOperation()

    # Create an instance of OrderOperation class
    order_operation = OrderOperation()
    customer_operation = CustomerOperation()

    # Show admin menu
    while True:
        interface.customer_menu()
        customer_choice = interface.get_user_input("Enter your choice: ", 1)

        # Show profile
        if customer_choice == '1':
            interface.print_object(object)

        # Update profile
        elif customer_choice == '2':
            customer_input, value = interface.get_user_input(
                "enter the attribute and value you want to Update(eg: user_name Zhicheng)",
                2)
            interface.print_message("You can change (eg: user_name, user_mobile,user_password, user_email)")
            if not customer_input or not value:
                print("You need to enter four arguments: name, password, email, and mobile.")
            else:
                update = customer_operation.update_profile(customer_input, value, object)
                if update:
                    interface.print_message("Update successful!")
                else:
                    interface.print_error_message("Update profile", "Invalid input")

        # Show products
        elif customer_choice == '3':
            style = interface.get_user_input("Please input the style (keyword or page) you want to show", 1)
            style = style.lower()
            if style == 'keyword':
                product = interface.get_user_input("Please input which keyword you want to show", 1)
                product = product.lower()
                product_list = product_operation.get_product_list_by_keyword(product)
                interface.show_list("customer", "Product", product_list)
                interface.print_message("Show product successful")
                create = interface.get_user_input("Do you want to create an order? (yes/no)", 1)
                create = create.lower()
                if create == "yes":
                    product_id = interface.get_user_input("Please input the product id you want to create", 1)
                    product_price = interface.get_user_input("Please input the product price you want to create", 1)
                    order_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    order_operation.create_an_order(object.user_id, product_id, product_price, order_time)
                    interface.print_message("Create successful")
                else:
                    continue
            elif style == 'page':
                page_number = interface.get_user_input("Please input which page you want to show", 1)
                try:
                    page_number = int(page_number)
                except ValueError:
                    interface.print_message("Invalid input. Please enter a valid number.")
                else:
                    page = product_operation.get_product_list(page_number)
                    interface.show_list("customer", "Product", page)
                    interface.print_message("Show products successful")
            else:
                interface.print_error_message("Show product",
                                              "Invalid input, you must input 'keyword' or 'page' first")

        # Show history order
        elif customer_choice == '4':
            order = interface.get_user_input("please enter the order page you want to show", 1)
            try:
                order = int(order)
            except ValueError:
                interface.print_message("Invalid input. Please enter a valid number.")
            else:
                order_list = order_operation.get_order_list(object.user_id, order)
                interface.show_list("customer", "Order", order_list)
                interface.print_message("Show order successful")

        # Generate all consumption figures
        elif customer_choice == '5':
            interface.print_message("Start to generate single_customer_consumption figures")
            order_operation.generate_single_customer_consumption_figure(object.user_id)
            interface.print_message("generate single_customer_consumption figures finished")

        # Get a product by product id
        elif customer_choice == '6':
            create = interface.get_user_input("Do you want to get a product? (yes/no)", 1)
            create = create.lower()
            if create == "yes":
                product_id = interface.get_user_input("Please input the product id you want to create", 1)
                product_price = interface.get_user_input("Please input the product price you want to create", 1)
                order_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                order_operation.create_an_order(object.user_id, product_id, product_price, order_time)
                interface.print_message("Create successful")
            else:
                continue

        # Logout
        elif customer_choice == '7':
            interface.print_message("logout successful")
            break

        # Add customer menu choices here


def admin_control():
    interface = Interface()

    # Create an instance of ProductOperation class
    product_operation = ProductOperation()

    # Create an instance of OrderOperation class
    order_operation = OrderOperation()
    customer_operation = CustomerOperation()
    # Show admin menu
    while True:
        interface.admin_menu()
        admin_choice = interface.get_user_input("Enter your choice: ", 1)

        # Show products
        if admin_choice == '1':
            page = interface.get_user_input("Please select the page that you want to check", 1)
            try:
                page = int(page)
            except ValueError:
                interface.print_message("Invalid input. Please enter a valid number.")
            else:
                object_list = product_operation.get_product_list(page)
                interface.show_list("admin", "Product", object_list)
                interface.print_message("Show products successful!")

        # Add customers
        elif admin_choice == '2':
            name, password, email, mobile = interface.get_user_input("Please enter the (name password email mobile)", 4)
            # Verify that the user has entered four arguments
            if not name or not password or not email or not mobile:
                print("You need to enter four arguments: name, password, email, and mobile.")
            else:
                register = customer_operation.register_customer(name, password, email, mobile)
                if register:
                    interface.print_message(f"Customer {name} created successfully")
                else:
                    interface.print_error_message("Customer.register", "Register error")

        # Show customers
        elif admin_choice == '3':
            page = interface.get_user_input("Please select the page that you want to check", 1)
            try:
                page = int(page)
            except ValueError:
                interface.print_message("Invalid input. Please enter a valid number.")
            else:
                object_list = customer_operation.get_customer_list(page)
                interface.show_list("admin", "Customer", object_list)
                interface.print_message("Show customers successful!")

        # Show orders
        elif admin_choice == '4':
            customer_id = interface.get_user_input("Please select customer id that you want to check", 1)
            page = interface.get_user_input("Please select page that you want to check", 1)
            try:
                page = int(page)
            except ValueError:
                interface.print_message("Invalid input. Please enter a valid number.")
            else:
                if not customer_id or not page:
                    print("You need to enter two arguments: customer_id, page.")
                else:
                    object_list = order_operation.get_order_list(customer_id, page)
                    interface.show_list("admin", "Order", object_list)
                    interface.print_message("Show orders successful!")

        # Generate test data
        elif admin_choice == '5':
            interface.print_message("Start to generate the test data")
            product_operation.extract_products_from_files()
            order_operation.generate_test_order_data()
            interface.print_message("Test data finished")

        # Generate all statistical figures
        elif admin_choice == '6':
            interface.print_message("Start to generate category figures")
            product_operation.generate_category_figure()
            interface.print_message("generate category figures finished")

            interface.print_message("Start to generate discount figures")
            product_operation.generate_discount_figure()
            interface.print_message("generate discount figures finished")

            interface.print_message("Start to generate discount_likes_count figures")
            product_operation.generate_discount_likes_count_figure()
            interface.print_message("generate discount_likes_count figures finished")

            interface.print_message("Start to generate likes_count figures")
            product_operation.generate_likes_count_figure()
            interface.print_message("generate likes_count figures finished")

            interface.print_message("All Product figures finished")

            interface.print_message("Start to generate all_customers_consumption figures")
            order_operation.generate_all_customers_consumption_figure()
            interface.print_message("generate all_customers_consumption figures finished")

            interface.print_message("Start to generate all_top_10_best_sellers figures")
            order_operation.generate_all_top_10_best_sellers_figure()
            interface.print_message("generate all_top_10_best_sellers figures finished")

            interface.print_message("All statistical figures generate finished")

        # Delete all data
        elif admin_choice == '7':
            interface.print_message("Start to delete all data")

            interface.print_message("Start to delete Customer data")
            customer_operation.delete_all_customers()
            interface.print_message("Customer data has been deleted")

            interface.print_message("Start to delete products data")
            product_operation.delete_all_products()
            interface.print_message("products data has been deleted")

            interface.print_message("Start to delete orders data")
            order_operation.delete_all_orders()
            interface.print_message("orders data has been deleted")

            interface.print_message("Delete all data")

        # Delete the customer by customer id
        elif admin_choice == '8':
            delete = interface.get_user_input("Do you want to delete a customer? (yes/no)", 1)
            delete = delete.lower()
            if delete == "yes":
                customer_id = interface.get_user_input("Please input the customer id you want to delete", 1)
                customer_operation.delete_customer(customer_id)
                interface.print_message("Delete successful")
            elif delete == "no":
                continue
            else:
                interface.print_error_message("Invalid input", "Please input 'yes' or 'no'")

        # Delete order by order id
        elif admin_choice == '9':
            delete = interface.get_user_input("Do you want to delete an order? (yes/no)", 1)
            delete = delete.lower()
            if delete == "yes":
                order_id = interface.get_user_input("Please input the order id you want to delete", 1)
                order_operation.delete_order(order_id)
                interface.print_message("Delete successful")
            elif delete == "no":
                continue
            else:
                interface.print_error_message("Invalid input", "Please input 'yes' or 'no'")

        # Delete Product by product id
        elif admin_choice == '10':
            delete = interface.get_user_input("Do you want to delete a product? (yes/no)", 1)
            delete = delete.lower()
            if delete == "yes":
                product_id = interface.get_user_input("Please input the product id you want to delete", 1)
                product_operation.delete_product(product_id)
                interface.print_message("Delete successful")
            elif delete == "no":
                continue
            else:
                interface.print_error_message("Invalid input", "Please input 'yes' or 'no'")

        # Logout
        elif admin_choice == '11':
            interface.print_message("logout successful")
            break

    # Add admin menu choices here


def main():
    # Create an instance of Interface class
    interface = Interface()

    # Create an instance of ProductOperation class
    product_operation = ProductOperation()

    # Create an instance of OrderOperation class
    order_operation = OrderOperation()

    # Instantiate an AdminOperation object to manage administrator-related operations
    admin_operation = AdminOperation()

    # Instantiate a CustomerOperation object to manage customer-related operations
    customer_operation = CustomerOperation()

    # Use the CustomerOperation object to delete all existing customers
    customer_operation.delete_all_customers()

    # Use the OrderOperation object to delete all existing orders
    order_operation.delete_all_orders()

    # Use the ProductOperation object to extract product data from files
    product_operation.extract_products_from_files()

    # Use the OrderOperation object to generate test order data
    order_operation.generate_test_order_data()

    # Use the AdminOperation object to register an admin
    admin_operation.register_admin()

    # Print a welcome message to the shopping system
    interface.print_message("Welcome to shopping system")

    # Start with main_menu
    while True:
        # Show main menu and get user choice
        interface.main_menu()
        user_choice = interface.get_user_input("Enter your choice: ", 1)

        # Check if the user wants to quit
        if user_choice == '3':
            product_operation.delete_all_products()
            break

        # Check if the user wants to login
        elif user_choice == '1':
            login_control()

        # Check if the user wants to register
        elif user_choice == '2':
            name, password, email, mobile = interface.get_user_input("Please enter the (name password email mobile)", 4)
            register = False
            # Verify that the user has entered four arguments
            if not name or not password or not email or not mobile:
                print("You need to enter four arguments: name, password, email, and mobile.")
            else:
                register = customer_operation.register_customer(name, password, email, mobile)
            if register:
                interface.print_message("Customer created successfully")
            else:
                interface.print_error_message("Customer.register", "Register error")
                print(name, password, email, mobile)

        else:
            interface.print_error_message("Main menu", "Invalid input")

    # Print a goodbye message
    product_operation.delete_all_products()
    interface.print_message("Thank you for using our system, goodbye!")


if __name__ == "__main__":
    main()
