# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm
class User:

    # Initialization data
    def __init__(self, user_id='u_0000000000', user_name='', user_password='', user_register_time='00-00-0000_00:00:00',
                 user_role='customer'):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password
        self.user_register_time = user_register_time
        self.user_role = user_role

    # Return Initialization data
    def __str__(self):
        return f"{{'user_id':'{self.user_id}', 'user_name':'{self.user_name}', 'user_password':'{self.user_password}', 'user_register_time':'{self.user_register_time}', 'user_role':'{self.user_role}'}}"
