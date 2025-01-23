import json
from collections import defaultdict
from cart import dao
from products import Product, get_product

class Cart:
    def _init_(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])

def get_cart(username: str) -> list[Product]:
    # Retrieve cart details from the database
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Parse and aggregate all product IDs
    product_counts = defaultdict(int)
    for cart_detail in cart_details:
        for item in json.loads(cart_detail['contents']):
            product_counts[item] += 1

    # Fetch product details for unique product IDs in bulk
    unique_products = list(product_counts.keys())
    products_data = {prod_id: get_product(prod_id) for prod_id in unique_products}

    # Rebuild the full list of products in the order they appear in the cart
    result = []
    for prod_id in unique_products:
        result.extend([products_data[prod_id]] * product_counts[prod_id])

    return result

def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)