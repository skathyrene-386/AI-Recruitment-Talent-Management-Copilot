import pdfplumber
import docx

def extract_text_from_pdf(file):
    text=""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text=page.extract_text()
            if page_text:
                text += page_text+"\n"
    return text
    
def extract_text_from_docx(file):
    document=docx.Document(file)
    text="\n".join(para.text for para in document.paragraphs if para.text.strip())
    return text

def extract_text(file,file_name):
    lower_name=file_name.lower()
    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif lower_name.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        raise ValueError(f"Unsupported file type:{file_name},Only PDF and DOCX are supported.")
