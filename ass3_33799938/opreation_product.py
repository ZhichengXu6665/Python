# Class number : FIT9136 App02_FuCai Ke
# Group member :ZhiCheng Xu
# Student ID:33799938
# Last modify : 08/06/2024 2:30pm
import pandas as pd
import os
from model_product import Product
import matplotlib.pyplot as plt


class ProductOperation:

    # extract product from product file
    def extract_products_from_files(self):
        product_list = []
        for file_name in os.listdir('data/product/'):
            # only process .csv files
            if file_name.endswith('.csv'):
                file_path = os.path.join('data/product/', file_name)
                df = pd.read_csv(file_path)
                df.columns = df.columns.str.strip()
                for idx, row in df.iterrows():
                    product = Product(
                        row['id'],
                        row['model'],
                        row['category'],
                        row['name'],
                        row['current_price'],
                        row['raw_price'],
                        row['discount'],
                        row['likes_count']
                    )
                    product_list.append(product)

        # Write to products.txt
        with open('data/products.txt', 'w') as file:
            for product in product_list:
                file.write(product.__str__() + '\n')

    # get the product list
    def get_product_list(self, page_number):
        with open("data/products.txt", "r", encoding="utf-8") as file:
            products = [line.strip() for line in file.readlines()]

        product_list = []
        for product in products:
            try:
                product = eval(product)
                product_list.append(Product(
                    product['pro_id'],
                    product['pro_model'],
                    product['pro_category'],
                    product['pro_name'],
                    product['pro_current_price'],
                    product['pro_raw_price'],
                    product['pro_discount'],
                    product['pro_likes_count']
                ))
            except SyntaxError:
                product = product.strip("{''}").split("', '")
                product = [item.split("': '")[1] for item in product]
                product_list.append(Product(
                    product[0],
                    product[1],
                    product[2],
                    product[3],
                    product[4],
                    product[5],
                    product[6],
                    product[7]
                ))

        # Calculate the total number of pages
        total_pages = (len(product_list) - 1) // 10 + 1

        # Start index of products for the page
        start_index = (page_number - 1) * 10

        # End index of products for the page
        end_index = min(page_number * 10, len(product_list))

        # Get the products for the page
        page_products = product_list[start_index:end_index]

        return page_products, page_number, total_pages

    # Delete an product
    def delete_product(self, product_id):
        with open("data/products.txt", "r", encoding="utf-8") as file:
            products = [eval(line.strip()) for line in file.readlines()]

        for idx, product in enumerate(products):
            if product['pro_id'] == product_id:
                break
        else:
            return False

        products.pop(idx)

        with open("data/products.txt", "w", encoding="utf-8") as file:
            for product in products:
                file.write(str(product) + '\n')

        return True

    # Get the product list through keyword
    def get_product_list_by_keyword(self, keyword):
        with open("data/products.txt", "r", encoding="utf-8") as file:
            products = [line.strip() for line in file.readlines()]

        keyword = keyword.lower()
        target_list = []

        for product in products:
            try:
                product = eval(product)
                if keyword in product['pro_category'].lower():
                    target_list.append(Product(
                        product['pro_id'],
                        product['pro_model'],
                        product['pro_category'],
                        product['pro_name'],
                        product['pro_current_price'],
                        product['pro_raw_price'],
                        product['pro_discount'],
                        product['pro_likes_count']
                    ))
            except SyntaxError:
                product = product.strip("{''}").split("', '")
                product = [item.split("': '")[1] for item in product]
                if keyword in product[3].lower():  # Assuming product[3] is the product name
                    target_list.append(Product(
                        product[0],
                        product[1],
                        product[2],
                        product[3],
                        product[4],
                        product[5],
                        product[6],
                        product[7]
                    ))

        pages = len(target_list) // 10 + (len(target_list) % 10 > 0)  # Calculate total pages
        current_page = 1

        return [target_list, current_page, pages]

    # get product by using product id
    def get_product_by_id(self, product_id):
        with open("data/products.txt", "r", encoding="utf-8") as file:
            products = [eval(line.strip()) for line in file.readlines()]

        target_product = None

        for product in products:
            if product['pro_id'] == product_id:
                target_product = Product(
                    product['pro_id'],
                    product['pro_model'],
                    product['pro_category'],
                    product['pro_name'],
                    product['pro_current_price'],
                    product['pro_raw_price'],
                    product['pro_discount'],
                    product['pro_likes_count']
                )
                break

        return target_product

    # Generate the category figure
    def generate_category_figure(self):
        with open("data/products.txt", "r", encoding="utf-8") as file:
            products = [eval(line.strip()) for line in file.readlines()]

        df = pd.DataFrame(products)
        category_counts = df['pro_category'].value_counts()

        category_counts.sort_values(ascending=False).plot(kind='bar')
        plt.title('The Number Of Products For Every Category')
        plt.xlabel('Category')
        plt.ylabel('Product Quantity')
        plt.xticks(rotation=0)  # set the rotation to 0
        plt.savefig('data/figure/category_figure.png')
        plt.close()

    # Generate the discount figure
    def generate_discount_figure(self):
        with open("data/products.txt", "r", encoding="utf-8") as file:
            products = [eval(line.strip()) for line in file.readlines()]

        df = pd.DataFrame(products)
        df['pro_discount'] = df['pro_discount'].astype(float)
        df['discount_group'] = pd.cut(df['pro_discount'], bins=[0, 30, 60, float('inf')],
                                      labels=['<30', '30-60', '>60'])

        discount_group_counts = df['discount_group'].value_counts()

        discount_group_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Distribution of Products by Discount Value')
        plt.savefig('data/figure/discount_figure.png')
        plt.close()

    # Generate the like count figure
    def generate_likes_count_figure(self):
        with open("data/products.txt", "r", encoding="utf-8") as file:
            products = [eval(line.strip()) for line in file.readlines()]

        df = pd.DataFrame(products)

        # Ensure pro_likes_count is float
        df['pro_likes_count'] = df['pro_likes_count'].astype(float)

        category_likes = df.groupby('pro_category')['pro_likes_count'].sum()

        # Plotting
        category_likes.sort_values(ascending=True).plot(kind='barh', color='skyblue')  # Horizontal bar plot
        plt.title('Total Likes per Category')
        plt.xlabel('Total Likes')
        plt.ylabel('Category')

        # This line ensures that the labels are not cut off when saving the image
        plt.tight_layout()

        # Save the plot
        plt.savefig('data/figure/likes_count_figure.png')

        plt.close()

    # Generate the discount likes count figure
    def generate_discount_likes_count_figure(self):
        with open("data/products.txt", "r", encoding="utf-8") as file:
            products = [eval(line.strip()) for line in file.readlines()]

        df = pd.DataFrame(products)

        plt.scatter(df['pro_likes_count'], df['pro_discount'])
        plt.title('Likes Count vs. Discount')
        plt.xlabel('Likes Count')
        plt.ylabel('Discount')
        plt.savefig('data/figure/discount_likes_count_figure.png')
        plt.close()

    # Delete all of products
    def delete_all_products(self):
        with open("data/products.txt", "w") as file:
            pass
