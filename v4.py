import qrcode
import datetime

def generate_personalized_qr_code(name, place, topic):
    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Combine the user input and current date/time into the data string
    data = f"Name: {name}\nPlace: {place}\nTopic: {topic}\nDate and Time: {current_datetime}"

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

    return img

def main():
    # Take user input for the name, place, and topic
    name = input("Enter your name: ")
    place = input("Enter your place: ")
    topic = input("Enter the topic: ")

    # Generate the personalized QR code
    qr_code_img = generate_personalized_qr_code(name, place, topic)

    # Save the QR code image to a file
    qr_code_img.save("personalized_qr_code_with_time.png")

    print("Personalized QR code with date and time generated and saved as 'personalized_qr_code_with_time.png'.")

if __name__ == "__main__":
    main()
