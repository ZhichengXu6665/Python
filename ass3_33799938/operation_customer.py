# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm
import re
from operation_user import UserOperation
import time
from model_customer import Customer
import math


class CustomerOperation:

    # Check it is a validate email or not
    def validate_email(self, user_email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, user_email):
            return False
        return True

    # Check it is a validate mobile
    def validate_mobile(self, user_mobile):
        if len(user_mobile) != 10:
            return False
        if not user_mobile.isdigit():
            return False
        if not (user_mobile.startswith('04') or user_mobile.startswith('03')):
            return False
        return True

    def register_customer(self, user_name, user_password, user_email, user_mobile):
        user_operator = UserOperation()

        # check user_name and password
        if not user_operator.validate_username(user_name) or not user_operator.validate_password(user_password):
            return False

        # Check email and mobile phone
        if not self.validate_email(user_email) or not self.validate_mobile(user_mobile):
            return False

        # Check the user name exist or not
        if user_operator.check_username_exist(user_name):
            return False

        # Generate the register time
        user_id = user_operator.generate_unique_user_id()
        register_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Encrypted the password
        encrypted_password = user_operator.encrypt_password(user_password)

        # Create  an new customer
        new_customer = Customer(user_id, user_name, encrypted_password, register_time, 'customer', user_email,
                                user_mobile)

        # write the user in to the file
        with open("./data/users.txt", "a", encoding="utf-8") as file:
            file.write(str(new_customer) + "\n")

        return True

    # Update the message
    def update_profile(self, attribute_name, value, customer_object):
        user_operator = UserOperation()
        # Update the user name
        if attribute_name == "user_name":
            if not user_operator.validate_username(value):
                return False
            if user_operator.check_username_exist(value):
                return False
            customer_object.user_name = value
        # Update the password
        elif attribute_name == "user_password":
            if not user_operator.validate_password(value):
                return False
            customer_object.user_password = user_operator.encrypt_password(value)

        # Update the email
        elif attribute_name == "user_email":
            if not self.validate_email(value):
                return False
            customer_object.user_email = value

        # Update the mobile phone number
        elif attribute_name == "user_mobile":
            if not self.validate_mobile(value):
                return False
            customer_object.user_mobile = value
        else:
            return False

        # Write the new message into the file
        users = []
        with open("./data/users.txt", "r", encoding="utf-8") as file:
            users = [eval(line.strip()) for line in file.readlines()]
        for idx in range(len(users)):
            if customer_object.user_id == users[idx]['user_id']:
                users[idx] = eval(str(customer_object))
        with open("./data/users.txt", "w", encoding="utf-8") as file:
            for user in users:
                file.write(str(user) + "\n")

        return True

    # Delete the customer by customer id
    def delete_customer(self, customer_id):
        with open("./data/users.txt", "r", encoding="utf-8") as file:
            users = [eval(line.strip()) for line in file.readlines()]

        for i in range(len(users)):
            if users[i]['user_id'] == customer_id:
                del users[i]
                with open("./data/users.txt", "w", encoding="utf-8") as file:
                    for user in users:
                        file.write(str(user) + "\n")
                return True

        return False

    # Get the customer list
    def get_customer_list(self, page_number):
        with open("./data/users.txt", "r", encoding="utf-8") as file:
            users = [eval(line.strip()) for line in file.readlines()]

        customers = []
        for user in users:
            if user['user_role'] == 'customer':
                customers.append(user)
        total_page = math.ceil(len(customers) / 10)
        start = (page_number - 1) * 10
        end = start + 10
        customer_list = customers[start:end]

        return (customer_list, page_number, total_page)

    # Delete all the customers
    def delete_all_customers(self):
        with open("./data/users.txt", "r", encoding="utf-8") as file:
            users = [eval(line.strip()) for line in file.readlines()]

        users_list = []
        for user in users:
            if user['user_role'] != 'customer':
                users_list.append(user)

        with open("./data/users.txt", "w", encoding="utf-8") as file:
            for user in users_list:  # Change from 'users' to 'users_list'
                file.write(str(user) + "\n")
