''' Generate DOCX from Text '''

from docxtpl import DocxTemplate, RichText
from docx import Document

from app.core.config import Settings

def _parse_to_docx(resume_data:dict, output_path:str = None, user_id: str = None):
    ''' Save text content to a DOCX file '''
    
    if not output_path:
        output_path = f"/tmp/resume_{user_id}.docx" if user_id else "/tmp/resume.docx"

    print(f" template path: {Settings.ARTIFACTS_DIR}/resume_template.2.0.docx")
    
    template = DocxTemplate(f"{Settings.ARTIFACTS_DIR}/resume_template.2.0.docx")

    # Process profile contanct details
    resume_data["profile"]["contact_line"] = _build_contact_line(template, resume_data["profile"])

    # Process links in work_experience and projects
    for ent in (resume_data.get("work_experience") or []) + (resume_data.get("projects") or []):
        rt = RichText()

        if isinstance(ent.get("link"), str) and ent["link"].startswith("http"):

            rt.add(
                "[LINK]",
                url_id=template.build_url_id(ent["link"]),
                font="Times New Roman",
                color="0000FF"
            )
            ent["link"] = rt
        else:
            ent["link"] = None
    
    # Render the template with resume data
    template.render(resume_data)
    template.save(output_path)
    
    # clean empty line
    doc = Document(output_path)
    for para in doc.paragraphs:
        if not para.text.strip():
            p = para._element
            p.getparent().remove(p)
    
    # final save
    doc.save(output_path)
    return output_path




def _build_contact_line(template, profile):
    rt = RichText()

    items = [
        (profile.get("location"), False),
        (profile.get("email"), False),
        (profile.get("phone"), False),
        (profile.get("website"), True),
        (profile.get("linkedin"), True),
        (profile.get("github"), True),
    ]

    first = True
    for value, is_link in items:
        if not value:
            continue

        if not first:
            rt.add(" | ")
        first = False

        if is_link:
            rt.add(
                value,
                url_id=template.build_url_id(value),
                font="Times New Roman",
                color="0000FF"
            )
        else:
            rt.add(value)

    return rt
