# Ganga API | Scraper & Orchestrator

> **A high-performance FastAPI server designed to power the Ganga price comparison ecosystem using automated browser logic and statistical data cleaning.**

---

## Overview

Ganga API is the core engine of a Systems Engineering solution designed to automate product discovery across Colombia's leading e-commerce platforms: Mercado Libre and Éxito.

While it maintains a robust CLI mode for local testing, its primary function is to serve as a REST API. It leverages Playwright for asynchronous scraping and NumPy to ensure that users receive high-quality data, filtered from "noise" (like accessories or anomalous prices).

## Project Documentation

This project was developed following formal software engineering methodologies. You can review the detailed planning and design documents here:

* [Product Requirements Document (PRD)](./docs/PRD.md): Detailed problem statement, user requirements, and project scope.
* [Technical Design Document (TDD)](./docs/TDD.md): Technical architecture, data flow, and system specifications.

### Key Goals
* **Concurrency:** Runs multiple scrapers simultaneously using `asyncio` to minimize wait time.
* **Statistical Filtering:** Uses Interquartile Range (IQR) and Median filtering to remove irrelevant results or price anomalies.
* **Professional UX:** Renders high-quality visual components (Panels) in the terminal using the **Rich** library.

---

## The Ecosystem

This repository is the backend for the [Ganga Web Client](https://github.com/miguelvelezsk/ganga-web). Together, they form a full-stack architecture for intelligent shopping.

## Tech Stack

The project follows a modular design to handle asynchronous operations and heavy data analysis.

### Core Technologies
* **Python 3.10+**: The primary programming language, chosen for its robust support for asynchronous programming.
* **FastAPI**: High-performance web framework for the REST API layer.
* **Uvicorn** 0.45.0: An ASGI web server implementation for Python, used for serving the FastAPI application.
* **Playwright** 1.58.0: Selected for web automation and robust data extraction from dynamic content.
* **Numpy 2.4.4**: Implemented to perform statistical analysis and outlier removal on retrieved prices.

### Architectural Principles
* **Asynchronous Concurrency**: Uses `asyncio` to execute multiple scraping tasks in parallel.
* **Modular Design**: Structured into independent modules (scrapers, processing, error_handler) to adhere to the Single Responsibility Principle.
* **Documentation Standards**: Follows PEP 8 and PEP 257 (docstrings) for high maintainability.

---

## Tech Stack & Engineering


The system follows a strict pipeline to guarantee Data Quality:

1. **Parallel Execution**: Simultaneous browser instances are launched via Playwright.

2. **Statistical Filtering (NumPy)**: * IQR (Interquartile Range): Identifies and eliminates extreme price anomalies.

   * **Median Filter**: Removes "noise" (e.g., a case sold in a phone search) by filtering items priced significantly below the median.

4. **Ranking**: Products are weighted by price and rating, delivering the top 3 "Gangas" per platform.

## Infrastructure & Deployment
### Important Note on Performance

Due to the computational overhead of Playwright (which orchestrates full Chromium instances), this API is optimized for:

* Local Execution: Running alongside the frontend for development.

* Dedicated VPS: Requires at least 2GB RAM and dedicated CPU cycles to manage browser rendering effectively.

---

## Error Handling Strategy

The application implements a centralized error management system through the `error_handler` module to ensure consistent visual feedback.

* **Resilience**: Automatic retries (up to 3) for network or DOM loading issues.
* **Network Validation**: Detects connectivity at launch and terminates gracefully if unavailable.
* **Data Fallbacks**: If no products meet the 4-star requirement, the system informs the user and displays the highest-rated alternatives available.
* **Missing Attributes**: Handles missing ratings or titles by assigning 'NE' (No Existe) values to maintain data structure integrity.

---

## 🚀 Quick Start (Local)

1. Clone and install:
   ```
   git clone https://github.com/miguelvelezsk/ganga-api
   pip install -r requirements.txt
   playwright install chromium
   ```
2. Run the API:
   ```
   uvicorn main:app --reload
   ```
---

## Author

**Miguelangel Velez Aguirre**
* Systems Engineering Student at Universidad de Antioquia (UdeA)
* [LinkedIn Profile](https://www.linkedin.com/in/miguelangel-v%C3%A9lez-aguirre-235982168/) | [GitHub Portfolio](https://github.com/miguelvelezsk?tab=repositories)
