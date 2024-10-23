import qrcode
from PIL import Image
import os
from urllib.parse import urlparse

def generate_qr_code(url, index, folder_path):
    # Parse the URL to get the domain name
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image with custom color and transparent background
    qr_img = qr.make_image(fill_color='#f6a512', back_color='transparent')

    # Convert to RGBA to ensure transparency is handled
    qr_img = qr_img.convert("RGBA")

    # Create folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save QR code image with sequential filename
    filename = os.path.join(folder_path, f'{index}.png')
    qr_img.save(filename)

    print(f'QR code saved as {filename}')

def main():
    # List of URLs
    urls = [
        "https://drive.google.com/file/d/1j8Ozn-DYlB35sBsXHniGe9qUZNZ-h35u/view?usp=drive_link",
        "https://drive.google.com/file/d/1iy8yJ41qy0pvXta1LexYpzvxC2rFftM5/view?usp=drive_link",
        "https://drive.google.com/file/d/1i_JfRuzNh5dsAv5ry_RqZrEAus_1YxOR/view?usp=drive_link",
        "https://drive.google.com/file/d/1HVOzNfpQ9m8Q6WMZ5xO_OBGq31uQ922o/view?usp=drive_link",
        "https://drive.google.com/file/d/19hCaNPDdNi-E6N8mI2j047YtgUJ-z-9W/view?usp=drive_link",
        "https://drive.google.com/file/d/16_7mGX6aB1CIGQfUSvkVCTheT7zt9UnE/view?usp=drive_link",
        "https://drive.google.com/file/d/14hHK0E4T0j48k3oq99zt-kXdpd4gjGxC/view?usp=drive_link"
    ]

    # Folder path to save QR codes
    folder_path = 'qr_codes'

    # Generate and save QR codes
    for i, url in enumerate(urls, start=1):
        generate_qr_code(url, i, folder_path)

if __name__ == "__main__":
    main()
