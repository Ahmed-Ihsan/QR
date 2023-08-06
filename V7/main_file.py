import os
import qrcode
import datetime
import random
import string
from flask import Flask, render_template, request, send_file
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database URI
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

def create_pdf(filename, title, headings, paragraphs, image_path):
    # Create a new PDF document
    c = canvas.Canvas(filename, pagesize=letter)

    # Define styles for the title, headings, and paragraphs
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    paragraph_style = styles["Normal"]

    # Set the font and font size for the title
    title_style.fontName = "Helvetica-Bold"
    title_style.fontSize = 16
    c.drawCentredString(300, 750, title)

    # Write the current date to the PDF document
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, "Date: " + current_date)

    # Write the headings to the PDF document
    y_position = 700
    for heading in headings:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, heading)
        y_position -= 20

    # Write the paragraphs to the PDF document
    y_position -= 20
    for paragraph in paragraphs:
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, paragraph)
        y_position -= 20

    # Add the image to the PDF report
    if image_path:
        img = ImageReader(image_path)
        c.drawImage(img, 100, 100, width=200, height=200)

    # Save the PDF document
    c.save()
    
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
        filepath = f"static/image/{filename}.png"
        qr_code_img.save(filepath)
        
        # Generate the PDF report
        title = "QR Code Report"
        headings = ["Name", "Place", "Topic"]
        paragraphs = [
            f"Name: {data['name']}",
            f"Place: {data['place']}",
            f"Topic: {data['topic']}"
        ]
        create_pdf(f"static/pdf/{filename}.pdf", title, headings, paragraphs, filepath)

        # Delete the temporary QR code image after creating the PDF
        # os.remove(filepath)

        return render_template("result.html", filename=f"{filename}.png",fileimage= f"image/{filename}.png")
    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    # Send the PDF file for download
    filename = filename.replace('png','pdf')
    return send_file(f'static/pdf/{filename}', as_attachment=True, attachment_filename=f"{filename}")


@app.route("/users")
def show_users():
    users = User.query.all()
    return render_template("users.html", users=users)

if __name__ == "__main__":
    # Create the database tables if they don't exist
    db.create_all()
    app.run(debug=True)
