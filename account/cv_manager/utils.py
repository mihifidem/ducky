import qrcode
from io import BytesIO
from django.http import HttpResponse

def generate_qr(cv_url):
    """
    Genera un código QR a partir de una URL y devuelve un objeto HttpResponse con la imagen PNG.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(cv_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar la imagen en memoria
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")
