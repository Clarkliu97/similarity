import os
import tempfile
from docx import Document


file_error_choices = [
    (0, "File name not valid"),
    (1, "File is corrupted"),
    (2, "Invalid file extension"),
    (3, "Created_at date not found"),
    (4, "Invalid created_at date format"),
    (5, "File without words"),
    (6, "File without aurthor"),
]

report_choices = [
    ("Complete", "Complete"),
    ("Failed", "Failed"),
    ("Inprogress", "Inprogress"),
]

task_error_choices = [
    (1, "File not found"),
    (2, "No file with unique content"),
    (3, "Unknown author"),
    (4, "Threshold not found"),
    (5, "Error in file"),
]


def get_doc_text(file):

    tempf, tempfn = tempfile.mkstemp(suffix=".doc")
    for chunk in file.chunks():
        os.write(tempf, chunk)
    from subprocess import Popen, PIPE

    cmd = ["antiword", tempfn]
    p = Popen(cmd, stdout=PIPE)
    stdout, _ = p.communicate()
    text = stdout.decode("ascii", "ignore")
    return text


def extracttext(file):
    doc = Document(file)
    docText = "\n\n".join(paragraph.text for paragraph in doc.paragraphs)
    return docText
