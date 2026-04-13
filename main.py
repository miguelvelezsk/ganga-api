from modules import user_input
from modules.scrapers import mercado_libre_scraper
from modules import utils
import asyncio

product_name = user_input.get_product_name()
product_name = utils.format_product_name(product_name)

products = asyncio.run(mercado_libre_scraper.manage_flow(product_name))
print(products)
