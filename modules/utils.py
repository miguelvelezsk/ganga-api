"""
This module contains utility functions.
"""

def format_product_name(product_name: str) -> str:
    """
    Formats the product name for the URL.

    Args:
        product_name (str): The name of the product.

    Returns:
        str: The formatted product name.
    """
    return product_name.replace(" ", "-")