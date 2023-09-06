# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm
import random
import re
from model_admin import Admin
from model_customer import Customer


class UserOperation:

    # Generate user id
    def generate_unique_user_id(self):
        with open("./data/users.txt", "r", encoding="utf-8") as file:
            users = [eval(line.strip()) for line in file.readlines()]

        user_ids = [user['user_id'] for user in users]

        while True:
            user_id = "u_" + str(random.randint(1000000000, 9999999999))
            if user_id not in user_ids:
                return user_id

    # encrypt the password
    def encrypt_password(self, user_password):
        random_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        random_str = "".join(random.choices(random_chars, k=2 * len(user_password)))
        password_lst = list(user_password)
        random_lst = list(random_str)
        encrypted_password = "^^"
        for idx in range(len(user_password + random_str)):
            if idx % 3 == 2:
                encrypted_password += password_lst.pop(0)
            else:
                encrypted_password += random_lst.pop(0)

        encrypted_password += "$$"

        return encrypted_password

    # decrypt the password
    def decrypt_password(self, encrypted_password):
        encrypted_password = encrypted_password[2:-2]
        original_password = encrypted_password[2::3]

        return original_password

    # check the username exist or not
    def check_username_exist(self, user_name):
        with open("./data/users.txt", "r", encoding="utf-8") as file:
            users = [eval(line.strip()) for line in file.readlines()]

        user_names = [user['user_name'] for user in users]

        return user_name in user_names

    # check it is a validate user_name or not
    def validate_username(self, user_name):
        if not re.match(r'^[a-zA-Z_]{5,}$', user_name):
            return False
        return True

    # check it is a validate password or not
    def validate_password(self, user_password):
        if len(user_password) < 5:
            return False
        if not re.search(r'[a-zA-Z]', user_password):
            return False
        if not re.search(r'\d', user_password):
            return False
        return True

    # login through user_name and password
    def login(self, user_name, user_password):
        with open("./data/users.txt", "r", encoding="utf-8") as file:
            users = [eval(line.strip()) for line in file.readlines()]

        for user in users:
            if user['user_name'] == user_name and self.decrypt_password(user['user_password']) == user_password:
                if user['user_role'] == 'customer':
                    return Customer(user['user_id'], user['user_name'], user['user_password'],
                                    user['user_register_time'], user['user_role'], user['user_email'],
                                    user['user_mobile'])
                else:
                    return Admin(user['user_id'], user['user_name'], user['user_password'], user['user_register_time'],
                                 user['user_role'])

        return None
