"""
This module contains the logic for scraping Mercado Libre.
"""

from playwright.async_api import async_playwright, ElementHandle, Page
from modules import error_handler

URL = "https://listado.mercadolibre.com.co/"

async def manage_flow(product_name: str) -> list[str]:
    """
    Manages the flow of the Mercado Libre scraper.

    Args:
        product_name (str): The name of the product to search for.

    Returns:
        list[str]: A list of products found.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        await search_product(page, product_name)
        products = await extract_products(page)
        await page.close()
        await browser.close()
        await playwright.stop()
        return products

async def search_product(page: Page, product_name: str) -> None:
    """
    Searches for the product on Mercado Libre.

    Args:
        page (Page): The page to search on.
        product_name (str): The name of the product to search for.
    """
    await page.goto(f'{URL}{product_name}')
    await page.wait_for_selector('.ui-search-layout')
    await page.screenshot(path="./screenshots/product_mercado_libre.jpg")
    
async def extract_products(page: Page) -> list[dict[str, str]]:
    """
    Extracts products attributes from the page.

    Args:
        page (Page): The page to extract products from.

    Returns:
        list[str]: A list of products found.
    """
    products = await page.query_selector_all('.poly-card')
    product_list = []
    for product in products:
        product_dict = {}
        product_dict['title'] = await safe_extract('.poly-component__title', product, 'inner_text')
        product_dict['price'] = await safe_extract('.poly-component__price', product, 'inner_text')
        product_dict['link'] = await safe_extract('.poly-component__title', product, 'get_attribute')
        product_dict['rating'] = await safe_extract('.poly-phrase-label', product, 'inner_text')
        product_dict['shipping'] = await safe_extract('.poly-component__shipping-v2', product, 'inner_text')
        product_list.append(product_dict)
    return product_list

async def safe_extract(selector: str, product: ElementHandle, method: str) -> str:
    """
    Safely extracts attributes from a product, if the attribute is not found, it returns "NE" (No exists).

    Args:
        selector (str): The selector to use.
        product (ElementHandle): The product to extract attributes from.
        method (str): The method to use.

    Returns:
        str: The extracted attribute.
    """
    element = await product.query_selector(selector)
    if element:
        if method == 'inner_text':
            return await element.inner_text()
        elif method == 'get_attribute':
            return await element.get_attribute('href')
    return "NE"
    
    
    