import qrcode

# Take user input for the name, place, and topic
name = input("Enter your name: ")
place = input("Enter your place: ")
topic = input("Enter the topic: ")

# Combine the user input into the data string
data = f"Name: {name}\nPlace: {place}\nTopic: {topic}"

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
img.save("personalized_qr_code.png")

print("Personalized QR code generated and saved as 'personalized_qr_code.png'.")
