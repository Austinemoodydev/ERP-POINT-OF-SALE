from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfgen import canvas


def product_label(product):

    filename = f'label_{product.id}.pdf'

    pdf = canvas.Canvas(filename)

    pdf.drawString(


        100,


        750,


        product.name

    )

    pdf.drawImage(


        product.barcode_image.path,


        100,


        600,


        width=250,


        height=80

    )

    pdf.save()

    return filename


def bulk_labels(products):

    pdf = SimpleDocTemplate(


        'bulk_labels.pdf'

    )

    story = []

    for p in products:

        pass

    pdf.build(story)


def product_label(product):

    filename = f'label_{product.id}.pdf'

    pdf = canvas.Canvas(filename)

    pdf.drawString(


        100,


        750,


        product.name

    )

    pdf.drawImage(


        product.barcode_image.path,


        100,


        600,


        width=250,


        height=80

    )

    pdf.save()

    return filename
