from .forecasting import monthly_sales_forecast
from .services import gross_profit


def ai_assistant(question):
    question = question.lower()

    if "sales" in question:
        return f"Sales forecast is {monthly_sales_forecast()}"

    if "profit" in question:
        return f"Current gross profit is {gross_profit()}"

    return "I do not understand the question."
