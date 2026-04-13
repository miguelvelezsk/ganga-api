"""
This module contains a function in charge of handling errors.
"""

from rich.console import Console

console = Console()
error_messages = {
    'no_minimum_rating': 'No encontramos productos con calificación mayor a 4 estrellas, te mostramos los mejores disponibles.',
    'no_products_found': 'No encontramos el producto {} en el e-commerce {}, reintentando…',
    'no_valid_product_name': 'No has ingresado un nombre válido, inténtalo de nuevo.',
    'no_network_connection': 'No hay una red disponible, revisa tu conexión a internet.',
    'no_data_found': 'No se encuentra la información deseada, finalizando ejecución',
    'regular_error': 'Ocurrió un error inesperado, finalizando ejecución'
}

def handle_error(error_type: str, product_name: str = "", e_commerce: str = "") -> None:
    """
    Handles errors by printing the appropriate error message.

    Args:
        error_type (str): The type of error to handle.
        product_name (str, optional): The name of the product. Defaults to "".
        e_commerce (str, optional): The name of the e-commerce. Defaults to "".
    """
    if error_type in error_messages:
        console.print(f"Error: {error_messages[error_type].format(product_name, e_commerce)}", style="bold red")
    else:
        console.print(f"Error: {error_messages['regular_error']}", style="bold red")