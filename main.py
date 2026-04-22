from fastapi import FastAPI
from orchestrator import orchestrator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/search")
async def search_product(product_name: str):
    top_products = await orchestrator(product_name)
    return top_products
