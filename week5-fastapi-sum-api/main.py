from fastapi import FastAPI

app = FastAPI()


@app.get("/add/")
def add_numbers(number1: int, number2: int):
    return number1 + number2