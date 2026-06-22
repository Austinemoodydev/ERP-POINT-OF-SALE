import qrcode


from io import BytesIO


from django.core.files.base import ContentFile


def generate_qr(product):

    qr = qrcode.make(


        product.barcode

    )

    buffer = BytesIO()

    qr.save(buffer)

    return ContentFile(



        buffer.getvalue(),



        f'{product.barcode}.png'


    )
