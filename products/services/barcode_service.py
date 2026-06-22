import barcode

from barcode.writer import ImageWriter

from io import BytesIO

from django.core.files.base import ContentFile


def generate_barcode(product):

    code = product.barcode

    ean = barcode.get(


        'code128',


        code,


        writer=ImageWriter()


    )

    buffer = BytesIO()

    ean.write(buffer)

    filename = f"{code}.png"

    return ContentFile(

        buffer.getvalue(),

        filename

    )
