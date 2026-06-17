import requests


def stk_push(
        phone,
        amount):

    payload = {

        "phone": phone,

        "amount": amount

    }

    # Daraja API logic

    return payload

# additionsLater you'll add:

# OAuth Token
# STK Push
# Paybill
# C2B
# B2C
# Reversals
# Transaction Status
