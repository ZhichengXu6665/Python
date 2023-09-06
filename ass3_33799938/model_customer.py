# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm
from model_user import User


class Customer(User):

    # Initialization data
    def __init__(self, user_id='u_0000000000', user_name='', user_password='', user_register_time='00-00-0000_00:00:00',
                 user_role='customer', user_email='', user_mobile='0123456789'):
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)
        self.user_email = user_email
        self.user_mobile = user_mobile

    # Return Initialization data
    def __str__(self):
        return (super().__str__()[:-1] + f", 'user_email':'{self.user_email}','user_mobile':'{self.user_mobile}'}}")
