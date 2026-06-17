import requests

# TODO: integrate WhatsApp Business API


def send_whatsapp(
        phone,
        message):

    payload = {

        "phone": phone,

        "message": message

    }

    return payload
