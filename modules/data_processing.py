"""
This module contains the logic for processing the data.
"""
import numpy as np

def process_data(
    products_mercado_libre: list[dict[str, str]], 
    products_exito: list[dict[str, str]],
    product_name: str
) -> list[dict[str, int | str]]:
    products_mercado_libre_filtered = []
    products_exito_filtered = []
    for product in products_mercado_libre:
        if filter_invalid_products(product):
            process_price(product)
            process_title(product)
            process_shipping(product)
            if filter_by_relevance(product, product_name):
                products_mercado_libre_filtered.append(product)

    for product in products_exito:
        if filter_invalid_products(product):
            process_price(product)
            process_title(product)
            process_shipping(product)
            if filter_by_relevance(product, product_name):
                products_exito_filtered.append(product)

    products_joined = join_products(products_mercado_libre_filtered, products_exito_filtered)
    products_joined = filter_by_interquartile_range(products_joined)
    products_joined = filter_by_median(products_joined)
    products_sorted = sort_products(products_joined)
    top_products = get_top_products(products_sorted)

    return top_products
    
def filter_invalid_products(product: dict[str, str]) -> bool:
    """
    Filters out products that are not valid (title, link or price is 'NE').

    Args:
        product: A product.
    
    Returns:
        True if the product is valid, False otherwise.
    """
    if product['title'] == 'NE' or product['link'] == 'NE' or product['price'] == 'NE':
        return False
    return True

def process_title(product: dict[str, str]) -> None:
    """
    Processes the title of the product removing the extra spaces and the \xa0 character.

    Args:
        product: A product.
    
    Returns:
        None
    """
    product['title'] = product['title'].strip().replace("\xa0", " ")
    
def process_price(product: dict[str, str]) -> None:
    """
    Processes the price of the product discarting the currency symbol, the dots and the spaces.

    Args:
        product: A product.
    
    Returns:
        None
    """
    product['price'] = int(product['price'].replace("$", "").replace(".", "").replace(" ", "").strip().split('\n')[0])

def process_shipping(product: dict[str, str]) -> None:
    """
    Processes the shipping of the product.

    Args:
        product: A product.
    
    Returns:
        None
    """
    product['shipping'] = product['shipping'].strip().replace("\xa0", " ").split("\n")[0]

def filter_by_relevance(product: dict[str, str], product_name: str) -> bool:
    """
    Filters out products that are not relevant to the product name.

    Args:
        product: A product.
        product_name: The name of the product.
    
    Returns:
        True if the product is relevant to the product name, False otherwise.
    """
    product_name_words = product_name.split()
    if all(product_word.lower() in product['title'].lower() for product_word in product_name_words):
        return True
    return False

def calculate_interquartile_range(products: list[dict[str, int | str]]) -> tuple[int, int]:
    """
    Calculates the Interquartile Range (IQR) for the products list.

    Args:
        products: A list of products.
    
    Returns:
        A tuple containing the lower and upper bounds of the IQR.
    """
    prices = [product['price'] for product in products]
    q1 = np.percentile(prices, 25)
    q3 = np.percentile(prices, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return lower_bound, upper_bound

def filter_by_interquartile_range (products: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
    """
    Filters out outliers from the products list based on the Interquartile Range (IQR).

    Args:
        products: A list of products.
    
    Returns:
        A list of products with outliers removed.
    """
    if len(products) == 0:
        return []
    lower_bound, upper_bound = calculate_interquartile_range(products)
    return [product for product in products if product['price'] >= lower_bound and product['price'] <= upper_bound]
    
def join_products(products_mercado_libre: list[dict[str, int | str]], products_exito: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
    """
    Joins the products from Mercado Libre and Exito.

    Args:
        products_mercado_libre: A list of products from Mercado Libre.
        products_exito: A list of products from Exito.
    
    Returns:
        A list of products from both Mercado Libre and Exito.
    """
    for product in products_mercado_libre:
        product['source'] = 'Mercado Libre'
    for product in products_exito:
        product['source'] = 'Exito'
    return products_mercado_libre + products_exito

def filter_by_median(products: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
    """
    Filters out outliers from the products list based on the median.

    Args:
        products: A list of products.
    
    Returns:
        A list of products with outliers removed.
    """
    if len(products) == 0:
        return []
    median = np.median([product['price'] for product in products])
    return [product for product in products if product['price'] >= median * 0.8]
            
def sort_products(products: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
    """
    Sorts the products by price in ascending order and rating value in descending order.

    Args:
        products: A list of products.
    
    Returns:
        A list of products sorted by price.
    """
    return sorted(products, key=lambda x: (x['price'], -(float(x['rating']) if x['rating'] != 'NE' else 0)))
    
def get_top_products(products: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
    """
    Gets the top (MAX 6) products from the products list.

    Args:
        products: A list of products.
    
    Returns:
        A list of the top 3 products.
    """
    products_mercado_libre = [product for product in products if product['source'] == 'Mercado Libre'][:3]
    products_exito = [product for product in products if product['source'] == 'Exito'][:3]
    return products_mercado_libre + products_exito
