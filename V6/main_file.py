import os
import qrcode
import datetime
import random
import string
from flask import Flask, render_template, request, send_file
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database URI
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

def generate_personalized_qr_code(data, version,box_size,border):
    # Combine the user input and current date/time into the data string
    data_str = f"Name: {data['name']}\nPlace: {data['place']}\nTopic: {data['topic']}\nDate and Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Generate the QR code with the user-specified version
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=4,
    )
    qr.add_data(data_str)
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
        data = {
            'name': request.form["name"],
            'place': request.form["place"],
            'topic': request.form["topic"]
        }
        version = int(request.form["version"])
        box_size = int(request.form["box_size"])
        border = int(request.form["border"])

        # Create a new User instance and add it to the database
        user = User(name=data['name'], place=data['place'], topic=data['topic'])
        db.session.add(user)
        db.session.commit()

        qr_code_img = generate_personalized_qr_code(data, version, box_size, border)

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

@app.route("/users")
def show_users():
    users = User.query.all()
    return render_template("users.html", users=users)

if __name__ == "__main__":
    # Create the database tables if they don't exist
    db.create_all()
    app.run(debug=True)
