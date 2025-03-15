# modules/resume_parser.py
import PyPDF2
import docx
import io

def extract_text_from_resume(uploaded_file):
    """Extract text from PDF or DOCX resume file"""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension in ['docx', 'doc']:
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Please upload a PDF or DOCX file.")

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    text = ""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.getvalue()))
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    
    return text

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    doc = docx.Document(io.BytesIO(docx_file.getvalue()))
    text = ""
    
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    return text
