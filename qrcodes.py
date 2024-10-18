import cv2
from pyzbar.pyzbar import decode
import qrcode


def scan_qr_code(image_path: str):
    img = cv2.imread(image_path)
    qr_codes = decode(img)

    if qr_codes:
        for qr_code in qr_codes:
            qr_data = qr_code.data.decode('utf-8')
            print(f"QR Code data: {qr_data}")
            return qr_data
    else:
        print("No QR code found")
        return None



def generate_qr_code(data: str, file_path: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(file_path)

if __name__ == "__main__":
    generate_qr_code("https://www.example.com", "example_qr.png")
    print("QR code generated and saved as example_qr.png")
    scan_qr_code("example_qr.png")