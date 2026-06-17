from .forecasting import monthly_sales_forecast
from .services import gross_profit
from .reports import branch_performance
from .services import reorder_recommendations  # adjust module name if different


def executive_dashboard():

    return {

        "forecast":
        monthly_sales_forecast(),

        "profit":
        gross_profit(),

        "branches":
        branch_performance(),

        "reorders":
        reorder_recommendations()

    }
