# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm
class Order:

    # Initialization data
    def __init__(self, order_id='o_00000', user_id='', pro_id='', order_time='00-00-0000_00:00:00'):
        self.order_id = order_id
        self.user_id = user_id
        self.pro_id = pro_id
        self.order_time = order_time

    # Return Initialization data
    def __str__(self):
        return f"{{'order_id':'{self.order_id}', 'user_id':'{self.user_id}', 'pro_id':'{self.pro_id}', 'order_time':'{self.order_time}'}}"
