from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
import datetime

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


if __name__ == "__main__":
    # Example content for the PDF report
    title = "Monthly Report"
    headings = ["Heading 1", "Heading 2", "Heading 3"]
    paragraphs = [
        "This is a sample PDF report created using Python and ReportLab.",
        "You can add more content here as needed.",
        "Each heading and paragraph is placed on a separate line in the PDF.",
    ]
    image_path = "D:\D\QR\V7\static\zyo02oja.png"  # Replace this with the path to your image

    # Specify the filename for the PDF report
    filename = "monthly_report.pdf"

    # Create the PDF report
    create_pdf(filename, title, headings, paragraphs, image_path)
