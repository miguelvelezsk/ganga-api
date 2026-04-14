from modules import user_input
from modules.scrapers import mercado_libre_scraper
from modules.scrapers import exito_scraper
from modules import data_processing
from modules import utils
from modules import results
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import asyncio

console = Console()

def main():
    product_name = user_input.get_product_name()
    products_mercado_libre, products_exito = asyncio.run(run_scrapping(product_name))
    top_products = data_processing.process_data(products_mercado_libre, products_exito, product_name)

    console.print("\n")
    console.rule("[bold white]Productos encontrados")
    console.print("\n")
    results.display_results(top_products)

async def run_scrapping(product_name: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """
    Runs the scrapping process for the given product name.

    Args:
        product_name (str): The name of the product to search for.

    Returns:
        tuple[list[dict[str, str]], list[dict[str, str]]]: A tuple containing the products found in Mercado Libre and Exito.
    """
    product_name_mercado_libre = utils.format_product_name(product_name)
    product_name_exito = utils.format_product_name(product_name, "+")

    with Progress(SpinnerColumn(), TextColumn("{task.description}")) as progress:

        task1 = progress.add_task("Buscando en Mercado Libre...", total=None)
        task2 = progress.add_task("Buscando en Exito...", total=None)

        products_mercado_libre, products_exito = await asyncio.gather(
            mercado_libre_scraper.manage_flow(product_name_mercado_libre),
            exito_scraper.manage_flow(product_name_exito)
        )

        progress.update(task1, completed=True)
        progress.update(task2, completed=True)

    return products_mercado_libre, products_exito

main()
