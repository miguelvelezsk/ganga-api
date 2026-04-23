# Technical Design Document (TDD)

## Overview

A full-stack application consisting of a FastAPI backend that manages asynchronous Playwright scrapers and a Vite frontend for user interaction. The system emphasizes data integrity through statistical analysis using Numpy.

## Architecture

### Frontend (Vite)

- **Role:** User interface and request management.
- **Communication:** Consumes the Backend REST API via asynchronous fetch calls.
- **State Management:** Handles loading states during the scraping process (avg. 15-20s).

### Backend (FastAPI + Uvicorn)

- **Role:** Orchestration, data extraction, and processing.
- **API Layer:** Replaces the previous CLI. Uses Pydantic for data validation and CORS middleware for frontend communication.
- **Scraping Engine:** Parallel execution of Playwright instances for Mercado Libre and Éxito.

### Utils

This module contains helper functions and shared constants.

### Error handler

A centralized module that manages user-facing exceptions and system alerts. It uses the Rich library to standardize the visual style of errors in the CLI and supports dynamic string formatting for contextual feedback.

### Data Processing Module (Numpy)

- **Normalization:** Currency string to integer conversion and text sanitization.
- **Outlier Detection:** * **IQR Filter:** Removes products with anomalous prices.
    - **Median Logic:** Discards auxiliary items (accessories) priced 20% below the median of the search results.

## Deployment Note

Due to the high CPU and RAM overhead of headless browsers (Playwright), the backend is currently optimized for local execution or dedicated virtual private servers (VPS). Deployment on serverless or shared free-tier platforms is restricted by hardware limitations.

## Tech Stack

- Python 3.10
- Playwright 1.58.0
- Numpy 2.4.4
- Fastapi 0.136,0
- Uvicorn 0.45.0

## Data Flow

1. **Request:** User enters a product in the Vite web app.
2. **API Call:** Frontend sends a request to `GET /search?product_name={product}`.
3. **Execution:** FastAPI runs scrapers in parallel using `asyncio.gather`.
4. **Statistical Cleaning:** Numpy filters the raw data to ensure only relevant products remain.
5. **Response:** Backend returns a JSON object.
6. **Display:** Frontend renders product cards with the top 3 results per platform.

## Error Handling Strategy

- If no product meets the minimum rating threshold, the system displays a message *“No sé encontraron productos con calificación mayor a 4 estrellas, te mostramos los mejores disponibles.”* and shows the best available products.
- If no product is found on the e-commerce, the system displays a message *“No se encontró el producto {nombre de producto} en el e-commerce {nombre de e-commerce, reintentando (1 de 3)…}”*, retries up to 3 times and continues with the next e-commerce or sends the available data to the preprocessing and cleaning module.
- If the user enters an empty value or an invalid name with non alphabetic characters, the system displays a message “*No se ingresó un nombre válido, inténtalo de nuevo.*” and allows the user to try again.
- If the user doesn’t have network, the system displays a message “*No hay una red disponible, revisa tu conexión a internet”*  and terminates the execution.
- If the product doesn’t have a rating value, the system assigns a value of “NE” (No exists).
- If occurs a unexpected error, the system displays a message *“Ocurrió un error inesperado, finalizando ejecución”* and terminates the execution.

## Folder Structure

- /scraping_price_comparison
    - backend/
        - orchestrator.py
        - main.py
        - requirements.txt
        - README.md
        - modules/
            - __init__.py
            - data_processing.py
            - helpers.py
            - error_handler.py
            - scrapers/
                - __init__.py
                - mercado_libre_scraper.py
                - exito_scraper.py
            - tests/
                - test_scrapers.py