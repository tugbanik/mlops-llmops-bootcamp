from fastapi import FastAPI
from database import create_db_and_tables

from routers import advertising, iris, product_review_llm

app = FastAPI(title="Week-7 FastAPI ML/LLM with DB")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(advertising.router, prefix="/advertising", tags=["Advertising"])
app.include_router(iris.router, prefix="/iris", tags=["Iris"])
app.include_router(product_review_llm.router, prefix="/product-review", tags=["ProductReview"])