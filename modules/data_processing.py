"""
This module contains the logic for processing the data.
"""

def process_data(
    products_mercado_libre: list[dict[str, str]], 
    products_exito: list[dict[str, str]],
    product_name: str
) -> tuple[list[dict[str, int | str]], list[dict[str, int | str]]]:
    products_mercado_libre_filtered = []
    products_exito_filtered = []
    for product in products_mercado_libre:
        if filter_invalid_products(product):
            process_price(product)
            if filter_by_relevance(product, product_name):
                products_mercado_libre_filtered.append(product)

    for product in products_exito:
        if filter_invalid_products(product):
            process_price(product)
            if filter_by_relevance(product, product_name):
                products_exito_filtered.append(product)

    return products_mercado_libre_filtered, products_exito_filtered
    
def filter_invalid_products(product: dict[str, str]) -> bool:
    if product['title'] == 'NE' or product['link'] == 'NE' or product['price'] == 'NE':
        return False
    return True
    
def process_price(product: dict[str, str]) -> dict[str, int | str]:
    product['price'] = int(product['price'].replace("$", "").replace(".", "").replace(" ", "").strip().split('\n')[0])
    return product

def filter_by_relevance(product: dict[str, str], product_name: str) -> bool:
    product_name_words = product_name.split()
    if all(product_word.lower() in product['title'].lower() for product_word in product_name_words):
        return True
    return False
            