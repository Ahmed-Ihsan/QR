import os
import qrcode
import datetime
import random
import string
from flask import Flask, render_template, request, send_file
from io import BytesIO

app = Flask(__name__)

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

def generate_random_filename(length=8):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        place = request.form["place"]
        topic = request.form["topic"]

        qr_code_img = generate_personalized_qr_code(name, place, topic)

        # Generate a random filename for the image
        filename = generate_random_filename()

        # Create the 'static' folder if it doesn't exist
        if not os.path.exists("static"):
            os.makedirs("static")

        # Save the QR code image to the 'static' folder
        filepath = f"static/{filename}.png"
        qr_code_img.save(filepath)

        return render_template("result.html", filename=f"{filename}.png")
    return render_template("index.html")

@app.route("/download/<filename>")
def download_qr_code(filename):
    # Read the image from the 'static' folder
    filepath = f"static/{filename}"
    img_data = open(filepath, "rb").read()

    # Send the file for download
    return send_file(BytesIO(img_data), as_attachment=True, attachment_filename=f"{filename}")

if __name__ == "__main__":
    app.run(debug=True)
