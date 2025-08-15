from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdf():
    text_to_add = request.form['text']
    pdf_file = request.files['pdf']
    if pdf_file:
        # Create a new PDF with text to overlay
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 1)
        can.setFillColorRGB(1, 1, 1)  # Set color to white
        can.drawString(
            50, 750,
            text_to_add)  # Adjust coordinates to place text at the top
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        existing_pdf = PdfReader(pdf_file)
        output_pdf = PdfWriter()

        # Merge the new pdf with the old pdf
        for i, page in enumerate(existing_pdf.pages):
            page.merge_page(new_pdf.pages[0])
            output_pdf.add_page(page)

        output_pdf_path = 'modified_pdf.pdf'
        with open(output_pdf_path, 'wb') as out:
            output_pdf.write(out)

        return send_file(output_pdf_path, as_attachment=True)

    return 'No file uploaded', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080)  # Update to use Replit's recommended host and port
