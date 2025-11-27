''' Resume Service File Helper Functions '''

import fitz
import docx
from docx.oxml.ns import qn


def _extract_pdf_text(path: str):
    ''' Extract text from a PDF file '''
    if not path.endswith('.pdf'):
        return
    
    doc = fitz.open(path)
    parts = []
    for page in doc:
        parts.append(page.get_text("text"))

        for link in page.get_links():
            if 'uri' in link:
                parts.append(f"(Link: {link.get('text','')} {link['uri']})")

    return "\n".join(parts)



def _extract_docx_text(path: str):
    ''' Extract text from a DOCX file '''
    if not path.endswith('.docx'):
        return
    
    doc = docx.Document(path)
    out = []

    for para in doc.paragraphs:
        if para.text.strip():
            out.append(para.text.strip())

        # Find hyperlink elements in the paragraph XML and resolve their r:id to a URL
        for hyperlink in para._p.findall('.//' + qn('w:hyperlink')):
            rel_id = hyperlink.get(qn('r:id'))
            if not rel_id:
                continue
            try:
                url = doc.part.rels[rel_id].target_ref
            except KeyError:
                continue

            # Extract visible text inside the hyperlink element
            text_nodes = hyperlink.findall('.//' + qn('w:t'))
            link_text = "".join([t.text for t in text_nodes if t.text]).strip() or "Link"
            out.append(f"(Link: {link_text} {url})")

    return "\n".join(out)




if __name__ == "__main__":
    # test usage
    path = "/home/dk/Downloads/output.docx"
    
    if path.endswith('.docx'):
        docx_text = _extract_docx_text(path)
        print(docx_text)
        
    elif path.endswith('.pdf'):
        pdf_text = _extract_pdf_text(path)
        print(pdf_text)