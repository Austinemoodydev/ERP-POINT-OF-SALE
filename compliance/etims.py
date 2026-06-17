import requests


def submit_invoice(invoice):

    payload = {
        "invoice_number": invoice.invoice_number,
        "amount": str(invoice.total_amount)
    }

    # actual KRA API integration later

    response = requests.post(
        "ETIMS_API_URL",
        json=payload
    )

    return response.json()
