# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm
import time
import string
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import random
from operation_customer import CustomerOperation
from operation_user import UserOperation


class OrderOperation:

    # Generate order id
    def generate_unique_order_id(self):
        # Check if the order file exists
        if not os.path.exists('data/orders.txt'):
            return 'o_00001'

        # Read all the orders
        with open('data/orders.txt', 'r') as file:
            orders = file.readlines()

        # Generate unique order id
        while True:
            order_id = 'o_' + str(random.randint(10000, 99999))
            if any(order_id in order for order in orders):
                continue
            else:
                return order_id

    # create an order
    def create_an_order(self, customer_id, product_id, product_price, create_time=None):
        order_id = self.generate_unique_order_id()
        create_time = create_time or time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        order_info = {
            'order_id': order_id,
            'customer_id': customer_id,
            'product_id': product_id,
            'product_price': product_price,
            'create_time': create_time
        }

        # Append the order into the file
        with open('data/orders.txt', 'a') as file:
            file.write(str(order_info) + '\n')

        return True

    # delete an order
    def delete_order(self, order_id):
        # Check if the order file exists
        if not os.path.exists('data/orders.txt'):
            return False

        # Read all the orders
        with open('data/orders.txt', 'r') as file:
            orders = file.readlines()

        # Find the order with the given order id and delete it
        for idx, order in enumerate(orders):
            if order_id in order:
                del orders[idx]
                with open('data/orders.txt', 'w') as file:
                    file.writelines(orders)
                return True

        # The order is not found
        return False

    # Get an order list through customer id and page number
    def get_order_list(self, customer_id, page_number):
        # Check if the order file exists
        if not os.path.exists('data/orders.txt'):
            return [], 0, 0

        # Read all the orders
        with open('data/orders.txt', 'r') as file:
            orders = [eval(line.strip()) for line in file.readlines() if
                      eval(line.strip())['customer_id'] == customer_id]

        total_pages = (len(orders) - 1) // 10 + 1
        start_index = (page_number - 1) * 10
        end_index = min(page_number * 10, len(orders))

        page_orders = orders[start_index:end_index]
        return page_orders, page_number, total_pages

    # Generate the order test data
    def generate_test_order_data(self):
        customer_operation = CustomerOperation()
        user_operator = UserOperation()

        customer_ids = []
        for i in range(10):
            while True:
                user_name = ''.join(random.choices(string.ascii_letters + '_', k=6))
                if not user_operator.check_username_exist(user_name):
                    break
            user_password = f"customer1"
            user_email = f"{user_name}@example.com"
            random_num = random.randint(300000000, 499999999)
            user_mobile = "{:010d}".format(random_num)

            if customer_operation.register_customer(user_name, user_password, user_email, user_mobile):
                # Retrieve the customer id from the users.txt file
                with open("./data/users.txt", "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    last_line = lines[-1]
                    customer_id = eval(last_line)['user_id']
                    customer_ids.append(customer_id)

        with open("data/products.txt", "r", encoding="utf-8") as file:
            products = [eval(line.strip()) for line in file.readlines()]

        # Generate the order list
        for customer_id in customer_ids:

            # Random number of orders per customer
            for _ in range(random.randint(50, 200)):
                start_date = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                end_date = datetime.now().replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                delta = end_date - start_date
                random_days = random.randrange(delta.days)
                random_seconds = random.randrange(86400)
                order_time = start_date + timedelta(days=random_days, seconds=random_seconds)

                # Random product id and price
                random_product = random.choice(products)
                product_id = random_product['pro_id']

                # the price is a string in the data
                product_price = float(random_product['pro_current_price'])

                self.create_an_order(str(customer_id), product_id, product_price,
                                     order_time.strftime("%Y-%m-%d %H:%M:%S"))

    # Generate the single customer consumption figure
    def generate_single_customer_consumption_figure(self, customer_id):
        # Check if the order file exists
        if not os.path.exists('data/orders.txt'):
            return

        # Read all the orders
        with open('data/orders.txt', 'r') as file:
            orders = [eval(line.strip()) for line in file.readlines() if
                      eval(line.strip())['customer_id'] == customer_id]

        df = pd.DataFrame(orders)
        df['create_time'] = pd.to_datetime(df['create_time'])
        df['month'] = df['create_time'].dt.month

        monthly_consumption = df.groupby('month')['product_price'].sum()  # Assuming 'order_price' is in the order info

        monthly_consumption.plot(kind='bar')
        plt.title('Monthly Consumption for Customer {}'.format(customer_id))
        plt.xlabel('Month')
        plt.xticks(rotation=0)
        plt.ylabel('Consumption')
        plt.show()

    # Generate all customers consumption
    def generate_all_customers_consumption_figure(self):
        # Check if the order file exists
        if not os.path.exists('data/orders.txt'):
            return

        # Read all the orders
        with open('data/orders.txt', 'r') as file:
            orders = [eval(line.strip()) for line in file.readlines()]

        df = pd.DataFrame(orders)
        df['create_time'] = pd.to_datetime(df['create_time'])
        df['month'] = df['create_time'].dt.month

        monthly_consumption = df.groupby('month')['product_price'].sum()  # Assuming 'order_price' is in the order info

        monthly_consumption.plot(kind='bar')
        plt.title('Monthly Consumption for All Customers')
        plt.xlabel('Month')
        plt.xticks(rotation=0)
        plt.ylabel('Consumption')
        plt.savefig('data/figure/all_customers_consumption_figure.png')
        plt.close()

    # Generate all top 10 best sellers figure
    def generate_all_top_10_best_sellers_figure(self):
        # Check if the order file exists
        if not os.path.exists('data/orders.txt'):
            return

        # Read all the orders
        with open('data/orders.txt', 'r') as file:
            orders = [eval(line.strip()) for line in file.readlines()]

        df = pd.DataFrame(orders)

        best_sellers = df['product_id'].value_counts().nlargest(10)  # Assuming 'product_id' is in the order info

        best_sellers.sort_values(ascending=False).plot(kind='bar')
        plt.title('Top 10 Best-selling Products')
        plt.xlabel('Product')
        plt.ylabel('Number of Orders')
        plt.savefig('data/figure/top_10_best_sellers_figure.png')
        plt.close()

    # Delete all orders
    def delete_all_orders(self):
        # Check if the order file exists
        if not os.path.exists('data/orders.txt'):
            return

        # Empty the file
        with open('data/orders.txt', 'w') as file:
            pass
