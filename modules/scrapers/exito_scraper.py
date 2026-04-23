"""
This module contains the logic for scraping Exito.
"""

from playwright.async_api import async_playwright, ElementHandle, Page
from modules import error_handler
from fastapi import HTTPException

URL = "https://www.exito.com/s?q="

async def manage_flow(product_name: str) -> list[dict[str, str]]:
    """
    Manages the flow of the Exito scraper.

    Args:
        product_name (str): The name of the product to search for.

    Returns:
        list[dict[str, str]]: A list of products found.
    """
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--disable-extensions"]
            )
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            page = await context.new_page()
            is_found = await search_product(page, product_name)
            if is_found:
                products = await extract_products(page)
            else:
                products = []
        return products
    except HTTPException as e:
        raise e
    except Exception as e:
        error_handler.handle_error('no_network_connection', product_name, "Exito")

async def search_product(page: Page, product_name: str) -> bool:
    """
    Searches for the product on Exito.

    Args:
        page (Page): The page to search on.
        product_name (str): The name of the product to search for.
    """
    count_of_attempts = 1
    while count_of_attempts <= 3:
        try:
            await page.goto(f'{URL}{product_name}')
            await page.wait_for_selector('.product-grid_fs-product-grid___qKN2', timeout=10000)
            return True
        except HTTPException as e:
            raise e
        except Exception as e:
            if count_of_attempts <= 2:
                error_handler.print_message('no_products_found', product_name, 'Exito', count_of_attempts)
                count_of_attempts += 1
            else:
                error_handler.print_message('no_products_found_after_attempts', product_name, 'Exito', count_of_attempts)
                return False

async def extract_products(page: Page) -> list[dict[str, str]]:
    """
    Extracts products attributes from the page.

    Args:
        page (Page): The page to extract products from.

    Returns:
        list[dict[str, str]]: A list of products found.
    """
    try:
        products = await page.query_selector_all('.productCard_contentInfo__CBBA7')
        product_list = []
        for product in products:
            product_dict = {}
            product_dict['title'] = await safe_extract('.styles_name__qQJiK', product, 'inner_text')
            product_dict['price'] = await safe_extract('.ProductPrice_container__price__XmMWA', product, 'inner_text')
            product_relative_link = await safe_extract('.productCard_productLinkInfo__It3J2', product, 'get_attribute')
            product_dict['link'] = "https://www.exito.com" + product_relative_link
            product_dict['rating'] = "NE"
            product_dict['shipping'] = "NE"
            product_list.append(product_dict)
        return product_list
    except HTTPException as e:
        raise e
    except Exception as e:
        error_handler.handle_error('unexpected_error', e_commerce="Exito")

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
    try:
        element = await product.query_selector(selector)
        if element:
            if method == 'inner_text':
                return await element.inner_text()
            elif method == 'get_attribute':
                return await element.get_attribute('href')
        return "NE"
    except HTTPException as e:
        raise e
    except Exception as e:
        error_handler.handle_error('unexpected_error', e_commerce="Exito")
    
    
    