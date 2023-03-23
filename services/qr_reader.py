import cv2
from pyzbar.pyzbar import decode
from core.config import logger


def qr_reader(filename):
    """Read an image and decode the QR code.

    Args:
        filename (string): Path to file

    Returns:
        value (string): Value from QR code
    """
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 125, 1)
    qr_decoded = decode(thresh)
    if len(qr_decoded) > 0:
        value = qr_decoded[0].data.decode('utf-8')
        logger.info(f'Success decoded: {filename}. \n'
                    f'Result: {value}')
        return value
    elif thresh.mean() < 127:
        try:
            value = decode(255 - thresh)[0].data.decode('utf-8')
            if value:
                logger.info(f'Success decoded: {filename}. \n'
                            f'Result: {value}')
                return value
        except Exception as e:
            logger.warning(e)
            pass
    logger.warning(f'Not decoded: {filename}.')
    return 'QR пустой или плохого качества. Давай другой.'
