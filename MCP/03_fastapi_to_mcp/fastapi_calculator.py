from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI(title="Calculator API")

@app.post("/add")
def add_numbers(a: float, b: float) -> dict:
    """Returns the sum of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.
    """
    return { "result": a + b }

@app.post("/subtract")
def subtract_numbers(a: float, b: float) -> dict:
    """Returns the difference of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The difference of the two numbers.
    """
    return { "result": a - b }

@app.post("/multiply")
def multiply_numbers(a: float, b: float) -> dict:
    """Returns the product of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of the two numbers.
    """
    return { "result": a * b }

@app.post("/divide")
def divide_numbers(a: float, b: float) -> dict:
    """Returns the quotient of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The quotient of the two numbers.
    """
    if b == 0:
        return { "error": "Cannot divide by zero." }  
    return { "result": a / b }

mcp = FastApiMCP(app, name="Calculator API MCP")
mcp.mount_http()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
