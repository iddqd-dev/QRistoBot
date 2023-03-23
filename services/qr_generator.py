import qrcode
from core.config import logger


def qr_generator_h(data):
    """Read an data and create the QR code.

    Args:
        data (string): Data for convert to QR

    Returns:
        img (Image): QR Code
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    try:
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    except Exception as ex:
        logger.error(ex)
        return ex