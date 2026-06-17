import qrcode
import barcode
from barcode.writer import ImageWriter


def generate_barcode(code):

    ean = barcode.get(
        'code128',
        code,
        writer=ImageWriter()
    )

    filename = ean.save(
        f'media/barcodes/{code}'
    )

    return filename


def generate_qr(data, path):

    qr = qrcode.make(data)

    qr.save(path)
