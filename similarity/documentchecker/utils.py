import os
import tempfile
from docx import Document


def get_doc_text(file):
    
    tempf, tempfn = tempfile.mkstemp(suffix='.doc')
    for chunk in file.chunks():
        os.write(tempf, chunk)
    from subprocess import Popen, PIPE
    cmd = ['antiword', tempfn]
    p = Popen(cmd, stdout=PIPE)
    stdout, _ = p.communicate()
    text =  stdout.decode('ascii', 'ignore')
    return text


def extracttext(file):
    doc=Document(file)
    docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)
    return docText
