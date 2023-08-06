import qrcode

# Text or data you want to encode in the QR code
data = "Hello, this is a free QR code!"

# Generate the QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR code data
img = qr.make_image(fill_color="black", back_color="white")

# Save the QR code image to a file
img.save("free_qr_code.png")

print("Free QR code generated and saved as 'free_qr_code.png'.")