import requests


def sync_products(
        integration):

    response = requests.get(

        f"{integration.base_url}/products",

        headers={

            "Authorization":
            integration.api_key

        }

    )

    return response.json()
