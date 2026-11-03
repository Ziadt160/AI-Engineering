#libraries
from fastmcp import FastMCP

mcp = FastMCP(name="calculator_mcp")


@mcp.tool(name="add_numbers", description="Adds two numbers together.")
def add_numbers(a: float, b: float) -> float:
    """Returns the sum of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.
    """
    return a + b


@mcp.tool(name="subtract_numbers", description="Subtracts the second number from the first.")
def subtract_numbers(a: float, b: float) -> float:
    """Returns the difference of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The difference of the two numbers.
    """
    return a - b

@mcp.tool(name="multiply_numbers", description="Multiplies two numbers together.")
def multiply_numbers(a: float, b: float) -> float:
    """Returns the product of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of the two numbers.
    """
    return a * b

@mcp.tool(name="divide_numbers", description="Divides the first number by the second.")
def divide_numbers(a: float, b: float) -> float:
    """Returns the quotient of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The quotient of the two numbers.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

if __name__ == "__main__":
    mcp.run() # STDIO