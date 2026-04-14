"""
This module contains a function in charge of handling errors.
"""

from rich.console import Console

console = Console()
error_messages = {
    'no_minimum_rating': 'No se encontraron productos con calificación mayor a 4 estrellas, te mostramos los mejores disponibles.',
    'no_products_found': 'No se encontró el producto {} en el e-commerce {}, reintentando ({}/3)...',
    'no_products_found_after_attempts': 'No se encontró el producto {} en el e-commerce {}, saltando paso',
    'no_valid_product_name': 'No se ingresó un nombre válido, inténtalo de nuevo.',
    'no_network_connection': 'No hay conexión a la red, revisa tu conexión a internet.',
    'no_data_found': 'No se encontró la información deseada, finalizando ejecución',
    'unexpected_error': 'Ocurrió un error inesperado, finalizando ejecución'
}

def handle_error(error_type: str, product_name: str = "", e_commerce: str = "", counter: int = 0) -> None:
    """
    Handles errors by printing the appropriate error message.

    Args:
        error_type (str): The type of error to handle.
        product_name (str, optional): The name of the product. Defaults to "".
        e_commerce (str, optional): The name of the e-commerce. Defaults to "".
        counter (int, optional): The counter of the attempts. Defaults to 0.
    """
    if error_type in error_messages:
        console.print(f"Error: {error_messages[error_type].format(product_name, e_commerce, counter)}", style="bold red")
    else:
        console.print(f"Error: {error_messages['regular_error']}", style="bold red")