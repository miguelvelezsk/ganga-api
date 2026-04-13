"""
This module contains a function in charge of requesting the product name from the user.
"""

from rich.prompt import Prompt
from rich.console import Console
from modules import error_handler

console = Console()

def get_product_name() -> str:

    """
    Asks the user for the product name and validates it.

    Returns:
        str: The product name entered by the user.
    """
    console.rule("[bold red]Inicio de Aplicación")

    while True:

        product_name = Prompt.ask('\nIngrese el nombre de producto a buscar')

        if product_name != "" and all(word.isalnum() for word in product_name.split()):
            return product_name

        error_handler.handle_error('no_valid_product_name')

    
