# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm
from operation_user import UserOperation
from model_admin import Admin
import time


class AdminOperation:

    # Register the admin before the program start
    def register_admin(self):
        user_operator = UserOperation()

        # assuming this as admin username
        admin_username = "admin"

        # assuming this as admin password
        admin_password = "admin1"

        if user_operator.check_username_exist(admin_username):
            print("Admin username already exists!")
            return

        if not user_operator.validate_password(admin_password):
            print("Invalid admin password!")
            return

        user_id = user_operator.generate_unique_user_id()
        user_register_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        admin = Admin(
            user_id,
            admin_username,
            user_operator.encrypt_password(admin_password),
            user_register_time,
            "admin"
        )

        with open("./data/users.txt", "a", encoding="utf-8") as file:
            file.write(str(admin) + '\n')

        print("Admin account successfully registered.")
