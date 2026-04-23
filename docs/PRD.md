# Product Requirements Document (PRD)

## Problem Statement

Online shopping is increasingly common. In Colombia, in 2025 more than 19 million people bought products online. 

Mercado Libre is the leading company in Colombia, as it offers a good web application, and a good reputation, but sometimes, sellers on Mercado Libre take advantage of price volatility, making options like Exito very useful. 

In the Colombian market, comparing prices between major retailers like Mercado Libre and Éxito is a manual and inefficient process. Users often encounter "noise" in search results (accessories, related items) that skew price comparisons. This project provides a full-stack solution to automate retrieval, perform statistical cleaning, and present results through a modern web interface.

## Target User

- **General Consumers:** Shoppers in Colombia looking for the best deal without manually browsing multiple sites.
- **Developers:** Users interested in consuming the price comparison logic via the REST API.

## Requirements

### Functional requirements

- **FR1 (Web Interface):** A responsive frontend built with Vite to allow users to input search queries.
- **FR2 (API Search Endpoint):** A GET `/search` endpoint that orchestrates the scraping process.
- **FR3 (Statistical Filtering):** Integration of Numpy to apply IQR (Interquartile Range) and Median filters to eliminate irrelevant products (e.g., cases/cables when searching for smartphones).
- **FR4 (Standardized Output):** Data returned in JSON format including price, rating, shipping, and source.

### Non-functional requirements

- **Performance:** End-to-end execution (Scraping to UI) in under 20 seconds using asynchronous operations.
- **Scalability:** Decoupled Frontend-Backend architecture to allow independent updates.
- **UX/UI:** Clean, intuitive interface inspired by the original CLI "card" design.

## Out of Scope

- This version will not be available for other countries, only Colombia.
- This version will not support other languages, only Spanish.
- This version will not save comparisons.