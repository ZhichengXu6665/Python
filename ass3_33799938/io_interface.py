# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm

class Interface:

    # Get user input
    def get_user_input(self, message, num_of_args):
        user_input = input(message).split()

        # Fill with empty strings if the user input less than num_of_args arguments
        user_input += [''] * (num_of_args - len(user_input))

        # Ignore extra arguments if the user input more than num_of_args arguments
        user_input = user_input[:num_of_args]
        if num_of_args == 1:
            return user_input[0]
        else:
            return user_input

    # Print main menu
    def main_menu(self):
        print("1. Login")
        print("2. Register")
        print("3. Quit")

    # Print admin menu
    def admin_menu(self):
        print("1. Show products")
        print("2. Add customers")
        print("3. Show customers")
        print("4. Show orders")
        print("5. Generate test data")
        print("6. Generate all statistical figures")
        print("7. Delete all data")
        print("8. Delete customer using customer id")
        print("9. Delete order using order id")
        print("10. Delete product using product id")
        print("11. Logout")

    # Print customer menu
    def customer_menu(self):
        print("1. Show profile")
        print("2. Update profile")
        print("3. Show products (user input could be “3 keyword” or “3”)")
        print("4. Show history orders")
        print("5. Generate all consumption figures")
        print("6. Get product using product id")
        print("7. Logout")

    # Show list
    def show_list(self, user_role, list_type, object_list):
        if user_role == "admin" or (user_role == "customer" and list_type != "Customer"):
            self.print_message(f"Total pages: {object_list[2]}")
            for idx, obj in enumerate(object_list[0]):
                self.print_message(f"Row {idx + 1}: {obj.__str__()}")
            self.print_message(f"Current page: {object_list[1]}")
        else:
            self.print_message("You don't have access to this type of list.")

    # Print error message
    def print_error_message(self, error_source, error_message):
        print(f"Error in {error_source}: {error_message}")

    # Print message
    def print_message(self, message):
        print(message)

    # Print object
    def print_object(self, target_object):
        from operation_user import UserOperation
        user_operation = UserOperation()
        encrypted_password = target_object.user_password
        decrypted_password = user_operation.decrypt_password(encrypted_password)
        for key, value in target_object.__dict__.items():
            if key == 'user_password':
                print(f"{key}: {decrypted_password}")
            else:
                print(f"{key}: {value}")
