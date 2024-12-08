import functions_framework
from flask import request, jsonify
import io
import PyPDF2
import docx2txt
import markdownify


@functions_framework.http
def convert_file_to_text(request):
    if request.method != "POST":
        return jsonify({"error": "Only POST method is allowed"}), 405

    if "file_update" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file_update"]
    filename = file.filename
    file_extension = filename.split(".")[-1].lower()

    if file_extension == "pdf":
        text = convert_pdf_to_text(file)
    elif file_extension == "docx":
        text = convert_docx_to_text(file)
    else:
        text = file.read().decode("utf-8")
        text = format_text(text)
        return jsonify({"text": text})

    text = format_text(text)

    return jsonify({"text": text})

def format_text(text):
    # This is a simple example, you might need a more sophisticated conversion
    md_txt = markdownify.markdownify(text, heading_style="ATX")
    no_nl_txt = md_txt.replace('\n', ' ')
    return no_nl_txt


def convert_pdf_to_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


def convert_docx_to_text(file):
    text = docx2txt.process(file)
    return text
