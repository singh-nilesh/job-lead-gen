""" app.services.resume.Ingestion_service
    testing: ResumeIngestionService._extract_text
"""

import pytest
from app.services.resume.Ingestion_service import ResumeIngestionService
import re
    


@pytest.mark.asyncio
async def test_extract_resume_text_validation(app_db_mock, vector_store_mock):
    """ Test the resume text extraction and ingestion process """
    service = ResumeIngestionService(db=app_db_mock, vector_store=vector_store_mock)

    # Mock resume file path and user ID
    resume_filepath = "/home/dk/Downloads/output.docx"
    user_id = "1"
    result = service._extract_text(resume_filepath, user_id)

    # Print the extracted result for debugging
    print("Extracted Resume Text:\n", result)
    
    # Assert besed on Resume content
    assert result.startswith("NIL"), "Starts with name: NIL"
    assert re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", result), " contains a valid email address"
    assert len(re.findall(r"(https?://\S+|www\.\S+)", result)) == 4, " there are total 4 links in the resume"